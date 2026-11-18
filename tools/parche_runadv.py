#!/usr/bin/env python3
"""Parchea RUNADV.COM para la traducción: fuente propia, corte por palabras, pausa, entrada
de medio ancho, palabras de relleno, listas de objetos y textos del intérprete en castellano."""
import subprocess,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from fuente import codifica
SRC=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'src')

# Cadenas nuevas (etiqueta, texto). \n = salto de línea.
CADENAS=[
 ('s_err_disco','\nError de disco ('),
 ('s_err_al','): '),
 ('s_leer','al leer'),('s_escribir','al escribir'),
 ('s_dos_puntos',', '),
 ('s_fat','FAT dañada'),
 ('s_e_prot','disco protegido contra escritura'),('s_e_nodisco','no hay disco'),('s_e_crc','error de CRC'),
 ('s_e_seek','error de búsqueda'),('s_e_rnf','sector no encontrado'),('s_e_wf','fallo de escritura'),('s_e_otro','otro error'),
 ('s_pulsa_nl','\nPulsa una tecla.\n'),
 ('s_disco2','Pon el disco 2 en la unidad'),('s_pulsa','y pulsa una tecla.'),
 ('s_titulo1','A Casablanca,'),('s_titulo2','con amor'),
 ('s_switch','Opción «%c» no válida.\n'),
 ('s_no_puedes','No puedes hacer eso.\n'),
 ('s_no_llevas','No lo llevas. '),
 ('s_no_esta','Eso no está aquí. '),
 ('s_pausa','(Pulsa una tecla)'),
 ('s_no_conozco','No conozco la palabra «'),
 ('s_no_conozco2','».\n'),
 ('s_que_haces','¿Qué haces? '),
 ('s_num_partida','¿Número de partida? (0-9) '),
 ('s_grabando','Grabando la partida en el disco.\n'),
 ('s_err_grabar','Error al grabar.\n'),
 ('s_cargando','Cargando la partida del disco.\n'),
 ('s_err_cargar','Error al cargar.\n'),
 ('s_sin_partida','No hay ninguna partida grabada ahí.\n'),
 ('s_cargada','Partida cargada.\n'),
 ('s_f_abrir','Fallo al abrir'),('s_f_buscar','Fallo al buscar'),('s_f_escribir','Fallo al escribir'),('s_f_cerrar','Fallo al cerrar'),
 ('s_f_fin',' el fichero.\n'),
 ('s_f_cerrar2','Fallo al cerrar el fichero'),('s_f_leer','Fallo al leer el fichero'),
 ('s_f_nodatos1','No hay datos'),('s_f_nodatos2','No hay datos'),
 ('s_memoria','¡No hay memoria suficiente!'),
 ('s_aqui_hay','Aquí hay '),('s_llevas','Llevas '),('s_coma',', '),
 ('k_cmd_grabar','GRABAR'),('k_cmd_guardar','GUARDAR'),('k_cmd_save','SAVE GAME'),
 ('k_cmd_cargar','CARGAR'),('k_cmd_load','LOAD GAME'),
 ('k_f1','BUSCA '),('k_f2','COGE '),('k_f3','EXPLICA '),('k_f4','PREGUNTA FECHA'),('k_f5','LLAMA '),
 ('k_f6','MIRA '),('k_f7','MUESTRA '),('k_f8','PREGUNTA '),('k_f9','GRABAR'),('k_f10','CARGAR'),
]
# nombres largos de los 15 objetos (para las frases); los cortos (≤6) van en CASAB.TBL
LARGOS=['un diario','una carta','una foto','un periódico','una navaja','un manojo de llaves','un libro',
        'un abrigo','unos documentos','la revista TIME','un reloj','unas tenazas','una botella de whisky',
        'un collar','un ramo de flores']

