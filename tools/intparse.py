# Analizador de CASAB.INT (guion) usando la tabla de salas de CASAB.TBL
import struct
ALEN={0x80:3,0x81:1,0x82:1,0x83:0,0x84:0,0x89:0,0x90:2,0x91:2,0x92:1,0x93:1,0x94:0,0x95:2,0x96:1,0x97:1,0x98:1,0x99:1}
def rooms(tbl):
    r=[]
    for i in range(256):
        o,l=struct.unpack_from('<HH',tbl,i*4); r.append((o,l))
    return r
def parse_chunk(b):
    """devuelve lista de reglas: (cond1,cond2,acciones[(op,pos,args)]) ; pos absoluta dentro del trozo"""
    p=0; rules=[]
    while p<len(b):
        start=p
        conds=[]
        for k in range(2):
            c=[]
            while b[p]!=0xFF:
                if b[p]>=0xF0: c.append(b[p:p+1]); p+=1
                else: c.append(b[p:p+2]); p+=2
            p+=1; conds.append(c)
        acts=[]
        while b[p]!=0xFF:
            op=b[p]
            if op not in ALEN: raise ValueError('op %02x en %d'%(op,p))
            n=ALEN[op]; acts.append((op,p,b[p+1:p+1+n])); p+=1+n
        p+=1
        rules.append((start,conds,acts))
    return rules
if __name__=='__main__':
    # comprobación: uso: intparse.py disco2_original.dsk
    import sys,os
    sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
    from dsk import Disco
    D2=Disco(open(sys.argv[1],'rb').read())
    tbl=D2.lee('CASAB.TBL'); it=D2.lee('CASAB.INT'); msg=D2.lee('CASAB.MSG')
    starts={0}|{i+1 for i,c in enumerate(msg) if c==0}
    tot=0; bad=0; used=set(); n90=0
    for i,(o,l) in enumerate(rooms(tbl)):
        if l==0: continue
        try: rs=parse_chunk(it[o:o+l])
        except Exception as e: print('sala',i,o,l,e); bad+=1; continue
        tot+=1
        for s,c,a in rs:
            for op,p,arg in a:
                if op==0x90:
                    v=arg[0]|arg[1]<<8; n90+=1
                    if v not in starts: print('90h fuera',i,hex(v))
                    used.add(v)
    print('salas',tot,'malas',bad,'90h',n90,'mensajes usados',len(used))
