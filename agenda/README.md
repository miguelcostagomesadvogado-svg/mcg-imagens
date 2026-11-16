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
- `comentario` (opcional, carrosséis e imagens): texto do primeiro comentário, publicado pela própria página logo a seguir à peça, no Instagram e no Facebook. A API não permite fixar comentários: o Dr. Miguel fixa-o à mão quando puder. Se o comentário falhar, a peça fica publicada na mesma e o erro aparece em `erros_comentario` e no `ESTADO.md`.
- `publicar_atrasado` (opcional): `true` para publicar mesmo com mais de 6 h de atraso. Sem isso, uma peça atrasada mais de 6 h vai para `atrasadas/` e não sai.

## Primeiro comentário — OBRIGATÓRIO (pedido do Dr. Miguel, 16 nov. 2026)

Todos os carrosséis e imagens únicas levam o campo `comentario`, escolhido pelo Claude (o Dr. Miguel confia no critério e não quer escolher). Os stories não levam.

- Uma pergunta curta que dê vontade de responder e seja fácil de responder (uma palavra, um ano, um país, sim/não, uma opinião), ligada ao tema da peça. Exemplos aprovados: "Em que país está a ler isto? 🌍 Conte-nos nos comentários." · "Quando foi a última vez que a pensão de alimentos foi atualizada? Responda só com o ano."
- Nunca pedir que contem o seu caso pessoal em pormenor nem dados pessoais.
- Regras da OA: sem convite ao contacto (nada de "ligue", "envie mensagem", "fale connosco"), sem promessas, sem "especialista".
- Português europeu, tom humano, sem vestígios de IA, no máximo 1 emoji, nunca igual à primeira frase da legenda nem repetido de outra peça.

Resultado:
- `publicado/`: peças publicadas, com os ids de cada rede em `feito`.
- `erros/`: peças que falharam 3 vezes (o erro fica no campo `erros`).
- `atrasadas/`: peças que perderam a hora.
- `ESTADO.md`: estado da ligação à Meta e da última execução.
