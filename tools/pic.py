# Compresor y descompresor de los dibujos de OPEN.COM (PIC100/PIC101.MSX). araubi, 2026. MIT.
"""Formato de dibujo de OPEN.COM (PIC100/101): por cada par de líneas, N controles alternos
literal/ceros, filtro XOR acumulado, bytes pares = línea par, impares (rotados 2) = línea impar."""
def rl2(a): return ((a<<2)|(a>>6))&255
def rr2(a): return ((a>>2)|(a<<6))&255
def decodifica(d):
    W=d[0]; H=d[1]; p=2; vram=bytearray(128*H)
    for it in range(H//2):
        n=d[p]; p+=1; ctl=d[p:p+n]; p+=n; buf=bytearray(); lit=True
        for k in ctl:
            if lit: buf+=d[p:p+k]; p+=k
            else: buf+=bytes(k)
            lit=not lit
        buf+=bytes(2*W-len(buf))
        a=0
        for j in range(W):
            a^=buf[2*j]; buf[2*j]=a
            a^=buf[2*j+1]; buf[2*j+1]=rl2(a)
        for j in range(W):
            vram[(2*it)*128+j]=buf[2*j]; vram[(2*it+1)*128+j]=buf[2*j+1]
    return vram,W,H,p
def codifica(vram,W,H):
    out=bytearray([W,H])
    for it in range(H//2):
        e=[vram[(2*it)*128+j] for j in range(W)]; o=[vram[(2*it+1)*128+j] for j in range(W)]
        buf=bytearray(2*W); a=0
        for j in range(W):
            buf[2*j]=e[j]^a; a=e[j]
            v=rr2(o[j]); buf[2*j+1]=v^a; a=v
        # quita ceros finales
        n=len(buf)
        while n and buf[n-1]==0: n-=1
        ctl=[]; data=bytearray(); i=0; lit=True
        while i<n:
            j=i
            if lit:
                # literal hasta encontrar 3+ ceros seguidos
                while j<n and j-i<255:
                    if buf[j]==0 and j+2<n and buf[j+1]==0 and buf[j+2]==0: break
                    if buf[j]==0 and j+1>=n: break
                    j+=1
                data+=buf[i:j]
            else:
                while j<n and buf[j]==0 and j-i<255: j+=1
            ctl.append(j-i); i=j; lit=not lit
        assert len(ctl)<256
        out+=bytes([len(ctl)])+bytes(ctl)+data
    return bytes(out)
