#!/bin/bash
# Uso: render.sh VIDEO "TEXTO DO GANCHO" N_PALAVRAS_DOURADAS TAMANHO(54|57|60) ENTRELINHA(74|76) SAIDA.mp4 [DURACAO_MAX=23]
# Antes, testar o gancho: python3 mkhook.py "texto" N TAM ENTRE /tmp/t.png  -> tem de dar 3 linhas, gaps <= ~45, fundo <= 1308
set -e
K="$(cd "$(dirname "$0")" && pwd)"
SRC="$1"; TXT="$2"; NG="$3"; SZ="$4"; LH="$5"; OUT="$6"; T="${7:-23}"
python3 "$K/mkhook.py" "$TXT" "$NG" "$SZ" "$LH" /tmp/ov.png
ffmpeg -y -v error -t "$T" -i "$SRC" -loop 1 -i /tmp/ov.png -loop 1 -i "$K/cta2.png" -loop 1 -i "$K/arrow2.png" -loop 1 -i "$K/som10.png" -filter_complex "[0:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[b];[2:v]format=rgba,fade=in:st=2.4:d=0.35:alpha=1[c];[3:v]format=rgba,fade=in:st=2.4:d=0.35:alpha=1[ar];[4:v]format=rgba,fade=in:st=0.2:d=0.3:alpha=1[s];[b][1:v]overlay=0:0:shortest=1[v1];[v1][c]overlay=0:0:shortest=1[v2];[v2][ar]overlay=x=522:y='1328+8*abs(sin(t*5))':shortest=1[v3];[v3][s]overlay=0:0:shortest=1,format=yuv420p[v]" -map "[v]" -an -c:v libx264 -preset veryfast -crf 20 -r 30 -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
echo "erros: $(ffmpeg -v error -i "$OUT" -f null - 2>&1 | wc -l)"
