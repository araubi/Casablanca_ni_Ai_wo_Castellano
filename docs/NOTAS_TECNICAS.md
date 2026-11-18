# Casablanca ni Ai wo (MSX2) – notas técnicas para la traducción

カサブランカに愛を ―殺人者は時空を越えて― (Thinking Rabbit, MSX2, 1988). Aventura de texto con analizador
(se escriben órdenes) y dibujos. Estudio hecho el 3-11-2026 en openMSX 19.1 con las ROM del Sony HB-F900.

## 1. Versiones conocidas

| Fichero | Tamaño | SHA1 |
|---|---|---|
| `Casablanca (1988)(Thinking Rabbit)(JP)(Disk 1 of 2).dsk` | 720 KB | 073e5fa25bbf9bf89e6f3f59bde7d86b826b2d97 |
| `Casablanca (1988)(Thinking Rabbit)(JP)(Disk 2 of 2).dsk` | 720 KB | f99fb8c72065ae9128067b10d394599f0e729a50 |
| `Casablanca (1988)(Thinking Rabbit)(JP).dsk` | 1440 KB | 1c92bd0059c18ebb6e2d0e9214ba52e0a925a6dc |

- La imagen única de 1440 KB es **exactamente** los dos discos pegados uno detrás del otro (comprobado byte a byte). No hay otra versión.
- No hay versión MSX1, ni en cinta, ni traducción, ni parches conocidos (a fecha de noviembre de 2026).
- El disco 1 se formateó en un Sony (sector de arranque `SNYJX205`); el disco 2 en un **NEC PC-98** (`NEC 2.00`), señal de que los datos vienen de la versión de PC.

## 2. Arranque y ficheros

Disco 1 (arranca MSX-DOS 1.03): `AUTOEXEC.BAT` = `open` + `runadv casab`.

| Fichero | Tamaño | Qué es |
|---|---|---|
| MSXDOS.SYS, COMMAND.COM | | MSX-DOS 1 |
| OPEN.COM | 35.584 | Presentación: carga KANJI.FNT en VRAM 8000h y enseña PIC101/PIC100 (título con Bogart y Bergman). 26 KB finales son ceros. |
| RUNADV.COM | 37.504 | Intérprete («Adventure interpriter Ver 1.22»), C compilado + rutinas en ensamblador. Pide el disco 2. 16 KB finales son ceros. |
| PIC100.MSX, PIC101.MSX | | Pantallas del título |
| KANJI.FNT | 72.358 | Fuente propia: 3.289 glifos de 16×11 (22 bytes cada uno) |

Disco 2 (87 KB libres; el disco 1 tiene 548 KB libres):

| Fichero | Tamaño | Qué es |
|---|---|---|
| CASAB.TBL | 4.603 | Tabla de salas, estado inicial, inventario y vocabulario |
| CASAB.INT | 25.700 | Guion (código de reglas por sala) |
| CASAB.MSG | 42.316 | Todos los mensajes (Shift-JIS) |
| PIC1…PIC72.MSX | | 70 dibujos (faltan PIC8 y PIC30); formato comprimido propio, cabecera `64 93` |
| ADVTMP.DAT | 2.560 | Partidas guardadas (10 huecos, «データ番号は？(0-9)») |

## 3. Pantalla y texto

- **SCREEN 6** (512×212, 4 colores). Dibujo arriba a la izquierda, título y objetos llevados a la derecha, ventana de texto debajo con desplazamiento.
- Línea de texto: **60 columnas de 8 px** (30 caracteres de ancho completo). 285 líneas del original miden exactamente 60.
- El intérprete corta solo al llegar al margen (por carácter, sin respetar palabras). El original pone saltos `0Ah` a mano.
- Paginación: la acción `84h` del guion escribe «どれかキーを押して下さい。», espera tecla y borra la ventana.

### Rutina de escritura (RUNADV, `putc_sjis` 244Bh)
- Controles: 0Dh, 0Ah, 08h/7Fh (borrar), 0Ch (limpiar ventana).
- **Doble byte (Shift-JIS)**: `sjis_a_jis` (28C9h) → `busca_glifo` (26E4h) calcula la dirección en VRAM del glifo de KANJI.FNT, lo lee (22 bytes), lo pasa a 2 bpp (`expande_1bpp_2bpp`, 25EAh) y lo copia con BLTVM (SUB-ROM 0195h). Celda de 16×11.
- **Un byte** (ASCII, kana de medio ancho): pide el patrón 8×8 a la **BIOS** (SUB-ROM GETPAT 0105h) y lo pinta en celda de 8×11. Así sale «What to do?».

### KANJI.FNT (en VRAM 8000h–19AA5h)
Glifo = 11 filas × 16 bits (22 bytes). Bases por rango JIS (en `busca_glifo`):

| JIS | Contenido | Dirección VRAM |
|---|---|---|
| 2121h… | símbolos | 8000h |
| 2330h… | cifras ０-９ | 8814h |
| 2340h… | mayúsculas Ａ-Ｚ | 88F0h |
| 2360h… | minúsculas ａ-ｚ | 8B42h |
| 2421h… | hiragana | 8D94h |
| 2521h… | katakana | 94B6h |
| 3021h… | kanji nivel 1 completo (2.965) | 9BD8h |

