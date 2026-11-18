# Casablanca ni Ai wo (MSX2) – curiosidades

- **Homenaje directo a la película.** El título enseña a Humphrey Bogart e Ingrid Bergman dibujados (PIC101). En el final, la heroína se llama **Ilsa** por Ilsa Lund: «¿Ilsa fue idea tuya?» «¡Claro! ¿Has visto Casablanca? La que ganó el Óscar, con Ingrid Bergman. La vi tres veces».
- **Viajes en el tiempo.** El crimen ocurre en 1945 y se viaja a 1916 en la máquina del doctor Elgar. En la biblioteca hay una novela de **H. G. Wells** y un número de la revista **TIME**. La combinación del dial son fechas: el vocabulario guarda 19160615, 15061945, 19450615… y una lista de combinaciones «trampa» (11111111, 12345678, 98765432…).
- **Se puede jugar en inglés.** El vocabulario acepta sinónimos ingleses (OPEN, KNOCK, LOOK, TAKE, KISS…) y el aviso del intérprete es «What to do?» en inglés. También entiende romaji, que convierte a kana.
- **Fecha imposible.** La firma de la tabla dice `CASAB.ADW Ver1.40 1981/9/7`: un año antes de existir el MSX (probablemente 1987/9/7 mal tecleado). El intérprete se llama a sí mismo «Adventure **interpriter** Ver 1.22».
- **Faltas en el vocabulario:** KRYHOLE (por KEYHOLE), CALENDER, TERR. Y entiende insultos: ﾊﾞｶ ｱﾎ ﾏﾇｹ ﾎﾞｹ ﾎﾞｹﾅｽ (tonto, idiota, bobo…).
- **Discos de dos máquinas.** El disco 1 se formateó en un Sony MSX y el disco 2 en un **NEC PC-98** (sector de arranque «NEC 2.00»): los datos vienen de la versión de PC.
- **Faltan PIC8 y PIC30** en la numeración de los dibujos. PIC24, PIC29 y PIC31 tienen el atributo de archivo apagado, como si se hubieran copiado aparte.
- **Ceros de relleno.** OPEN.COM lleva 26 KB de ceros y RUNADV.COM 16 KB: son las variables del programa en C guardadas dentro del fichero.
- **Mensajes sin usar** en CASAB.MSG: «同じことを何回もしないように！» (¡No hagas lo mismo tantas veces!), «そんなことをすると無くしますよ。» (Si haces eso, lo perderás), «どのように合わせる？» (¿Cómo lo combinas?), «閉まっています。» (Está cerrado) y «手に取ってみたら？» (¿Y si lo coges?). Ninguna regla del guion los cita.
- **Opción oculta.** `runadv casab -d` arranca en modo de depuración (banner «Adventure interpriter Ver 1.22», volcados «Flags %d», «Things %d»). En la prueba, con ella el juego no enseñó los textos de la sala.
- **Fuente propia.** No usa la ROM de kanji del MSX: OPEN.COM sube a la VRAM una fuente de 16×11 con todo el kanji de nivel 1 (2.965 caracteres). Solo los caracteres de un byte salen de la BIOS.
