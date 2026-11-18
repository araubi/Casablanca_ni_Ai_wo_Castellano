"""Reconstruye CASAB.MSG, CASAB.TBL y CASAB.INT con los textos en castellano.
trad/mensajes.txt : DESPLAZ|texto   ('/' = salto de línea; mensajes sin traducir se quedan en japonés)
trad/vocabulario.txt : ID|PALABRAS SEPARADAS POR ESPACIOS   (ID del original; una línea RELLENO|...)
trad/objetos.txt : N|corto|largo"""
import os,struct,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from fuente import codifica
from intparse import rooms,parse_chunk
DIR=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'trad')
RELLENO_EXTRA=int(os.environ.get('MSG_RELLENO','0'))
def lee_tabla(nombre,ncampos):
    r={}
    p=os.path.join(DIR,nombre)
    if not os.path.exists(p): return r
    for l in open(p,encoding='utf-8'):
        l=l.rstrip('\n')
        if not l.strip() or l.startswith('#'): continue
        c=l.split('|')
        r[c[0].strip()]=c[1:] if ncampos>2 else c[1]
    return r
def mensajes(msg):
    out=[];p=0
    while p<len(msg):
        e=msg.index(0,p); out.append((p,msg[p:e])); p=e+1
    return out
def construye(tbl,msg,intf):
    tr=lee_tabla('mensajes.txt',2)
    nuevo=bytearray(); mapa={}
    for k,(o,b) in enumerate(mensajes(msg)):
        t=tr.get('%04X'%o)
        if t is not None:
            b=codifica(t.replace('/','\n'))
        if RELLENO_EXTRA and k>60: b=codifica('x%d'%k)
        if k==1 and RELLENO_EXTRA: nuevo+=b'\0'*RELLENO_EXTRA
        mapa[o]=len(nuevo)
        assert len(b)<511,('mensaje largo',hex(o),len(b))
        nuevo+=b+b'\0'
    assert len(nuevo)<=0xFFFF,('CASAB.MSG pasa de 64 KB',len(nuevo))
    # INT: reescribe los desplazamientos de la acción 90h
    it=bytearray(intf)
    for i,(o,l) in enumerate(rooms(tbl)):
        if l==0: continue
        for s,c,a in parse_chunk(intf[o:o+l]):
            for op,p,arg in a:
                if op==0x90:
                    v=arg[0]|arg[1]<<8; n=mapa[v]
                    it[o+p+1]=n&255; it[o+p+2]=n>>8
    # TBL
    t=bytearray(tbl[:0x400]); p=0x400
    while tbl[p]!=0xff: p+=1
    p+=1
    while tbl[p]!=0xff: p+=1
    p+=1
    t+=tbl[0x400:p]
    obj=lee_tabla('objetos.txt',3)
    nombres=[]; q=p
    while tbl[q]!=0xff:
        e=tbl.index(0,q); nombres.append(tbl[q:e]); q=e+1
    largos=[]
    for i,nm in enumerate(nombres):
        o=obj.get(str(i+1))
        if o:
            assert len(o[0])<=6,('nombre corto largo',o[0]); t+=codifica(o[0])+b'\0'; largos.append(o[1])
        else: t+=nm+b'\0'; largos.append(None)
    t+=b'\xff'; q+=1
    voc=tbl[q:]; ents=voc.split(b'\0')
    assert ents[-1]==b'\xff',ents[-1]
    ents=ents[:-1]
    vt=lee_tabla('vocabulario.txt',2)
    for i in range(len(ents)):
        if str(i) in vt: ents[i]=codifica(vt[str(i)].strip())
    id_relleno=len(ents)
    ents.append(codifica(vt.get('RELLENO','EL LA LOS LAS').strip()))
    t+=b'\0'.join(ents)+b'\0\xff'
    return bytes(t),bytes(nuevo),bytes(it),id_relleno,largos
