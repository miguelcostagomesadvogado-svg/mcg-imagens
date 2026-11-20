# Série de Reels «Como trabalho» (20 nov. 2026)

Alguém pesquisa no telemóvel «advogado para <área>», toca no resultado MCG Advogado e o vídeo mostra,
passo a passo, o que acontece depois do contacto. 17,8 s, 1080x1920, 30 fps, sem som.

- Gerador: `gen.py` (Pillow + ffmpeg). `python3 gen.py series.json <pasta-saida> [slug]`
- Uma entrada por área em `series.json`: slug, area, pesquisa, resultado, documentos, foto, foco_y, barra_y (opcional:
  250 quando a cara da modelo está baixa na foto e a caixa de pesquisa a tapava; por omissão 880).
- Cenas (17,8 s): 0–4 s pesquisa (cartão ao estilo da ficha Google com a foto de perfil; toque em WhatsApp);
  4–8,1 s «A primeira resposta · no WhatsApp» e 8,1–12,2 s «· no Direct do Instagram»: a mensagem da cliente
  (campo `mensagem`) e a resposta COMPLETA da marca, como o Dr. Miguel a envia (cartão MCG no WhatsApp; cartão do
  perfil mcg.advogado no Direct; nome, cédula, MCG Advogado, telefone, e-mail, Instagram e Facebook — sem a morada,
  que não entra nas redes); linhas a aparecer devagar para as pessoas reconhecerem a marca; 12,2–17,8 s os 6 passos,
  o lema e a pílula «Saiba mais na legenda» (o fecho com a foto saiu para caber nos 18 s).
- 20 nov. 2026: o Dr. Miguel NÃO quer o resultado a remeter para o site (ainda não está online); remeter
  para a ficha Google, o Instagram ou o Facebook (facebook.com/advogados.portugal.mcg.miguelcostagomes).
- Vídeos: `../../reels/como-trabalho/`. Legendas e primeiros comentários: `legendas.md` / `legendas.json`.
- A barra de pesquisa é genérica de propósito: sem logótipo nem nome do Google (marcas de terceiros
  e regras de anúncios da Meta).
