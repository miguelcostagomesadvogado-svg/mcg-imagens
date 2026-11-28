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
- 2026-11-17: ipc-mae-abraco-cama.jpg (capa carrossel 19h00, pensão e inflação)
- 2026-11-19: ipc-mulher-mesa-chamada.jpg (capa carrossel 19h00, aumento da pensão); não usadas: ipc-mae-filha-bolas.jpg, ipc-mulher-mesa-telemovel.jpg
- 2026-11-17: avos-avo-abraca-neta.jpg (capa carrossel 12h30), avos-avo-pequeno-almoco.jpg (story 21h), domicilio-mulher-porta.jpg (capa carrossel 20h00), domicilio-porta-noite.jpg (story 22h), emails-mulher-portatil-2.jpg (imagem 10h30), fiador-mulher-sofa.jpg (imagem 18h); não usadas: emails-mulher-portatil.jpg, fiador-papel-maos.jpg (já usada a 16 nov.)
- 2026-11-18: sofia-carro-mao-cabeca.jpg (capa carrossel 19h00, história da Sofia — despedimento), sofia-carro-janela-2.jpg (diapositivo 2), sofia-carro-janela.jpg (diapositivo 3); a mesma modelo é a protagonista da história — não voltar a usar esta modelo noutras peças

## 2026-11-18
ferias-mulher-hotel-mala.jpg (capa 12h30), ferias-mulher-mala-relva.jpg (story 21h), procuracao-mulher-assina.jpg (10h30), fatura-senhora-calculadora.jpg (18h), infiltracao-balde-gota.jpg (capa 20h), infiltracao-bolor.jpg (story 22h)

## 2026-11-19
partilha-mulher-janela-casa.jpg (capa 12h30), partilha-mulher-chaves.jpg (story 21h), penhora-mulher-tapa-rosto.jpg (capa 20h), penhora-mulher-maos-rosto.jpg (story 22h), desconto-mulher-ferramentas.jpg (10h30), seguro-entrega-chave.jpg (18h); não usadas: partilha-mulher-porta-antiga.jpg (mulher a rir), seguro-maos-chave.jpg

## 2026-11-20 — Reels «Como trabalho» (pesquisa + passo a passo)
reelpesq-partilhas-mulher-oculos.jpg, reelpesq-divorcio-mulher-parede.jpg, reelpesq-alimentos-mae-sala.jpg, reelpesq-acidente-mulher-exterior.jpg, reelpesq-despedimento-mulher-azul.jpg, reelpesq-penal-mulher-noite.jpg; não usadas: reelpesq-cand02 (parece menor — nunca usar), reelpesq-cand05, reelpesq-cand10, reelpesq-cand12, reelpesq-cand11 (de costas, Pequim — não usar); a cand04 falhou o download
- 2026-11-20 (Reel «advogado em Portugal»): reelpesq-portugal-mulher-janela.jpg; não usadas: reelpt-cand01 a 07 e 09 (a cand04 parece muito jovem — não usar)

## 2026-11-21
falso-mulher-quadro-parede.jpg (capa 12h30), falso-mulher-museu.jpg (story 21h), chuva-mulher-retrato.jpg (capa 20h), chuva-mulher-janela.jpg (story 22h), devolve-mulher-cadeira.jpg (10h30), fora-mulher-telefone-hotel.jpg (18h); miguel-cover.jpg nos fechos; não usadas: falso-mulher-galeria-escura.jpg, chuva-mulher-vidro.jpg, devolve-mulher-fita-caixa.jpg

## 2026-11-22
persi-mulher-carta-cozinha.jpg (capa 12h30, história da Joana), persi-mulher-abraca-papeis.jpg (fecho 12h30), persi-mulher-mesa-pequeno-almoco.jpg (story 21h) — a mesma modelo; heranca-ue-mulher-blazer.jpg (capa 20h, história da Teresa, Património), heranca-ue-mulher-mala.jpg (fecho 20h), heranca-ue-mulher-documentos.jpg (story 22h) — a mesma modelo; imagem-mae-fotografa-filha.jpg (10h30), pais-idosos-maos.jpg (18h)

## 2026-11-23
lesao-mulher-palete.jpg (capa 12h30 e crachá do fecho, história da Carla), lesao-mulher-armazem-caixas.jpg (story 21h), natal-mae-filha-cama2.jpg (capa 20h, história da Daniela), natal-mae-filha-cama.jpg (fecho 20h) — a mesma modelo; natal-mae-filha-chao.jpg (story 22h), legitima-mae-filha-abraco.jpg (10h30), alcool-mulher-conduz-reflexo.jpg (18h); não usadas: lesao-mulher-armazem-pc.jpg, legitima-mae-filha-parque.jpg, alcool-mulher-conduz-noite.jpg

## 2026-11-24
menor-mae-filho-sofa, menor-mae-filho-retrato, menor-mae-filho-tv, faturas-empresaria-fato, faturas-empresaria-retrato, faturas-empresaria-caderno, credito-mulher-cartao, senhorio-chave-porta

## 2026-11-26
colacao-mulher-album.jpg (capa 12h30, história da Beatriz), colacao-album-maos.jpg (story 21h), divcredito-mulher-anel.jpg (capa 20h, história da Teresa, Património), divcredito-maos-anel.jpg (story 22h), ferias-mulher-mala.jpg (10h30), tgv-mulher-caixas.jpg (18h); miguel-cover.jpg nos fechos; não usada: tgv-mulher-caixa.jpg

## 2026-11-27
bf-mulher-encomenda.jpg (capa 12h30, história da Mariana), bf-mulher-porta.jpg (story 21h), ita-muleta-bengala.jpg (capa 20h, história da Cláudia), camara-vigilancia-parede.jpg (10h30), cao-mulher-labrador.jpg (18h); miguel-cover.jpg no fecho das 12h30; não usadas: ita-mulher-muletas.jpg (sorridente, não serve), cao-mulher-campo.jpg

## 2026-11-28
vd-mulher-telefone-escuro.jpg (capa 12h30, história da Catarina), vd-mulher-telefone-escuro-2.jpg (fecho 12h30) — a mesma modelo; vd-mulher-mao-rosto.jpg (story 21h), viuva-senhora-sofa.jpg (capa 20h, história da Isabel), viuva-alianca-mao.jpg (story 22h), marquise-varandas-fechadas.jpg (10h30), terreno-mulher-portao.jpg (18h); miguel-cover.jpg no fecho das 20h; não usadas: marquise-varanda-noite.jpg, terreno-mulher-vedacao.jpg
