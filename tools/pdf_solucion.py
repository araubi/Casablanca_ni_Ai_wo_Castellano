#!/usr/bin/env python3
# Genera Casablanca_ES_solucion.pdf (guía de solución de la traducción española). MIT.
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sys,os
F='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('S',F+'DejaVuSans.ttf')); pdfmetrics.registerFont(TTFont('SB',F+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('M',F+'DejaVuSansMono.ttf'))
pdfmetrics.registerFontFamily('S',normal='S',bold='SB')
ACC=colors.HexColor('#7a2e2e')
st=dict(
 t=ParagraphStyle('t',fontName='SB',fontSize=22,leading=28,textColor=ACC,spaceAfter=4),
 st=ParagraphStyle('st',fontName='S',fontSize=11,leading=15,textColor=colors.HexColor('#555555'),spaceAfter=10),
 h1=ParagraphStyle('h1',fontName='SB',fontSize=15,leading=20,textColor=ACC,spaceBefore=12,spaceAfter=6),
 h2=ParagraphStyle('h2',fontName='SB',fontSize=11.5,leading=15,spaceBefore=8,spaceAfter=3),
 p=ParagraphStyle('p',fontName='S',fontSize=9.5,leading=13.5,spaceAfter=4),
 c=ParagraphStyle('c',fontName='M',fontSize=9,leading=12),
 n=ParagraphStyle('n',fontName='S',fontSize=8.8,leading=12,textColor=colors.HexColor('#333333')),
)
def P(x,s='p'): return Paragraph(x,st[s])
def pasos(filas):
    """filas: lista de (orden, nota)"""
    data=[[P('<b>Orden</b>','n'),P('<b>Qué pasa</b>','n')]]
    for o,nota in filas: data.append([Paragraph(o,st['c']),P(nota,'n')])
    t=Table(data,colWidths=[62*mm,108*mm],repeatRows=1)
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#efe6e0')),
        ('LINEBELOW',(0,0),(-1,-1),0.25,colors.HexColor('#cccccc')),('TOPPADDING',(0,0),(-1,-1),2.5),('BOTTOMPADDING',(0,0),(-1,-1),2.5)]))
    return t
E=[]
E.append(P('A Casablanca, con amor','t'))
E.append(P('<i>Casablanca ni Ai wo</i> (Thinking Rabbit, 1988, MSX2) · Guía de la traducción al castellano · araubi · versión 1.0','st'))
tit=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'docs','titulo.png')
if os.path.exists(tit): E.append(Image(tit,width=120*mm,height=90*mm)); E.append(Spacer(1,4))
E.append(P('Esta guía lleva la partida de principio a fin con las órdenes de la traducción. Se ha jugado entera en openMSX '
 '(Sony HB-F900) con los discos traducidos, en este mismo orden. '
 'Las órdenes se pueden escribir en mayúsculas o minúsculas y van sin tildes; la Ñ es opcional (ENSEÑA = ENSENA). Valen también otros sinónimos (COGE/TOMA, MIRA/EXAMINA, O/OESTE…).'))
E.append(P('Antes de empezar','h1'))
for x in [
 'Juegas como Roy, periodista del <i>Daily Casablanca</i>, junto a Jerry. Jerry ha recibido el diario de su amiga May Elgar, que ha desaparecido; el padre de May, el doctor Elgar, investigaba cómo controlar el tiempo.',
 'Cuando la ventana se llena aparece ▼ abajo a la derecha, y en las escenas largas sale «(Pulsa una tecla)»: pulsa cualquier tecla para seguir.',
 'Graba a menudo con GRABAR (o GUARDAR) y recupera con CARGAR.',
 '<b>Formas de morir:</b> intentar MATAR a alguien, o encender la máquina del tiempo con el contador mal puesto. Si Reynolds no ha bebido, ni siquiera te deja entrar en la máquina.',
 '<b>Objetos que no hay que regalar:</b> el reloj, el ramo, la navaja y las cartas se pierden si se los das a quien no toca (John Rockhops, Jack, Tom en 1916, Marsha…). La guía solo los entrega donde hace falta.',
 ]: E.append(P('• '+x))

