import os,sys
from playwright.sync_api import sync_playwright
from PIL import Image
src=open('/home/claude/mcg-imagens/modelos/dia-2026-11-22/gen.py').read()
head=src[:src.index('P={}')].replace("2026-11-22/","2026-11-24/").replace("build/d22/","build/d24/")
exec(head)
P={}
# ===== CARROSSEL A — Patrícia / compra do filho menor (Black Friday) =====
SHOP=""":root{--a1:#ffb347;--a2:#5fd3e6}
.sticker{background:#ffb347;color:#0f1f3d;border:4px solid #fff}
.rec{margin-top:34px;align-self:center;width:640px;background:#f6f1e6;color:#0f1f3d;font-family:Mono;font-size:30px;line-height:1.6;padding:34px 40px 46px;transform:rotate(-2deg);box-shadow:0 18px 30px rgba(0,0,0,.35);position:relative}
.rec:after{content:'';position:absolute;left:0;right:0;bottom:-16px;height:16px;background:linear-gradient(-45deg,transparent 12px,#f6f1e6 0) 0 0/24px 16px,linear-gradient(45deg,transparent 12px,#f6f1e6 0) 0 0/24px 16px}
.rec b{font-family:AB;font-size:34px}
.rec .l{display:flex;justify-content:space-between}"""
def tags(h=1350,op=.18):
    t=''.join(f'<g transform="translate({x},{y}) rotate({r})" opacity="{op}"><path d="M0 0 h120 l40 40 l-40 40 h-120 z" fill="none" stroke="#ffb347" stroke-width="4"/><circle cx="122" cy="40" r="8" fill="none" stroke="#ffb347" stroke-width="4"/><text x="16" y="52" font-family="AB" font-size="30" fill="#ffb347">-{p}%</text></g>' for x,y,r,p in [(820,170,18,30),(60,1060 if h==1350 else 1500,-14,50),(860,(1150 if h==1350 else 1560),8,20)])
    return f'<div class="deco"><svg width="1080" height="{h}">{t}</svg></div>'
