; Ampliación de RUNADV.COM para la traducción al castellano de "Casablanca ni Ai wo".
; Se añade al final del .COM (9380h) y se mueve el inicio del montón (L4A24) detrás.
; araubi, 2026. Código MIT.

putc_sjis   equ 244Bh
scroll_win  equ 2395h
chget       equ 25A5h
kilbuf      equ 25BDh
cls_win     equ 2350h
busca_voc   equ 0F32h
tokeniza    equ 0D75h
COL         equ 22BBh
FILA        equ 22BCh
FILA_FIN    equ 22BFh
COL_IZQ     equ 22C0h
COL_DER     equ 22C1h
HAY_OBJ     equ 5214h
LLEVA_OBJ   equ 5215h

	include "id.inc"
	org 9380h

; --- puts con corte por palabras -------------------------------------------
ext_puts:
	ld (pp),hl
	xor a
	ld (prev),a
ep_bucle:
	ld hl,(pp)
	ld a,(hl)
	or a
	ret z
	cp 21h
	jr c,ep_nopal
	ld b,a
	ld a,(prev)
	cp 21h
	jr nc,ep_emite          ; dentro de una palabra
	; principio de palabra: medir
	ld c,0
ep_mide:
	ld a,(hl)
	cp 21h
	jr c,ep_fin_mide
	inc c
	inc hl
	jr ep_mide
ep_fin_mide:
	ld a,(COL_IZQ)
	ld e,a
	ld a,(COL)
	cp e
	jr z,ep_emite           ; ya al principio de la línea
	add a,c
	dec a
	ld e,a
	ld a,(COL_DER)
	cp e
	jr nc,ep_emite          ; cabe
	ld a,0Ah
	call putc_sjis
	jr ep_emite
ep_nopal:
	cp 20h
	jr nz,ep_emite
	; espacio: se omite si un salto automático lo ha dejado al principio de línea
	ld a,(prev)
	cp 21h
	jr c,ep_emite
	ld a,(COL_IZQ)
	ld e,a
	ld a,(COL)
	cp e
	jr z,ep_salta
ep_emite:
	ld hl,(pp)
	ld a,(hl)
	ld (prev),a
	call putc_sjis
ep_salta:
	ld hl,(pp)
	inc hl
	ld (pp),hl
	jr ep_bucle

; --- salto de línea con pausa "▼" cuando el texto llenaría la ventana ---------
ext_nl:
	ld a,(COL_IZQ)
	ld (COL),a
	ld a,(FILA)
	ld hl,FILA_FIN
	cp (hl)
	jr nz,en_sin_scroll
	ld a,(nlin)
	cp 5
	call nc,espera_mas
	ld hl,nlin
	inc (hl)
	jp scroll_win
en_sin_scroll:
	ld hl,nlin
	inc (hl)
	ld a,(FILA)
	inc a
	ld (FILA),a
	ret

espera_mas:
	ld a,(COL)
	push af
	ld a,(COL_DER)
	push af
	ld a,0FFh
	ld (COL_DER),a
	ld a,63
	ld (COL),a
	ld a,0B2h
	call putc_sjis
	call kilbuf
	call chget
	ld a,63
	ld (COL),a
	ld a,20h
	call putc_sjis
	pop af
	ld (COL_DER),a
	pop af
	ld (COL),a
	xor a
	ld (nlin),a
	ret

ext_fin_entrada:
	xor a
	ld (nlin),a
	ld a,0Ah
	jp putc_sjis

ext_cls:
	ld a,1
	ld (nlin),a
	jp cls_win

; --- palabras de relleno (artículos, preposiciones) que el analizador ignora ---
ext_busca:
	push hl			; Ñ/ñ (A4h/A5h) -> N para buscar en el vocabulario
eb_n:	ld a,(hl)
	or a
	jr z,eb_fin
	cp 0A4h
	jr z,eb_pon
	cp 0A5h
	jr nz,eb_sig
eb_pon:	ld (hl),'N'
eb_sig:	inc hl
	jr eb_n
eb_fin:	pop hl
	call busca_voc
	ld a,h
	or a
	ret nz
	ld a,l
	cp ID_RELLENO
	ret nz
	pop af
	jp tokeniza

; --- listas de objetos: "Aquí hay un X, una Y." / "Llevas un X." ------------
ext_obj_sala:
	ld a,(HAY_OBJ)
	ld hl,s_aqui_hay
	jr eo_comun
ext_obj_lleva:
	ld a,(LLEVA_OBJ)
	ld hl,s_llevas
eo_comun:
	or a
	jr z,eo_pre
	ld hl,s_coma
eo_pre:
	push bc
	call ext_puts
	pop bc
	ld l,c
	ld h,0
	add hl,hl
	ld de,nombres_largos
	add hl,de
	ld a,(hl)
	inc hl
	ld h,(hl)
	ld l,a
	jp ext_puts

ext_no_conozco:
	ld hl,s_no_conozco
	jp ext_puts

; --- glifo de medio ancho (8x11) desde la fuente propia en VRAM 1A000h -------
; Sustituye a glifo_medio_ancho (GETPAT de la BIOS). Pila: búfer, código, retorno.
vdp_r14     equ 28F1h
lee_vram    equ 292Dh
ext_glifo:
	pop hl
	pop de
	ld (hl),8
	inc hl
	ld (hl),0
	inc hl
	ld (hl),11
	inc hl
	ld (hl),0
	inc hl
	push hl
	ld d,0
	ld h,d
	ld l,e
	add hl,hl
	add hl,hl
	add hl,de
	add hl,hl
	add hl,de
	ld de,2000h
	add hl,de
	ex de,hl
	ld a,6
	call vdp_r14
	pop hl
	ld bc,11
	jp lee_vram

pp:	dw 0
prev:	db 0
nlin:	db 0
buf_entrada:	ds 42

	include "cadenas.inc"
; --- teclado: minúsculas sin CAPS y Ñ (sustituye la llamada a CHGET del conversor romaji) ---
ext_chget:
	call 25A5h		; CHGET del juego
	cp 'a'
	jr c,ec_n
	cp 'z'+1
	jr nc,ec_n
	sub 20h			; minúscula -> mayúscula (no pasa a kana)
	ret
ec_n:	cp ';'			; en el teclado japonés no hay Ñ: ; hace de Ñ
	jr z,ec_enye
	cp 0A4h			; ñ de un teclado español/europeo -> Ñ
	ret nz
ec_enye: ld a,0A5h
	ret

fin_ext:

