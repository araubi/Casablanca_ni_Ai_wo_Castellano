#!/usr/bin/env python3
"""Genera font/titulo_es.png: el título en castellano que sustituye al japonés en PIC101.MSX.
Zona x 228-511, y 4-52 de la pantalla de 512x200 (SCREEN 6: píxeles el doble de altos que de anchos).
Usa FreeSerif Bold Italic (GNU FreeFont) y la fuente de la traducción. araubi, 2026. MIT.
uso: genera_titulo.py   (necesita Pillow y fonts-freefont-ttf)"""
import os,sys,glob
from PIL import Image,ImageDraw,ImageFont
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(RAIZ,'tools'))
from fuente import construye as fnt, codifica
X0,Y0,W,H=228,4,284,49
def ttf(nombre,t): return ImageFont.truetype(glob.glob('/usr/share/fonts/**/'+nombre,recursive=True)[0],t)
def texto(s,f,umbral=110):
    d=ImageDraw.Draw(Image.new('L',(1,1))); b=d.textbbox((0,0),s,font=f)
    im=Image.new('L',(b[2]-b[0]+8,b[3]-b[1]+8),0); ImageDraw.Draw(im).text((4-b[0],4-b[1]),s,font=f,fill=255)
    w,h=im.size; im=im.resize((max(1,w//2),max(1,h//4)),Image.LANCZOS)
    return im.point(lambda p:255 if p>umbral else 0)
def pequeno(s):
    G=fnt(); cs=codifica(s); im=Image.new('L',(8*len(cs),11),0)
    for i,c in enumerate(cs):
        for y in range(11):
            for x in range(8):
                if G[c*11+y]&(0x80>>x): im.putpixel((i*8+x,y),255)
    return im
m=Image.new('1',(W,H),0)
def pega(im,x,y): m.paste(im.convert('1'),(x-X0,y-Y0),im.convert('1'))
t1=texto('A Casablanca,',ttf('FreeSerifBoldItalic.ttf',84)); t2=texto('con amor',ttf('FreeSerifBoldItalic.ttf',84))
t3=pequeno('El asesino que cruzó el tiempo')
pega(t1,250,6); y2=6+t1.size[1]-2; pega(t2,505-t2.size[0],y2)
yl=y2+t2.size[1]+1
for x in range(300,508): m.putpixel((x-X0,yl-Y0),1)
pega(t3,507-t3.size[0],yl+3)
m.save(os.path.join(RAIZ,'font','titulo_es.png'))
