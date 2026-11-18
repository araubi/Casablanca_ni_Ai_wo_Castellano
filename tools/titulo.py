"""Pone el título en castellano (font/titulo_es.png) en PIC101.MSX. araubi, 2026. MIT."""
import os
from PIL import Image
import pic
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
X0,Y0=228,4
def aplica(orig):
    v,W,H,_=pic.decodifica(orig); v=bytearray(v)
    m=Image.open(os.path.join(RAIZ,'font','titulo_es.png')).convert('1')
    for y in range(m.size[1]):
        for x in range(m.size[0]):
            X=X0+x; Y=Y0+y; o=Y*128+X//4; s=6-2*(X%4)
            c=0 if m.getpixel((x,y)) else 3
            v[o]=(v[o]&~(3<<s)&255)|(c<<s)
    return pic.codifica(v,W,H)