E.append(P('1. Año 1945 · El laboratorio del doctor Elgar','h1'))
E.append(P('15 de junio de 1945. Empiezas delante del laboratorio con el diario de May y un collar.'))
secc=[
('Delante de la puerta',[('LLAMA A LA PUERTA','Abre Reynolds, el ayudante del doctor.'),('DI MI NOMBRE','«¿Es usted amigo de la señorita?»'),
  ('ENSENA EL DIARIO','Se entera de que May ha desaparecido y os deja pasar.'),('ENTRA','Estás en el salón. Hoy no deja pasar a nadie más allá…'),('SAL','Vuelves a la puerta.')]),
('Mirar por la ventana',[('O','Al oeste del laboratorio.'),('N','Junto a la ventana del laboratorio.'),('MIRA POR LA VENTANA','¡El doctor está muerto en el suelo! Hay que avisar a Reynolds.'),('S',''),('E','Otra vez en la puerta.')]),
('Dar la noticia',[('LLAMA A LA PUERTA',''),('ENTRA','En el salón.'),('DI EL CASO','Reynolds se horroriza y ya os deja ir por toda la casa.')]),
('Habitación del doctor',[('N',''),('ABRE LA ESTANTERIA',''),('COGE LA NOVELA','Una novela de ciencia ficción de H. G. Wells.'),('COGE LA REVISTA','Un número de la revista TIME.'),
  ('LEE LA NOVELA','Entre las páginas hay una carta en alemán dirigida al doctor.'),('S','')]),
('Habitación de May',[('SUBE',''),('ABRE EL CAJON',''),('COGE LA FOTO','Foto de May (MIRA LA FOTO la enseña en pantalla).'),('BAJA','')]),
('El laboratorio',[('O','El doctor, con una navaja clavada.'),('MIRA EL CADAVER',''),('COGE LA NAVAJA',''),('REGISTRA EL CADAVER','En el bolsillo hay un manojo de llaves.'),('COGE LAS LLAVES','')]),
('Jardín trasero y colina',[('N','Al salir se llevan el cadáver al hospital.'),('ABRE LA CAJA','La caja de herramientas.'),('COGE LAS TENAZAS',''),('S','Dejas de mirar la caja (con ella delante no puedes subir).'),
  ('N','Cima de la colina, junto al estanque.'),('MIRA ALREDEDOR','Hay un periódico hecho una bola.'),('COGE EL PERIODICO','Un periódico viejísimo.'),('S',''),('S','De vuelta en el laboratorio.')]),
('La casa abandonada',[('E',''),('S','Sales de la casa.'),('E','Al otro lado del camino.'),('N',''),('E','Delante de la casa abandonada, con la puerta clavada.'),
  ('USA LAS TENAZAS','Arrancas los clavos.'),('E','Dentro, a oscuras.'),('COGE EL WHISKY','Una botella cubierta de polvo.'),('O',''),('O',''),('S',''),('O','Otra vez delante del laboratorio.')]),
('La anciana y el florista',[('O',''),('N',''),('O','Delante de una casa elegante.'),('LLAMA A LA PUERTA','«Adelante».'),('ABRE LA PUERTA',''),('O','Una anciana en silla de ruedas.'),
  ('ENSENA EL COLLAR','Le gusta mucho y te regala un reloj de bolsillo.'),('E',''),('E',''),('S',''),('S','La floristería.'),
  ('DA EL RELOJ','El florista te regala un ramo de flores.'),('DA EL RAMO','Te devuelve el reloj… ¡y te quedas también el ramo! Hacen falta los dos.'),('N',''),('E','Delante del laboratorio.')]),
('La máquina del tiempo',[('LLAMA A LA PUERTA',''),('ENTRA',''),('O','El laboratorio.'),('DA EL WHISKY','«No bebo.»'),('DA EL WHISKY','«He dejado la bebida…»'),
  ('DA EL WHISKY','«Bueno, un poquito.» Se queda bebiendo y ya no te vigila.'),('MIRA LA MAQUINA','Ves el dial de cerca.'),('GIRA EL DIAL','Pide un número de ocho cifras.'),
  ('19160615','Año, mes y día: 15 de junio de 1916.'),('ENTRA EN LA MAQUINA',''),('ENCIENDE EL INTERRUPTOR','La máquina vibra… y salís despedidos sobre la hierba.')]),
]
def bloque(secc):
    for t,f in secc: E.append(KeepTogether([P(t,'h2'),pasos(f)]))
