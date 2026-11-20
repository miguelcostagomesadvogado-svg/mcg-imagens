# Série de Reels «Como trabalho» (20 nov. 2026)

Alguém pesquisa no telemóvel «advogado para <área>», toca no resultado MCG Advogado e o vídeo mostra,
passo a passo, o que acontece depois do contacto. 17 s, 1080x1920, 30 fps, sem som.

- Gerador: `gen.py` (Pillow + ffmpeg). `python3 gen.py series.json <pasta-saida> [slug]`
- Uma entrada por área em `series.json`: slug, area, pesquisa, resultado, documentos, foto, foco_y, barra_y (opcional:
  250 quando a cara da modelo está baixa na foto e a caixa de pesquisa a tapava; por omissão 880).
- Cenas: 0–5 s pesquisa (foto da modelo + barra genérica sem logótipos + resultado + toque); 5–14,6 s
  «O que acontece a seguir» (6 passos, 1,45 s cada); 14,6–17 s fecho com a foto do Dr. Miguel em navy,
  lema e pílula «Saiba mais na legenda».
- Vídeos: `../../reels/como-trabalho/`. Legendas e primeiros comentários: `legendas.md` / `legendas.json`.
- A barra de pesquisa é genérica de propósito: sem logótipo nem nome do Google (marcas de terceiros
  e regras de anúncios da Meta).
