#!/usr/bin/env python3
"""Fuente de un byte (8x11) para la traducción: base C-BIOS (licencia BSD), glifos en filas 2-9.
Se añade al final de KANJI.FNT para que OPEN.COM la suba a la VRAM 1A000h."""
import os
CB=open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'font','cbios_font.bin'),'rb').read()
# código propio -> (código C-BIOS o None, ajuste)
MAPA={'á':0xA0,'í':0xA1,'ó':0xA2,'ú':0xA3,'ñ':0xA4,'Ñ':0xA5,'é':0xA6,'ü':0xA7,'¿':0xA8,
      'Á':0xA9,'É':0xAA,'Í':0xAB,'Ó':0xAC,'¡':0xAD,'Ú':0xAE,'Ü':0xAF,'«':0xB0,'»':0xB1,'▼':0xB2,'º':0xB3,'ª':0xB4}
def glifo8(c): return list(CB[c*8:c*8+8])
def mayus_acento(letra,acento):
    g=glifo8(ord(letra))
    out=[0]*11
    for y in range(8): out[2+y]=g[y]
    if acento=='agudo': out[0]=0x10; out[1]=0x20
    elif acento=='dieresis': out[1]=0x48 if False else 0x50
    # la mayúscula C-BIOS ocupa filas 0-6 del 8x8 -> 2-8 aquí; acento en 0-1 con hueco
    return out
def construye():
    f=bytearray(256*11)
    def pon(code,rows8,off=2):
        for y in range(8): f[code*11+off+y]=rows8[y]
    for c in range(0x20,0x7f): pon(c,glifo8(c))
    pon(0xA0,glifo8(0xA0)); pon(0xA1,glifo8(0xA1)); pon(0xA2,glifo8(0xA2)); pon(0xA3,glifo8(0xA3))
    pon(0xA4,glifo8(0xA4)); pon(0xA5,glifo8(0xA5)); pon(0xA6,glifo8(0x82)); pon(0xA7,glifo8(0x81))
    pon(0xA8,glifo8(0xA8)); pon(0xAD,glifo8(0xAD)); pon(0xB0,glifo8(0xAE)); pon(0xB1,glifo8(0xAF))
    pon(0xB3,glifo8(0xA7)); pon(0xB4,glifo8(0xA6))
    for code,l,a in ((0xA9,'A','agudo'),(0xAA,'E','agudo'),(0xAB,'I','agudo'),(0xAC,'O','agudo'),(0xAE,'U','agudo'),(0xAF,'U','dieresis')):
        g=mayus_acento(l,a); f[code*11:code*11+11]=bytes(g)
    # ▼ marcador de "sigue": triángulo pequeño
    tri=[0,0,0,0,0x7C,0x38,0x10,0,0,0,0]
    f[0xB2*11:0xB2*11+11]=bytes(tri)
    return bytes(f)
def codifica(s):
    out=bytearray()
    for ch in s:
        if ch in MAPA: out.append(MAPA[ch])
        elif ch=='\n': out.append(10)
        elif 0x20<=ord(ch)<0x7f: out.append(ord(ch))
        else: raise ValueError('carácter sin glifo: %r en %r'%(ch,s))
    return bytes(out)
def kanji_fnt(orig):
    base=0x8000; destino=0x1A000
    pad=destino-base-len(orig)
    assert pad>=0
    return orig+bytes(pad)+construye()
if __name__=='__main__':
    from PIL import Image
    f=construye(); im=Image.new('L',(16*9,16*12),90)
    for c in range(256):
        for y in range(11):
            b=f[c*11+y]
            for x in range(8): im.putpixel((c%16*9+x,c//16*12+y),255 if b&(0x80>>x) else 0)
    im.resize((16*9*3,16*12*3),Image.NEAREST).save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'font','fuente_es.png'))
