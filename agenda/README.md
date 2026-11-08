# Agenda de publicações

Cada peça é um ficheiro `AAAA-MM-DD-HHMM-<slug>.json` nesta pasta. A GitHub Action
"Publicar nas redes" corre de 15 em 15 minutos e publica as peças com
`"aprovado": true` cuja hora já chegou.

```json
{
  "quando": "2026-11-09T12:30",
  "redes": ["instagram", "facebook"],
  "tipo": "carrossel",
  "imagens": ["2026-11-09/1230-carrossel-1.jpg", "2026-11-09/1230-carrossel-2.jpg"],
  "legenda": "Texto completo, com bloco de contactos e hashtags.",
  "aprovado": false
}
```

- `quando`: hora de Lisboa (AAAA-MM-DDTHH:MM).
- `redes`: `instagram`, `facebook` ou ambas.
- `tipo`: `carrossel` (2 a 20 imagens 1080x1350), `imagem` (1 imagem), `story` (1 ou mais imagens 1080x1920, cada uma publicada como story), `texto` (só Facebook, sem imagens).
- `imagens`: caminhos no repositório, pela ordem, sempre JPEG.
- `legenda`: vazia nos stories.
- `aprovado`: só passa a `true` depois do "sim" do Dr. Miguel.
- `publicar_atrasado` (opcional): `true` para publicar mesmo com mais de 6 h de atraso. Sem isso, uma peça atrasada mais de 6 h vai para `atrasadas/` e não sai.

Resultado:
- `publicado/`: peças publicadas, com os ids de cada rede em `feito`.
- `erros/`: peças que falharam 3 vezes (o erro fica no campo `erros`).
- `atrasadas/`: peças que perderam a hora.
- `ESTADO.md`: estado da ligação à Meta e da última execução.
