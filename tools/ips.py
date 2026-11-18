#!/usr/bin/env python3
"""Parches IPS de la traducción de Casablanca ni Ai wo.
  ips.py crea   original.dsk traducido.dsk parche.ips
  ips.py aplica original.dsk parche.ips salida.dsk
araubi, 2026. Licencia MIT."""
import sys,hashlib
def crea(a,b):
    assert len(a)==len(b)
    out=bytearray(b'PATCH'); i=0
    while i<len(b):
        if a[i]==b[i]: i+=1; continue
        j=i
        # agrupa cambios separados por menos de 6 bytes iguales
        while j<len(b) and j-i<0xFFFF:
            if a[j]!=b[j]: j+=1; continue
            k=j
            while k<len(b) and a[k]==b[k] and k-j<6: k+=1
            if k-j>=6 or k>=len(b): break
            j=k
        if i==0x454F46: i-=1          # el desplazamiento «EOF» no puede usarse
        out+=i.to_bytes(3,'big')+(j-i).to_bytes(2,'big')+b[i:j]; i=j
    return bytes(out+b'EOF')
def aplica(a,p):
    assert p[:5]==b'PATCH','no es un IPS'
    d=bytearray(a); i=5
    while p[i:i+3]!=b'EOF':
        o=int.from_bytes(p[i:i+3],'big'); n=int.from_bytes(p[i+3:i+5],'big'); i+=5
        if n==0:
            r=int.from_bytes(p[i:i+2],'big'); d[o:o+r]=p[i+2:i+3]*r; i+=3
        else:
            d[o:o+n]=p[i:i+n]; i+=n
    return bytes(d)
if __name__=='__main__':
    m=sys.argv[1]; x,y,z=sys.argv[2:5]
    if m=='crea':
        a=open(x,'rb').read(); b=open(y,'rb').read(); p=crea(a,b)
        assert aplica(a,p)==b; open(z,'wb').write(p)
    else:
        r=aplica(open(x,'rb').read(),open(y,'rb').read()); open(z,'wb').write(r)
    print(z,hashlib.sha1(open(z,'rb').read()).hexdigest())
