#!/usr/bin/env python3
"""Volcado legible de las reglas del juego (palabras FD resueltas, mensajes en castellano).
uso: reglas2.py disco2_original.dsk > reglas.txt"""
import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from intparse import rooms,parse_chunk
from dsk import Disco
D2=Disco(open(sys.argv[1],'rb').read())
tbl=D2.lee('CASAB.TBL'); it=D2.lee('CASAB.INT')
voc=tbl[0x4e6:].split(b'\0')
# mensajes españoles por desplazamiento original
es={}
for l in open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'trad','mensajes.txt'),encoding='utf8'):
    if '|' in l:
        o,t=l.rstrip('\n').split('|',1)
        try: es[int(o,16)]=t
        except: pass
def w(i):
    s=voc[i].decode('cp932','replace').split() if i<len(voc) else []
    en=[x for x in s if x.isascii()]
    return (en[0] if en else (s[0] if s else '?'))
for r,(o,l) in enumerate(rooms(tbl)):
    if l==0: continue
    print('== SALA',r)
    prev=None
    for s,(c1,c2),a in parse_chunk(it[o:o+l]):
        alts=[];cur=[];
        for x in c1:
            if len(x)==1 and x[0]==0xFE: alts.append(cur);cur=[];continue
            cur.append(x)
        alts.append(cur)
        res=[]
        for k,al in enumerate(alts):
            ref = res[-1] if res else (prev[0] if prev else [])
            o2=[]
            for j,x in enumerate(al):
                if len(x)==1 and x[0]==0xFD: o2.append(ref[j] if j<len(ref) else '?')
                elif len(x)==1 and x[0]==0xFC: o2.append('*')
                elif len(x)==1: o2.append('%02X'%x[0])
                else: o2.append(w(x[1]) if x[0]==0 else '%02X:%02X'%(x[0],x[1]))
            res.append(o2)
        prev=res
        cs=' '.join('%02X:%02X'%(x[0],x[1]) if len(x)==2 else '%02X'%x[0] for x in c2)
        acts=[]
        for op,p,arg in a:
            if op==0x90: acts.append('«%s»'%es.get(arg[0]|arg[1]<<8,'?')[:70])
            else: acts.append('%02X'%op+(':'+arg.hex() if arg else ''))
        print('  %s / [%s] -> %s'%(' | '.join(' '.join(x) for x in res) or '(auto)',cs,' '.join(acts)))