def genera_inc(largos):
    L=[]
    for et,tx in CADENAS:
        b=codifica(tx)+b'\0'
        L.append(et+':\tdb '+','.join('%d'%x for x in b))
    for i,tx in enumerate(largos):
        L.append('nl_%d:\tdb '%i+','.join('%d'%x for x in codifica(tx)+b'\0'))
    L.append('nombres_largos:\tdw '+','.join('nl_%d'%i for i in range(len(largos))))
    L.append('tabla_ordenes:\tdw k_cmd_save,1450h,k_cmd_grabar,1450h,k_cmd_guardar,1450h,k_cmd_load,14D6h,k_cmd_cargar,14D6h,0,0')
    L.append('tabla_rw:\tdw s_leer,s_escribir')
    L.append('tabla_err:\tdw s_e_prot,s_e_nodisco,s_e_crc,s_e_seek,s_e_rnf,s_e_wf,s_e_otro')
    L.append('tabla_fkeys:\tdw k_f1,k_f2,k_f3,k_f4,k_f5,k_f6,k_f7,k_f8,k_f9,k_f10')
    return '\n'.join(L)+'\n'

def ensambla(id_relleno,largos):
    open(os.path.join(SRC,'cadenas.inc'),'w').write(genera_inc(largos))
    open(os.path.join(SRC,'id.inc'),'w').write('ID_RELLENO equ %d\n'%id_relleno)
    src=open(os.path.join(SRC,'ext.asm')).read()
    if 'id.inc' not in src:
        src=src.replace('\torg 9380h','\tinclude "id.inc"\n\torg 9380h'); open(os.path.join(SRC,'ext.asm'),'w').write(src)
    r=subprocess.run(['pasmo','-d','ext.asm','ext.bin','ext.sym'],cwd=SRC,capture_output=True,text=True)
    if r.returncode: print(r.stdout,r.stderr); raise SystemExit('pasmo')
    sym={}
    for l in open(os.path.join(SRC,'ext.sym')):
        p=l.split()
        if len(p)>=3 and p[1]=='EQU': sym[p[0].upper()]=int(p[2].rstrip('H'),16)
    return open(os.path.join(SRC,'ext.bin'),'rb').read(),sym