Hoja en `imagenes/fuente_simbolos_kana.png`. **No hay letras acentuadas, ñ, ¿ ni ¡** (JIS X 0208 no las tiene). La VRAM **1A000h–1FFFFh (24 KB) está libre**: caben ~1.100 glifos más.

## 4. Formatos de datos

### CASAB.MSG
- Cadenas Shift-JIS terminadas en 00h, con 0Ah para saltar de línea. 803 mensajes, 20.292 caracteres de doble byte.
- El guion las cita por **desplazamiento de 16 bits sin signo** (acción `90h lo hi`): el fichero puede llegar a **64 KB** (ahora 42 KB, 66 mensajes ya están por encima de 8000h y funcionan).
- `getmsg` (133Dh) lee **512 bytes** al búfer 53B3h: cada mensaje, con su 00h, tiene que caber en 512 bytes (el más largo del original tiene 244).
- 5 mensajes no se usan (ver CURIOSIDADES).

### CASAB.TBL
- 000h–3FFh: 256 × (desplazamiento, longitud) de 16 bits del trozo de CASAB.INT de cada sala.
- 400h: posición inicial de cada objeto (00h = lo llevas; C8h, que es 200, parece «fuera del juego»). Empiezas con el diario y el collar.
- 496h: nombres de los 15 objetos del inventario (SJIS, terminados en 00h, lista acabada en FFh).
- 4E6h: firma `*カサブランカに愛を  CASAB.ADW  Ver1.40 1981/9/7*`.
- Vocabulario: 46 verbos y 127 nombres; cada entrada son **sinónimos separados por espacios** (katakana de medio ancho, romaji e **inglés**: `ｱｹﾙ OPEN ﾋﾗｸ`). Volcado en `textos/CASAB_TBL_vocabulario.txt`.

### CASAB.INT (guion)
Por cada regla: condiciones (dos listas acabadas en FFh; bytes <F0h ocupan 2, ≥F0h 1) y acciones hasta FFh.

| Acción | Bytes | Efecto (deducido del intérprete) |
|---|---|---|
| 80h | +3 | compuesta (subcódigos 10h/20h: objetos y salas) |
| 81h n | +1 | ir a la sala n (FFh = no) |
| 82h / 83h | 0 | recordar sala / volver a ella |
| 84h | 0 | «pulsa una tecla» y borrar ventana |
| 89h | 0 | fin de la acción |
| 90h lo hi | +2 | escribir mensaje de CASAB.MSG |
| 91h p e | +2 | dibujar PICp.MSX |
| 92h n | +1 | variable 04D5h = n |
| 93h, 95h | +1, +2 | el ejecutor de acciones no los trata (quizá se usan en otra fase) |
| 94h | 0 | lista de objetos de la sala («が あります») |
| 96h n / 97h n | +1 | contador n −1 / +1 |
| 98h n | +1 | coger el objeto n (si no está: «そんなものはここにはないので、») |
| 99h n | +1 | dejar el objeto n (si no lo llevas: «持っていないので、») |

## 5. Textos dentro de RUNADV.COM (hay que traducirlos aparte)
«What to do? » (inglés), «カサブランカ／に愛を» (título de la derecha), «ディスク２に入れ替えて、どれかキーを押してください。», errores de disco (ＦＡＴ不良, シークエラー…), inventario («が あります。», «を 持っています。», «何も持っていません。»), «そのようなことはできません。», «'ということばはつかえません。», «持っていないので、», «そんなものはここにはないので、», menú de partidas (ｾｰﾌﾞ ｹﾞｰﾑ / ﾛｰﾄﾞ ｹﾞｰﾑ, «データ番号は？(0-9)», «ゲーム進行状況を ディスケットに 書き込みます»…), «メモリー ガ タラン!!». Unos 35 textos; varios son **trozos que se pegan al nombre de un objeto o a la palabra tecleada** (orden japonés: «X を 持っています»), así que hay que tocar el código que los compone, no solo el texto.

## 6. Entrada del jugador
- Se teclea en mayúsculas; el eco sale en letras de ancho completo (ＬＯＯＫ).
- El analizador convierte **romaji a kana** (tablas 1647h) y acepta las palabras inglesas del vocabulario.
- Opciones de RUNADV tras «-»: D (depuración), J/K/A (modo de entrada), C (borrar pantalla).

## 7. Desensamblado
`desensamblado/runadv.asm` y `open.asm`: recorrido del código desde 0100h más semillas revisadas a mano; lo no alcanzado queda como `db` con el texto SJIS en comentario. **Montan idénticos** con `pasmo --bin` (comprobado aquí); la sintaxis es la común con sjasmplus (falta probarlo en el PC). Nombres y comentarios en las rutinas clave (arranque, opciones, guion, getmsg, escritura SJIS, fuente, VDP, BIOS). `herramientas/genfinal.py` los regenera.
