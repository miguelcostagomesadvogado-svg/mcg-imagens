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
- `legenda`: vazia nos stories. **No máximo 5 hashtags** (limite do Instagram): sempre #Portugal #DefendaOsSeusDireitos e mais 3 do tema, com acentos corretos, sem localidades nem países. O publicador corta automaticamente o que passar de 5, mas a legenda deve já vir certa.
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

## Carrosséis em formato de história (decidido pelo Dr. Miguel, 18 nov. 2026)

Os carrosséis passam a ser um misto: **histórias** e **informativos diretos** (como até aqui), em alternância — cerca de 3 histórias por cada 2 informativos, para não cansar e continuar a aparecer nas pesquisas por temas concretos. Primeiro exemplo: `2026-11-18-1900-carrossel-historia-sofia.json`.

Estrutura da história (6 diapositivos):
1. Capa com gancho e a protagonista na foto (etiqueta "UMA HISTÓRIA · <ÁREA>", "A história da <Nome>." + DESLIZE).
2. O conflito (o que aconteceu).
3. O que ela/ele pensou (o erro comum).
4. e 5. A viragem: o direito, em linguagem simples, com artigo confirmado no texto da lei (na dúvida, não citar).
6. Fecho com contactos, "Guarde e partilhe" e a linha "Caso ilustrativo, com nome fictício."

Regras:
- Nomes fictícios e comuns; nunca nomes de clientes atuais; nunca apresentar como caso real do escritório.
- Nunca terminar com uma vitória do advogado ("ganhámos"); a história acaba no direito que a pessoa tinha.
- A mesma modelo em todas as fotos da história (é a protagonista); idade, género e cenário coerentes com o texto (ex.: modelo jovem → poucos anos de casa).
- Legenda conta a história em resumo, cita os artigos e leva "Caso ilustrativo, com nome fictício." antes da nota informativa.
