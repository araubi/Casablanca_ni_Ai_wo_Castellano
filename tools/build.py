#!/usr/bin/env python3
"""Construye los discos en castellano de Casablanca ni Ai wo a partir de los originales.
uso: build.py d1_original.dsk d2_original.dsk salida_dir"""
import sys,os,hashlib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from dsk import Disco
from fuente import kanji_fnt
import parche_runadv
SHA={'d1':'073e5fa25bbf9bf89e6f3f59bde7d86b826b2d97','d2':'f99fb8c72065ae9128067b10d394599f0e729a50'}
def main(p1,p2,out,textos=True):
    a=open(p1,'rb').read(); b=open(p2,'rb').read()
    assert hashlib.sha1(a).hexdigest()==SHA['d1'],'disco 1 distinto del original'
    assert hashlib.sha1(b).hexdigest()==SHA['d2'],'disco 2 distinto del original'
    D1=Disco(a); D2=Disco(b)
    id_relleno=250
    if textos:
        import textos as T
        tbl,msg,intf,id_relleno,largos=T.construye(D2.lee('CASAB.TBL'),D2.lee('CASAB.MSG'),D2.lee('CASAB.INT'))
        D2.escribe('CASAB.TBL',tbl); D2.escribe('CASAB.MSG',msg); D2.escribe('CASAB.INT',intf)
    com,S=parche_runadv.parchea(D1.lee('RUNADV.COM'),id_relleno,*([[l or parche_runadv.LARGOS[i] for i,l in enumerate(largos)]] if textos else []))
    D1.escribe('RUNADV.COM',com)
    D1.escribe('KANJI.FNT',kanji_fnt(D1.lee('KANJI.FNT')))
    os.makedirs(out,exist_ok=True)
    open(os.path.join(out,'Casablanca_ES_disco1.dsk'),'wb').write(D1.imagen())
    open(os.path.join(out,'Casablanca_ES_disco2.dsk'),'wb').write(D2.imagen())
    print('RUNADV.COM %d bytes, ampliación hasta %04X'%(len(com),S['FIN_EXT']))
if __name__=='__main__':
    args=[x for x in sys.argv[1:] if not x.startswith('-')]
    main(*args,textos='--sin-textos' not in sys.argv)