def parchea(com,id_relleno,largos=LARGOS):
    ext,S=ensambla(id_relleno,largos)
    c=bytearray(com)
    def p(addr,old,new):
        o=addr-0x100
        old=bytes.fromhex(old) if isinstance(old,str) else old
        assert c[o:o+len(old)]==old,('bytes inesperados en %04X: %s'%(addr,c[o:o+len(old)].hex()))
        if isinstance(new,str): new=bytes.fromhex(new)
        assert len(new)<=len(old) or True
        c[o:o+len(new)]=new
    def w16(v): return bytes([v&255,v>>8])
    def ref(addr,old_target,label,op=0x21):
        p(addr,bytes([op])+w16(old_target),bytes([op])+w16(S[label]))
    def ptr(addr,old_target,label):
        p(addr,w16(old_target),w16(S[label]))
    # 1) glifo de medio ancho desde la fuente propia en VRAM 1A000h (sustituye GETPAT)
    p(0x286F,'E1E536',bytes([0xC3])+w16(S['EXT_GLIFO']))
    # 2) puts con corte por palabras
    p(0x258E,'22198E',bytes([0xC3])+w16(S['EXT_PUTS']))
    # 3) salto de línea con pausa
    p(0x2432,'3AC022',bytes([0xC3])+w16(S['EXT_NL']))
    p(0x1F9E,'3E0AC34B24',bytes([0xC3])+w16(S['EXT_FIN_ENTRADA'])+b'\0\0')
    p(0x24B6,'CD5023',bytes([0xCD])+w16(S['EXT_CLS']))
    # 4) entrada en letras de medio ancho, hasta 38 caracteres, búfer nuevo
    p(0x1E2D,'FE20DA531EFE','FE20D8C34B24')  # cp 20h / ret c / jp putc_sjis
    p(0x1E9D,'81400808','20080000'); p(0x1EA2,'81510808','5F080000')
    p(0x1FAE,'080820200808','082008000000')
    p(0x1F76,'FE15','FE26')
    ref(0x08B5,0x5230,'BUF_ENTRADA'); ref(0x08C0,0x5230,'BUF_ENTRADA')
    # 5) palabras de relleno
    p(0x0DDB,'CD320F',bytes([0xCD])+w16(S['EXT_BUSCA']))
    # 5b) minúsculas sin CAPS y Ñ
    p(0x16EB,'CDA525',bytes([0xCD])+w16(S['EXT_CHGET']))
    # 5c) panel derecho separado del dibujo
    p(0x25C9,'E5696022',bytes([0xC3])+w16(S['EXT_X'])+b'\0')
    # 6) listas de objetos
    p(0x0532,'CD8E25',bytes([0xCD])+w16(S['EXT_OBJ_SALA']))
    p(0x056B,'82C620','000000')
    p(0x0559,'080808','2E0A00')
    p(0x05B1,'CD8E25',bytes([0xCD])+w16(S['EXT_OBJ_LLEVA']))
    p(0x0603,'82C620','000000')
    p(0x05ED,'080808','2E0A00')
    t=codifica('No llevas nada.\n')+b'\0'; p(0x05D7,c[0x5D7-0x100:0x5D7-0x100+len(t)],t)
    # 7) palabra desconocida: No conozco la palabra «X».
    p(0x0DEF,'3E27CD4B24',bytes([0xCD])+w16(S['EXT_NO_CONOZCO'])+b'\0\0')
    ref(0x0DFA,0x0E11,'S_NO_CONOZCO2')
    # 8) textos del intérprete
    for a,old,lab in [(0x026C,0x2FF,'S_ERR_DISCO'),(0x0278,0x2FA,'S_ERR_AL'),(0x0292,0x2F1,'S_DOS_PUNTOS'),(0x02A2,0x2E6,'S_FAT'),
                      (0x02BB,0x2C7,'S_PULSA_NL'),(0x03F7,0x4BA,'S_DISCO2'),(0x0404,0x49D,'S_PULSA'),
                      (0x042D,0x486,'S_TITULO1'),(0x043A,0x47F,'S_TITULO2'),(0x0721,0x72E,'S_SWITCH'),
                      (0x08E7,0x8F7,'S_NO_PUEDES'),(0x0C0D,0xCC6,'S_NO_LLEVAS'),(0x0BD9,0xCD9,'S_NO_ESTA'),
                      (0x0B27,0xCF8,'S_PAUSA'),(0x07E1,0x807,'S_QUE_HACES'),(0x13C2,0x143B,'S_NUM_PARTIDA'),
                      (0x1450,0x14A8,'S_GRABANDO'),(0x148F,0x1498,'S_ERR_GRABAR'),(0x14D6,0x157A,'S_CARGANDO'),
                      (0x14F1,0x156A,'S_ERR_CARGAR'),(0x1508,0x1556,'S_SIN_PARTIDA'),(0x1533,0x153C,'S_CARGADA'),
                      (0x1BBC,0x1C7C,'S_F_ABRIR'),(0x1BE3,0x1C6A,'S_F_BUSCAR'),(0x1C0E,0x1C61,'S_F_ESCRIBIR'),
                      (0x1C27,0x1C58,'S_F_CERRAR'),(0x1C41,0x1C4A,'S_F_FIN'),(0x1D0A,0x1D2C,'S_F_CERRAR2'),
                      (0x1CF1,0x1D3B,'S_F_LEER'),(0x1CA4,0x1D4A,'S_F_NODATOS1'),(0x1C8C,0x1D69,'S_F_NODATOS2'),
                      (0x101F,0x124B,'S_MEMORIA'),(0x15E9,0x15AA,'TABLA_ORDENES')]:
        ref(a,old,lab)
    p(0x0287,'115802',bytes([0x11])+w16(S['TABLA_RW']))
    p(0x02B0,'115C02',bytes([0x11])+w16(S['TABLA_ERR']))
    p(0x046F,'11FA01',bytes([0x11])+w16(S['TABLA_FKEYS']))
    p(0x0428,'3E32','3E32'); p(0x0435,'3E38','3E37')
    # 9) mover el montón detrás de la ampliación
    fin=(S['FIN_EXT']+1)&~1
    p(0x4A24,'6293',w16(fin))
    base=0x9380-0x100
    assert len(c)==base
    return bytes(c)+ext, S
