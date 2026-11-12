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
