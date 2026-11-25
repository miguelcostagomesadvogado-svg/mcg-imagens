import os,sys
from playwright.sync_api import sync_playwright
from PIL import Image
src=open('/home/claude/mcg-imagens/modelos/dia-2026-11-22/gen.py').read()
head=src[:src.index('P={}')].replace("2026-11-22/","2026-11-25/").replace("build/d22/","build/d25/")
exec(head)
exec(src[src.index("SF='"):src.index("VF=")])
P={}
NB='&nbsp;'
# ===== CARROSSEL A — Joana / reforço de Natal / recibo de vencimento =====
XMAS=""":root{--a1:#ff7a6b;--a2:#9fe0c0}
.sticker{background:#e3c167;color:#0f1f3d;border:4px solid #fff}
.rec{margin-top:34px;align-self:center;width:660px;background:#f6f1e6;color:#0f1f3d;font-family:Mono;font-size:31px;line-height:1.65;padding:34px 40px 46px;transform:rotate(-2deg);box-shadow:0 18px 30px rgba(0,0,0,.35);position:relative}
.rec:after{content:'';position:absolute;left:0;right:0;bottom:-16px;height:16px;background:linear-gradient(-45deg,transparent 12px,#f6f1e6 0) 0 0/24px 16px,linear-gradient(45deg,transparent 12px,#f6f1e6 0) 0 0/24px 16px}
.rec b{font-family:AB;font-size:33px}.rec .l{display:flex;justify-content:space-between}.rec .no{color:#c0392b;font-family:AB}"""
def lights(h=1350,op=.9):
    cols=['#e3c167','#ff7a6b','#9fe0c0','#f6f1e6']
    path=f'<path d="M-20 70 Q 270 150 540 80 T 1100 90" fill="none" stroke="#b9c3dc" stroke-width="2" opacity=".5"/>'
    pts=[(40,86),(130,107),(220,120),(310,122),(400,112),(490,94),(580,80),(670,86),(760,103),(850,112),(940,108),(1030,95)]
    b=''.join(f'<circle cx="{x}" cy="{y+14}" r="9" fill="{cols[i%4]}" opacity="{op}"/><circle cx="{x}" cy="{y+14}" r="22" fill="{cols[i%4]}" opacity=".18"/>' for i,(x,y) in enumerate(pts))
    return f'<div class="deco"><svg width="1080" height="{h}" style="position:absolute;top:{60 if h==1350 else 120}px">{path}{b}</svg></div>'