bloque(secc)
E.append(P('2. Año 1916 · El pueblo','h1'))
E.append(P('Estás en un prado al pie de la colina, treinta años antes. El doctor Elgar es joven y vive aquí.'))
bloque([
('Hasta casa de Kenny',[('O',''),('S',''),('S',''),('E','Casa de Jeff (no hace falta hablar con él).'),('E','Cruce.'),('N',''),('E','Delante de la casa de Kenny Nichols.')]),
('Kenny, el periodista',[('LLAMA A LA PUERTA',''),('DI MI NOMBRE',''),('ENSENA EL PERIODICO','«¿Son lectores? Pasen.»'),('E','Su casa está llena de periódicos.'),
  ('ENSENA EL PERIODICO','Te cuenta dónde vive el doctor Elgar.'),('ENSENA LA REVISTA','Le asombra la revista TIME «del futuro».'),('DA LA REVISTA','La guarda como un tesoro y os deja pasar a la colina por detrás.'),('N','')]),
('La casita de la cima (el abrigo)',[('N',''),('N','Delante de la casita del doctor.'),('USA LAS LLAVES','Una de las llaves viejas del manojo abre la puerta.'),('ABRE LA PUERTA',''),('ENTRA','El salón.'),
  ('N','El estudio.'),('ABRE EL ARMARIO',''),('MIRA LA ROPA','Al fondo hay un abrigo hecho una bola.'),('COGE EL ABRIGO','Está empapado de sangre.'),
  ('S',''),('S',''),('S',''),('S',''),('LLAMA A LA PUERTA','Kenny os deja pasar por su casa.'),('O',''),('O',''),('S','Cruce.'),('S','Delante de la casa de Marsha Evans.')]),
('Marsha y el doctor Elgar',[('LLAMA A LA PUERTA','No hay respuesta.'),('LLAMA A LA PUERTA','Nadie contesta.'),('LLAMA A LA PUERTA','A la tercera abre Marsha.'),('DI MI NOMBRE',''),
  ('ENSENA EL ABRIGO','Reconoce el abrigo de Elgar: él está dentro.'),('ENTRA','La sala de visitas, con el joven doctor Elgar.'),
  ('ENSENA EL DIARIO','«¡Así que era eso!»'),('ENSENA LA CARTA','La carta es suya, escrita treinta años después. Al leerla os cuenta toda la verdad del crimen.'),
  ('ENSENA LA NAVAJA','Os da los documentos de su investigación.'),('DA LA CARTA','Os da la llave de su laboratorio y os dice el número para volver.'),('N','Al salir, Marsha cierra otra vez.'),('LLAMA A LA PUERTA',''),('LLAMA A LA PUERTA',''),('LLAMA A LA PUERTA','«¿Son ustedes? Adelante.»'),
  ('ENTRA',''),('N','Marsha os devuelve la carta: no hay que abrirla hasta el final.')]),
('Volver a la máquina',[('N',''),('N',''),('E',''),('LLAMA A LA PUERTA',''),('E','Kenny os propone montar un periódico juntos: así nace el Daily Casablanca.'),('N',''),('N',''),('N',''),
  ('ABRE LA PUERTA',''),('ENTRA',''),('USA LAS LLAVES','Abres el laboratorio.'),('O','Aquí está la máquina que construyó el joven Elgar.'),('MIRA LA MAQUINA',''),('GIRA EL DIAL',''),
  ('15061945','El número que os dio Elgar (aquí va día, mes y año).'),('ENTRA EN LA MAQUINA',''),('ENCIENDE EL INTERRUPTOR','Algo sale mal: un ruido tremendo, mucho calor…')]),
])
E.append(P('3. Año 1885 · El final','h1'))
E.append(P('Despiertas en una cama. La máquina os ha llevado demasiado atrás y has perdido los documentos.'))
bloque([
('En casa de Liza',[('O','Liza Nichols os cuidó tras el accidente.'),('MIRA EL CALENDARIO','15 de junio de 1885.'),('PREGUNTA SU NOMBRE',''),('PREGUNTA POR EL NINO','Su hijo, que nacerá el año que viene, es Kenny.'),
  ('DA EL RAMO','Mientras ella mira las flores, podéis salir. (Sin el ramo no os deja marchar.)'),('O','')]),
('Los documentos',[('O',''),('N','Cerca de la cima, donde salisteis despedidos.'),('MIRA ALREDEDOR','Ahí están los documentos.'),('COGE LOS DOCUMENTOS',''),('S',''),('S','')]),
('La casa blanca',[('O',''),('O',''),('N',''),('O','Con el reloj y los documentos aparece una casa conocida: la casa elegante de 1945.'),('O',''),('ABRE LA PUERTA',''),
  ('ENTRA','Os recibe una mujer que se alegra de veros…'),('O','La habitación del fondo, con otra máquina.'),('E','Ella os lo explica todo. Pulsa una tecla en cada página.'),
  ('LEE LA CARTA','Ahora sí: la carta de Marsha (opcional, pero merece la pena).'),('E','Volvéis a 1945. Final, créditos y epílogo.')]),
])
doc=SimpleDocTemplate(sys.argv[1],pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=18*mm,bottomMargin=18*mm,
  title='Casablanca ni Ai wo - Solución (traducción ES)',author='araubi')
def pie(c,d):
    c.setFont('S',8); c.setFillColor(colors.grey); c.drawRightString(190*mm,10*mm,'A Casablanca, con amor · solución · %d'%d.page)
doc.build(E,onFirstPage=pie,onLaterPages=pie)
