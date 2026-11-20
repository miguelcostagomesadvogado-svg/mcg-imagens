# Série de Reels «Como trabalho» (20 nov. 2026)

Alguém pesquisa no telemóvel «advogado para <área>», toca no resultado MCG Advogado e o vídeo mostra,
passo a passo, o que acontece depois do contacto. 17,8 s, 1080x1920, 30 fps, sem som.

- Gerador: `gen.py` (Pillow + ffmpeg). `python3 gen.py series.json <pasta-saida> [slug]`
- Uma entrada por área em `series.json`: slug, area, pesquisa, resultado, documentos, foto, foco_y, barra_y (opcional:
  250 quando a cara da modelo está baixa na foto e a caixa de pesquisa a tapava; por omissão 880).
- Cenas: 0–4,4 s pesquisa (foto da modelo + barra genérica + cartão ao estilo da ficha Google
  «MCG Advogados - Miguel Costa Gomes» com a fotografia de perfil do Instagram/ficha, botões Ligar · WhatsApp ·
  Instagram · Facebook e toque em WhatsApp); 4,4–7,6 s «A primeira resposta» (mensagem da cliente, campo
  `mensagem` do series.json, e a resposta com o cartão da marca `cartao-resposta.png`, sem a morada, e os
  contactos, como o Dr. Miguel responde no WhatsApp e no Direct); 7,6–15,4 s «O que acontece a seguir»
  (6 passos, 1,2 s cada); 15,4–17,8 s fecho com a foto do Dr. Miguel em navy, lema e pílula.
- 20 nov. 2026: o Dr. Miguel NÃO quer o resultado a remeter para o site (ainda não está online); remeter
  para a ficha Google, o Instagram ou o Facebook (facebook.com/advogados.portugal.mcg.miguelcostagomes).
- Vídeos: `../../reels/como-trabalho/`. Legendas e primeiros comentários: `legendas.md` / `legendas.json`.
- A barra de pesquisa é genérica de propósito: sem logótipo nem nome do Google (marcas de terceiros
  e regras de anúncios da Meta).