AA='BLACK FRIDAY · FAMÍLIA'
A=[]
A.append(photo('menor-mae-filho-sofa.jpg','40% center')+'''<div class="bottom"><div class="sticker">BLACK FRIDAY · 27 NOV</div><div class="lab">A HISTÓRIA DA PATRÍCIA</div>
<h1 style="font-size:64px">O Tomás tem 9 anos. <em>Gastou 300&nbsp;€ numa promoção, sozinho.</em></h1><div class="swipe">DESLIZE ▶▶</div></div>''')
A.append(tags()+'''<div class="wrap"><div class="lab">PASSO 1 · O CONFLITO</div><h1>Pagou. <em>E agora?</em></h1>
<div class="rec"><div class="l"><b>TELEMÓVEL</b><b>299,90&nbsp;€</b></div><div class="l"><span>PAGO EM DINHEIRO</span><span>✔</span></div><div class="l"><span>CLIENTE: 9 ANOS</span><span>?</span></div></div>
<p>Juntou as prendas de anos, viu o desconto e comprou-o numa loja do centro comercial. <b>A Patrícia só soube ao jantar.</b></p></div>''')
A.append(tags()+'''<div class="wrap"><div class="lab">PASSO 2 · O ERRO</div><div class="bubble">“Pagou, está pago. A loja já não tem de desfazer nada.”</div>
<div class="x"><i>✖</i>É o que muita gente pensa.</div><p>Uma criança não pode, em regra, fazer sozinha <b>uma compra destas.</b></p></div>''')
A.append(tags(op=.1)+'''<div class="wrap"><div class="lab">PASSO 3 · A REGRA</div><h1>Os pais podem <em>pedir a anulação.</em></h1>
<p>Os menores não têm, em regra, capacidade para fazer negócios sozinhos. A compra é anulável a pedido dos pais, <b>no prazo de um ano</b> a contar do dia em que souberam dela.</p><div class="law">Código Civil, arts. 123.º e 125.º, n.º 1, al. a)</div></div>''')
A.append(tags(op=.1)+'''<div class="wrap"><div class="lab">PASSO 4 · ATENÇÃO</div><h1>As pequenas despesas <em>contam.</em></h1>
<div class="warn">Um lanche, um livro ou um bilhete de cinema são válidos: são <b>despesas da vida corrente, de pequena importância.</b> Um telemóvel de 300&nbsp;€, aos 9 anos, dificilmente será.</div>
<p>Guarde o talão e fale com a loja por escrito.</p><div class="law">Código Civil, art. 127.º, n.º 1, al. b)</div></div>''')
A.append(photo('menor-mae-filho-retrato.jpg','45% center')+'''<div class="bottom"><div class="lab">O DIREITO DELA</div>
<h1 style="font-size:58px">A Patrícia podia desfazer a compra. <em>A lei protege quem ainda não tem idade para decidir.</em></h1>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''')
for i,b in enumerate(A,1): P[f'1230-carrossel-{i}']=doc(SHOP,b+hud(i,AA)+FOOT)
# ===== CARROSSEL B — Património / Leonor / faturas por cobrar =====
src2=src[src.index('PAT="""'):src.index('BP=[]')]
exec(src2)
exec(src[src.index("SF='"):src.index("VF=")])
BP=[]
BP.append(pslide(1,'''<div class="pbottom"><div class="tag">FECHO DO ANO · FATURAS POR COBRAR</div><div class="k" style="margin-top:6px">A HISTÓRIA DA LEONOR</div>
<div class="t" style="font-size:62px">Três faturas por pagar. <i>O cliente diz sempre «para a semana».</i></div></div>''','faturas-empresaria-fato.jpg','55% center'))
BP.append(pslide(2,'''<div class="pw"><div class="k">O CONFLITO</div><div class="t">Quatro meses <i>à espera.</i></div><div class="rule"></div>
<div class="b">A Leonor tem uma empresa de interiores. Um cliente deve-lhe 18&nbsp;000&nbsp;€. Não é raro: só duas em cada dez empresas portuguesas pagam a tempo.</div>
<div class="ref">ESTUDO INFORMA D&amp;B, JULHO DE 2026</div></div>'''))
BP.append(pslide(3,'''<div class="pw"><div class="k">O ERRO COMUM</div><div class="rule" style="margin-top:30px"></div>
<div class="q">«Cobrar juros vai estragar a relação. Mais vale esperar.»</div><div class="rule"></div>
<div class="b">É assim que muitas empresas acabam a financiar, sem querer, <i style="color:#e3c167">os clientes que pagam tarde.</i></div></div>'''))
BP.append(pslide(4,'''<div class="pw"><div class="k">A REGRA</div><div class="t">O atraso <i>tem um custo.</i></div><div class="rule"></div>
<div class="b">Quem paga tarde deve juros de mora. Entre empresas, o credor tem ainda direito a pelo menos 40&nbsp;€ pelos custos de cobrança, sem ter de os pedir antes.</div>
<div class="ref">CÓDIGO CIVIL, ART. 806.º · DL N.º 62/2013, ART. 7.º, N.º 1</div></div>'''))
BP.append(pslide(5,'''<div class="pw"><div class="k">ATENÇÃO</div><div class="t">A prova <i>decide.</i></div><div class="rule"></div>
<div class="b">Guarde as faturas, as guias de entrega e os e-mails em que o cliente admite a dívida. Uma interpelação escrita, com data, faz toda a diferença.</div></div>'''))
BP.append(pslide(6,'''<div class="pbottom"><div class="k">O DIREITO DELA</div><div class="t" style="font-size:54px">A Leonor tinha direito ao capital, aos juros e aos 40&nbsp;€. <i>Não era um favor que pedia.</i></div>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''','faturas-empresaria-retrato.jpg','40% center'))
for i,b in enumerate(BP,1): P[f'2000-carrossel-{i}']=doc(PAT,b+FOOT)
# ===== IMAGEM 10h30 — Pode ou não pode (senhorio) =====
KEY=""":root{--a1:#e3c167;--a2:#9fd8ff}"""
DOOR='<div class="deco"><svg width="1080" height="1350"><g opacity=".22" stroke="#9fd8ff" stroke-width="4" fill="none"><rect x="860" y="760" width="150" height="300" rx="6"/><circle cx="985" cy="915" r="9"/><path d="M860 760 l-60 30 v300 l60 -30"/></g></svg></div>'
P['1030-imagem']=doc(KEY,'''<div class="photo" style="background-image:url(file://'''+F+'''senhorio-chave-porta.jpg);background-position:center 45%;height:700px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:400px;height:320px;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:34px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">PODE OU NÃO PODE?</div>
<div style="position:absolute;top:56px;right:70px;z-index:5;font-family:Mono;font-size:26px;color:#0f1f3d;background:#9fd8ff;padding:8px 16px;transform:rotate(3deg)">CASA ARRENDADA</div>
<div style="position:absolute;left:80px;right:80px;top:620px;z-index:3">
<h1 style="font-size:58px;padding-right:120px">O senhorio pode entrar em minha casa quando eu não estou?</h1>
<div style="font-family:AB;font-size:96px;color:#e3c167;margin-top:18px">NÃO PODE.</div>
<p style="font-size:33px;margin-top:10px">A casa arrendada é o domicílio de quem lá vive. O senhorio pode examiná-la, mas <b>em dia e hora combinados.</b> Entrar sem consentimento pode ser crime.</p>
<div class="law">Código Civil, art. 1038.º, al. b) · Código Penal, art. 190.º</div></div>'''+FOOT)
# ===== IMAGEM 18h00 — O Advogado comenta (crédito ao consumo) =====
NEWS=""":root{--a1:#e3c167;--a2:#9fd8ff}
.qt{font-family:PF;font-style:italic;font-size:44px;line-height:1.25;color:#fff;border-left:4px solid #e3c167;padding-left:26px;margin-top:26px}
.qa{font-size:24px;color:#b9c3dc;margin-top:10px;padding-left:30px;letter-spacing:1px}
.ln{font-size:31px;line-height:1.45;margin-top:16px;text-align:justify;hyphens:none}.ln b{color:#e3c167}"""
P['1800-imagem']=doc(NEWS,'''<div class="photo" style="background-image:url(file://'''+F+'''credito-mulher-cartao.jpg);background-position:center 35%;height:560px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:280px;height:300px;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:34px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">O ADVOGADO COMENTA</div>
<div style="position:absolute;top:56px;right:70px;z-index:5;font-family:Mono;font-size:26px;color:#0f1f3d;background:#9fd8ff;padding:8px 16px;transform:rotate(3deg)">CRÉDITO · 20 NOV</div>
<div style="position:absolute;left:80px;right:80px;top:470px;z-index:3">
<h1 style="font-size:54px">A nova lei do «compre agora, <em>pague depois»</em> ainda não chegou.</h1>
<div class="qt">«Enfim… era hoje, mas não foi!»</div><div class="qa">DUARTE GOMES PEREIRA, ASFAC · JORNAL PT50</div>
<div class="ln"><b>O que aconteceu:</b> a diretiva europeia devia aplicar-se desde 20 de novembro. Segundo a ASFAC, falta a lei portuguesa.</div>
<div class="ln"><b>Para si:</b> antes de pagar em prestações, veja o custo total.</div>
<div class="law">Diretiva (UE) 2023/2225, art. 48.º</div></div>'''+FOOT)
# ===== STORIES =====
VF='<div style="font-family:AB;font-size:50px;color:#0f1f3d;background:#e3c167;align-self:flex-start;padding:10px 24px">VERDADEIRO OU FALSO?</div>'
P['0700-story-1']=story(SHOP,tags(1920),'''<div class="sticker" style="align-self:flex-start">BLACK FRIDAY · 27 NOV</div><h1 style="font-size:80px">O seu filho de 9 anos comprou um telemóvel sozinho.</h1><p style="font-size:44px;text-align:left">Pagou com as poupanças dele. Pode desfazer a compra?</p>''')
P['0700-story-2']=story(SHOP,tags(1920),VF+'''<h1 style="font-size:78px;margin-top:50px">“Se o meu filho menor comprou e pagou, a compra já não se pode desfazer.”</h1>''')
P['0700-story-3']=story(SHOP,tags(1920),'''<div style="font-family:AB;font-size:130px;color:#ff7a6b">FALSO.</div><p style="font-size:46px;text-align:left">Em regra, os pais podem pedir a anulação no prazo de um ano depois de saberem. <b>As pequenas despesas do dia a dia são válidas.</b></p><div class="law" style="font-size:30px">Código Civil, arts. 125.º e 127.º</div>''')
PS='<div class="frame"></div><div class="selo" style="top:150px">PATRIMÓNIO</div>'
P['1500-story-1']=story(PAT,PS,'''<div class="tag" style="align-self:flex-start">FECHO DO ANO</div><div class="t" style="font-size:80px">Só duas em cada dez empresas portuguesas <i>pagam a tempo.</i></div><div class="b" style="font-size:40px;margin-top:24px;text-align:left">E as faturas da sua empresa?</div>''')
P['1500-story-2']=story(PAT,PS,VF+'''<div class="q" style="font-size:72px;margin-top:60px">«Se o cliente paga tarde, só me resta esperar.»</div>''')
P['1500-story-3']=story(PAT,PS,'''<div class="t" style="font-size:120px;color:#e3c167">Falso.</div><div class="b" style="font-size:46px;margin-top:30px">Entre empresas, o atraso dá direito a juros e a pelo menos 40&nbsp;€ pelos custos de cobrança.</div><div class="ref">DL N.º 62/2013, ART. 7.º, N.º 1</div>''')
P['2100-story']=story(SHOP,'','''<div class="sticker" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><h1 style="font-size:74px">O filho comprou sozinho na promoção? <em>A compra pode ser anulada.</em></h1><p style="font-size:42px;text-align:left">Veja a história da Patrícia no post de hoje. Deixe a sua dúvida nos comentários do post.</p>''','menor-mae-filho-tv.jpg','40% center')
P['2200-story']=story(PAT,'<div class="selo" style="top:150px">PATRIMÓNIO</div>','''<div class="tag" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><div class="t" style="font-size:74px">Faturas por cobrar? <i>O atraso tem um custo para quem deve.</i></div><div class="b" style="font-size:42px;margin-top:24px;text-align:left">A história da Leonor está no post de hoje. Deixe a sua dúvida nos comentários do post.</div>''','faturas-empresaria-caderno.jpg','45% center')
only=sys.argv[1:]
os.makedirs(OUT,exist_ok=True); os.makedirs(B,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
    pg=b.new_page()
    for k,h in P.items():
        if only and k not in only: continue
        H=1920 if 'story' in k else 1350
        pg.set_viewport_size({'width':1080,'height':H})
        fn=B+k+'.html'; open(fn,'w').write(h); pg.goto('file://'+fn); pg.wait_for_timeout(600)
        pg.screenshot(path=B+k+'.png'); Image.open(B+k+'.png').convert('RGB').save(OUT+k+'.jpg',quality=92)
    b.close()
print('ok',len(P))
