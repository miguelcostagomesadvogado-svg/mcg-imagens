# Fotografias já usadas — NÃO REPETIR

Regra do Dr. Miguel (9 nov. 2026): **nunca repetir fotografias em publicações novas**.

Todas as fotografias do Unsplash já descarregadas estão registadas em `fetch/*.txt`
(uma linha `nome.jpg URL` por foto). Antes de usar uma fotografia nova:

1. Tira o identificador da imagem do URL devolvido pelo `download_asset`
   (ex.: `photo-1758876201660-103984519266`).
2. `grep -l "<identificador>" fetch/*.txt` — se aparecer, essa fotografia JÁ FOI USADA: escolhe outra.
3. Não reutilizar ficheiros que já estão em `fotos/` em peças novas
   (exceção: `fotos/miguel-cover.jpg`, a fotografia do próprio Dr. Miguel no diapositivo final).

Evitar também repetir o mesmo modelo (a mesma pessoa) em fotografias diferentes da mesma série
de fotógrafo. Privilegiar senhoras atraentes, com ar profissional, sempre coerentes com o tema.

- 2026-11-12: heranca-mulher-documento.jpg (capa carrossel), heranca-idosa-retrato.jpg (story 08h30), heranca-mesa-papeis.jpg (story 21h), abandono-sofa-telefone.jpg (imagem 18h)
- 2026-11-13: online-mulher-blazer-cartao.jpg (capa carrossel), online-mulher-cama-cartao.jpg (story 08h30), online-mulher-recebe-encomenda.jpg (story 21h), irs-mulher-contas.jpg (imagem 18h)
- 2026-11-14: queixa-mulher-estrada-noite.jpg (capa carrossel), queixa-policia-carro.jpg (story 08h30), queixa-mulher-noite-rua.jpg (story 21h), viacao-carros-colisao.jpg (imagem 18h)
- 2026-11-15: dividas-casal-sofa.jpg (capa carrossel), dividas-mulher-maos-cabeca.jpg (story 21h), achado-notas-chao.jpg (imagem 18h); não usadas: dividas-casal-cozinha.jpg (mesmo casal da capa), achado-mulher-carteira.jpg, achado-carteira-maos.jpg
- 2026-11-16: itinere-bicicleta-caida.jpg (capa carrossel A), itinere-pessoa-bicicleta-passeio.jpg (story 21h), parental-mae-filha-caminho.jpg (capa carrossel B), parental-mulher-mao-crianca.jpg (story 22h), citacao-mulher-sofa.jpg (imagem 10h30), citacao-papel-maos.jpg (imagem 18h); não usadas: itinere-mulher-bicicleta-estrada.jpg, parental-mulher-crianca-neve.jpg, experimental-aperto-maos.jpg, experimental-mulher-papeis.jpg