AA='NATAL · TRABALHO'
A=[]
A.append(photo('recibo-loja-tablet.jpg','25% center')+'''<div class="bottom"><div class="sticker">REFORÇO DE NATAL · NOV 2026</div><div class="lab">A HISTÓRIA DA JOANA</div>
<h1 style="font-size:64px">Entrou no reforço de Natal. <em>O salário chegou por MB Way, sem recibo.</em></h1><div class="swipe">DESLIZE ▶▶</div></div>''')
A.append(lights()+f'''<div class="wrap"><div class="lab">PASSO 1 · O CONFLITO</div><h1>Primeiro salário. <em>Nenhum papel.</em></h1>
<div class="rec"><div class="l"><b>SALÁRIO</b><b>TRANSFERIDO ✔</b></div><div class="l"><span>DESCONTOS</span><span>?</span></div><div class="l"><span>RECIBO</span><span class="no">NÃO HÁ</span></div></div>
<p>A Joana foi contratada por uma loja para a época de Natal. Pediu o recibo e ouviu: <b>«Isso depois vê-se.»</b></p></div>''')
A.append(lights()+'''<div class="wrap"><div class="lab">PASSO 2 · O ERRO</div><div class="bubble">“É só um mês. Recibo é para quem fica na casa.”</div>
<div class="x"><i>✖</i>É o que muita gente pensa.</div><p>Um contrato curto <b>continua a ser um contrato de trabalho.</b></p></div>''')
A.append(lights(op=.5)+'''<div class="wrap"><div class="lab">PASSO 3 · A REGRA</div><h1>Cada salário, <em>o seu recibo.</em></h1>
<p>Até ao pagamento, a empresa tem de entregar um documento com a categoria, o número da Segurança Social, a retribuição, os descontos e o <b>valor líquido</b>.</p><div class="law">Código do Trabalho, art. 276.º, n.º 3</div></div>''')
A.append(lights(op=.5)+'''<div class="wrap"><div class="lab">PASSO 4 · ATENÇÃO</div><h1>Sem recibo, <em>falta a prova.</em></h1>
<div class="warn">É pelo recibo que vê o que lhe foi descontado. E é com ele que confirma se o seu trabalho foi <b>declarado à Segurança Social.</b></div>
<p>Guarde os comprovativos das transferências e veja as remunerações declaradas na Segurança Social Direta.</p></div>''')
A.append(photo('recibo-loja-cabides.jpg','30% center')+'''<div class="bottom"><div class="lab">O DIREITO DELA</div>
<h1 style="font-size:56px">A Joana tinha direito ao recibo desde o primeiro salário. <em>Mesmo num contrato de Natal.</em></h1>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''')
for i,b in enumerate(A,1): P[f'1230-carrossel-{i}']=doc(XMAS,b+hud(i,AA)+FOOT)
# ===== CARROSSEL B — Sara / rendas 2027 =====
HOME=""":root{--a1:#9fd8ff;--a2:#9fd8ff}
.sticker{background:#9fd8ff;color:#0f1f3d;border:4px solid #fff}
.msg{margin-top:34px;align-self:flex-start;max-width:820px;background:#f6f1e6;color:#0f1f3d;border-radius:28px 28px 28px 6px;padding:30px 36px;font-size:36px;line-height:1.4}
.msg small{display:block;font-family:Mono;font-size:24px;color:#4a5a7a;margin-bottom:8px}
.calc{margin-top:34px;border:3px solid #9fd8ff;border-radius:10px;padding:26px 34px;font-family:Mono;font-size:33px;line-height:1.75;background:rgba(159,216,255,.06)}
.calc .l{display:flex;justify-content:space-between}.calc .t{border-top:2px dashed #9fd8ff;margin-top:8px;padding-top:8px;color:#e3c167;font-family:AB}"""
def houses(h=1350,op=.16):
    hs=''.join(f'<g transform="translate({x},{y}) scale({s})" opacity="{op}" fill="none" stroke="#9fd8ff" stroke-width="4"><path d="M0 70 L70 10 L140 70 V160 H0 Z"/><rect x="55" y="105" width="30" height="55"/><rect x="18" y="85" width="26" height="22"/><rect x="96" y="85" width="26" height="22"/></g>' for x,y,s in [(860,150,1.0),(40,1080 if h==1350 else 1560,.8),(900,1050 if h==1350 else 1500,1.3)])
    pct=f'<text x="660" y="{330 if h==1350 else 420}" font-family="AB" font-size="120" fill="#9fd8ff" opacity=".08">2,56%</text>'
    return f'<div class="deco"><svg width="1080" height="{h}">{hs}{pct}</svg></div>'
