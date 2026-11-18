"""Sustituye ficheros dentro de una imagen FAT12 (MSX-DOS) sin tocar el resto."""
class Disco:
    def __init__(s,data):
        s.d=bytearray(data); d=s.d
        s.bps=d[11]|d[12]<<8; s.spc=d[13]; s.res=d[14]|d[15]<<8; s.nf=d[16]
        s.nroot=d[17]|d[18]<<8; s.tot=d[19]|d[20]<<8; s.spf=d[22]|d[23]<<8
        s.fatoff=s.res*s.bps; s.rootoff=(s.res+s.nf*s.spf)*s.bps; s.dataoff=s.rootoff+s.nroot*32
        s.ncl=(s.tot*s.bps-s.dataoff)//(s.spc*s.bps)+2
        s.fat=bytearray(d[s.fatoff:s.fatoff+s.spf*s.bps])
    def get(s,c):
        o=c*3//2; v=s.fat[o]|s.fat[o+1]<<8
        return v>>4 if c&1 else v&0xfff
    def set(s,c,v):
        o=c*3//2
        if c&1: s.fat[o]=(s.fat[o]&0x0f)|((v<<4)&0xf0); s.fat[o+1]=(v>>4)&0xff
        else: s.fat[o]=v&0xff; s.fat[o+1]=(s.fat[o+1]&0xf0)|((v>>8)&0x0f)
    def entrada(s,nombre):
        n,_,e=nombre.upper().partition('.')
        clave=(n.ljust(8)+e.ljust(3)).encode()
        for i in range(s.nroot):
            o=s.rootoff+i*32
            if s.d[o:o+11]==clave: return o
        return None
    def cadena(s,c):
        r=[]
        while 2<=c<0xff8: r.append(c); c=s.get(c)
        return r
    def lee(s,nombre):
        o=s.entrada(nombre); c=s.d[o+26]|s.d[o+27]<<8; sz=int.from_bytes(s.d[o+28:o+32],'little')
        cs=s.spc*s.bps
        return bytes(b''.join(s.d[s.dataoff+(x-2)*cs:s.dataoff+(x-1)*cs] for x in s.cadena(c))[:sz])
    def escribe(s,nombre,datos):
        o=s.entrada(nombre); assert o is not None, nombre
        c=s.d[o+26]|s.d[o+27]<<8
        for x in s.cadena(c): s.set(x,0)
        cs=s.spc*s.bps; n=(len(datos)+cs-1)//cs
        libres=[x for x in range(2,s.ncl) if s.get(x)==0][:n]
        assert len(libres)==n,'disco lleno'
        for i,x in enumerate(libres):
            s.set(x,libres[i+1] if i+1<n else 0xfff)
            blk=datos[i*cs:(i+1)*cs]; s.d[s.dataoff+(x-2)*cs:s.dataoff+(x-1)*cs]=blk+bytes(cs-len(blk))
        first=libres[0] if n else 0
        s.d[o+26]=first&255; s.d[o+27]=first>>8; s.d[o+28:o+32]=len(datos).to_bytes(4,'little')
    def imagen(s):
        for k in range(s.nf): s.d[s.fatoff+k*s.spf*s.bps:s.fatoff+(k+1)*s.spf*s.bps]=s.fat
        return bytes(s.d)