BB='RENDAS 2027 · ARRENDAMENTO'
BS=[]
BS.append(photo('renda-cozinha-cartao.jpg','35% center')+'''<div class="bottom"><div class="sticker">RENDAS 2027 · +2,56%</div><div class="lab">A HISTÓRIA DA SARA</div>
<h1 style="font-size:62px">Ia pagar a renda quando chegou a mensagem do senhorio. <em>Mais 10% em janeiro.</em></h1><div class="swipe">DESLIZE ▶▶</div></div>''')
BS.append(houses()+'''<div class="wrap"><div class="lab">PASSO 1 · O CONFLITO</div><h1>De 650&nbsp;€ <em>para 715&nbsp;€.</em></h1>
<div class="msg"><small>SENHORIO · 08:12</small>Bom dia, Sara. A partir de janeiro a renda passa a 715&nbsp;€. Obrigado.</div>
<p>O contrato tem três anos e não diz nada sobre aumentos. <b>A Sara não sabia se tinha de aceitar.</b></p></div>''')
BS.append(houses()+'''<div class="wrap"><div class="lab">PASSO 2 · O ERRO</div><div class="bubble">“Janeiro é mês de aumentos. O senhorio sobe o que quiser.”</div>
<div class="x"><i>✖</i>É o que muita gente pensa.</div><p>Quando o contrato não diz nada, <b>não é assim.</b></p></div>''')
BS.append(houses(op=.1)+'''<div class="wrap"><div class="lab">PASSO 3 · A REGRA</div><h1>O limite <em>é 2,56%.</em></h1>
<div class="calc"><div class="l"><span>RENDA ATUAL</span><span>650,00&nbsp;€</span></div><div class="l"><span>COEFICIENTE 2027</span><span>× 1,0256</span></div><div class="l t"><span>MÁXIMO</span><span>666,64&nbsp;€</span></div></div>
<p>Se o contrato for omisso, a renda sobe uma vez por ano, pelo coeficiente que o INE publica.</p><div class="law">Código Civil, art. 1077.º, n.º 2</div></div>''')
BS.append(houses(op=.1)+'''<div class="wrap"><div class="lab">PASSO 4 · ATENÇÃO</div><h1>Por escrito <em>e com 30 dias.</em></h1>
<div class="warn">O senhorio tem de comunicar <b>por escrito</b> o coeficiente e a nova renda, com pelo menos 30 dias de antecedência.</div>
<p>Se o contrato tiver outra regra de atualização, vale o contrato. Leia-o antes de responder.</p><div class="law">Código Civil, art. 1077.º, n.º 2, al. c)</div></div>''')
BS.append(photo('miguel-cover.jpg','center 25%')+'''<div class="bottom"><div class="lab">O DIREITO DELA</div>
<h1 style="font-size:56px">A Sara podia pagar 666,64&nbsp;€, não 715&nbsp;€. <em>A lei põe um teto ao aumento.</em></h1>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''')
for i,b in enumerate(BS,1): P[f'2000-carrossel-{i}']=doc(HOME,b+hud(i,BB)+FOOT)
# ===== IMAGEM 10h30 — Portugueses no estrangeiro (aceitar a herança: 10 anos) =====
EMI=""":root{--a1:#e3c167;--a2:#9fd8ff}"""
PLANE='<div class="deco"><svg width="1080" height="1350"><g opacity=".2" stroke="#9fd8ff" stroke-width="3" fill="none" stroke-dasharray="10 12"><path d="M60 1180 Q 540 980 1020 1120"/></g></svg></div>'
P['1030-imagem']=doc(EMI,'''<div class="photo" style="background-image:url(file://'''+F+'''heranca-fotografias-mesa.jpg);background-position:center 40%;height:680px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:380px;height:320px;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d)"></div>'''+PLANE+'''
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:32px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">PORTUGUESES NO ESTRANGEIRO</div>
<div style="position:absolute;left:80px;right:80px;top:600px;z-index:3">
<h1 style="font-size:58px">Os seus pais morreram em Portugal e a herança ficou por tratar?</h1>
<div style="font-family:AB;font-size:92px;color:#e3c167;margin-top:16px">10 ANOS.</div>
<p style="font-size:34px;margin-top:8px">O direito de aceitar a herança caduca ao fim de dez anos, contados desde que soube que era herdeiro. <b>Pode tratar disto sem vir a Portugal.</b></p>
<div class="law">Código Civil, art. 2059.º, n.º 1</div></div>'''+FOOT)
# ===== IMAGEM 18h00 — O Advogado comenta (OE 2027 aprovado) =====
NEWS=""":root{--a1:#e3c167;--a2:#9fd8ff}
.ln{font-size:32px;line-height:1.45;margin-top:18px;text-align:justify;hyphens:none}.ln b{color:#e3c167}"""
P['1800-imagem']=doc(NEWS,'''<div class="photo" style="background-image:url(file://'''+F+'''oe-secretaria-telemovel.jpg);background-position:center 30%;height:560px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:280px;height:300px;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:34px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">O ADVOGADO COMENTA</div>
<div style="position:absolute;top:56px;right:70px;z-index:5;font-family:Mono;font-size:26px;color:#0f1f3d;background:#9fd8ff;padding:8px 16px;transform:rotate(3deg)">OE 2027 · 24 NOV</div>
<div style="position:absolute;left:80px;right:80px;top:480px;z-index:3">
<h1 style="font-size:58px">O Orçamento para 2027 foi aprovado. <em>Ainda não está em vigor.</em></h1>
<div class="ln"><b>O que aconteceu:</b> o Parlamento aprovou ontem o Orçamento, em votação final global.</div>
<div class="ln"><b>O que diz a lei:</b> o Presidente da República tem 20 dias para o promulgar ou vetar. Só depois de publicada no Diário da República a lei produz efeitos.</div>
<div class="ln"><b>Para si:</b> confirme a data em que cada medida começa a valer.</div>
<div class="law">Constituição, arts. 119.º e 136.º, n.º 1</div></div>'''+FOOT)
# ===== STORIES =====
VF='<div style="font-family:AB;font-size:50px;color:#0f1f3d;background:#e3c167;align-self:flex-start;padding:10px 24px">VERDADEIRO OU FALSO?</div>'
P['0700-story-1']=story(XMAS,lights(1920),'''<div class="sticker" style="align-self:flex-start">REFORÇO DE NATAL</div><h1 style="font-size:80px">Mais de 1.500 vagas temporárias para o Natal, só numa empresa.</h1><p style="font-size:44px;text-align:left">Vai trabalhar um mês numa loja? Saiba o que lhe devem entregar.</p>''')
P['0700-story-2']=story(XMAS,lights(1920),VF+'''<h1 style="font-size:78px;margin-top:50px">“Num contrato de um mês, a empresa não tem de dar recibo.”</h1>''')
P['0700-story-3']=story(XMAS,lights(1920),'''<div style="font-family:AB;font-size:130px;color:#ff7a6b">FALSO.</div><p style="font-size:46px;text-align:left">Até ao pagamento, a empresa entrega um documento com a retribuição, os descontos e o valor líquido. <b>Seja qual for a duração do contrato.</b></p><div class="law" style="font-size:30px">Código do Trabalho, art. 276.º, n.º 3</div>''')
P['1500-story-1']=story(HOME,houses(1920),'''<div class="sticker" style="align-self:flex-start">RENDAS 2027 · +2,56%</div><h1 style="font-size:80px">Recebeu aviso de aumento da renda para janeiro?</h1><p style="font-size:44px;text-align:left">Faça as contas antes de pagar.</p>''')
P['1500-story-2']=story(HOME,houses(1920),VF+'''<h1 style="font-size:78px;margin-top:50px">“Em janeiro, o senhorio pode subir a renda quanto quiser.”</h1>''')
P['1500-story-3']=story(HOME,houses(1920),'''<div style="font-family:AB;font-size:130px;color:#ff7a6b">FALSO.</div><p style="font-size:46px;text-align:left">Se o contrato nada disser, o aumento anual tem como limite o coeficiente do INE: <b>2,56% em 2027</b>. Comunicado por escrito, com 30 dias de antecedência.</p><div class="law" style="font-size:30px">Código Civil, art. 1077.º, n.º 2</div>''')
P['2100-story']=story(XMAS,'','''<div class="sticker" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><h1 style="font-size:74px">Reforço de Natal? <em>O recibo também é para si.</em></h1><p style="font-size:42px;text-align:left">Veja a história da Joana no post de hoje. Deixe a sua dúvida nos comentários do post.</p>''','recibo-loja-balcao.jpg','55% center')
P['2200-story']=story(HOME,'','''<div class="sticker" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><h1 style="font-size:74px">A renda vai subir em janeiro? <em>Há um limite: 2,56%.</em></h1><p style="font-size:42px;text-align:left">A história da Sara está no post de hoje. Deixe a sua dúvida nos comentários do post.</p>''','renda-janela.jpg','30% center')
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
