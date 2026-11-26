import os,sys
from playwright.sync_api import sync_playwright
from PIL import Image
src=open('/home/claude/mcg-imagens/modelos/dia-2026-11-22/gen.py').read()
head=src[:src.index('P={}')].replace("2026-11-22/","2026-11-26/").replace("build/d22/","build/d26/")
exec(head)
P={}
# ===== CARROSSEL A — Beatriz / colação (casas sobrevalorizadas) =====
CASA=""":root{--a1:#e3c167;--a2:#9fd8ff}
.sticker{background:#e3c167;color:#0f1f3d;border:4px solid #fff}
.card{margin-top:34px;align-self:center;width:660px;background:#f6f1e6;color:#0f1f3d;font-family:Mono;font-size:30px;line-height:1.7;padding:30px 40px;transform:rotate(-2deg);box-shadow:0 18px 30px rgba(0,0,0,.35)}
.card b{font-family:AB;font-size:32px}.card .l{display:flex;justify-content:space-between}.card .up{color:#7a1f2b}"""
def casas(h=1350,op=.16):
    t=''.join(f'<g transform="translate({x},{y})" opacity="{op}" stroke="#9fd8ff" stroke-width="4" fill="none"><path d="M0 70 L70 0 L140 70 V160 H0 Z"/><rect x="50" y="100" width="40" height="60"/><path d="M150 40 h70 M185 10 v60" stroke="#e3c167"/></g>' for x,y in [(830,150),(70,(1100 if h==1350 else 1560)),(840,(1130 if h==1350 else 1600))])
    return f'<div class="deco"><svg width="1080" height="{h}">{t}</svg></div>'
AA='CASAS · HERANÇAS'
A=[]
A.append(photo('colacao-mulher-album.jpg','30% center')+'''<div class="bottom"><div class="sticker" style="margin-bottom:44px">CASAS SOBREVALORIZADAS · 24 NOV</div><div class="lab">A HISTÓRIA DA BEATRIZ</div>
<h1 style="font-size:62px">As casas nunca valeram tanto. <em>E a que o irmão recebeu em vida?</em></h1><div class="swipe">DESLIZE ▶▶</div></div>''')
A.append(casas()+'''<div class="wrap"><div class="lab">PASSO 1 · O CONFLITO</div><h1>Uma casa <em>dada em 2009.</em></h1>
<div class="card"><div class="l"><b>DOAÇÃO · T2</b><b>2009</b></div><div class="l"><span>VALOR NA ESCRITURA</span><span>90&nbsp;000&nbsp;€</span></div><div class="l up"><span>VALOR HOJE</span><span>260&nbsp;000&nbsp;€</span></div></div>
<p>Os pais deram um apartamento ao irmão da Beatriz. A mãe morreu este ano. <b>Na partilha, ele diz que a casa é só dele.</b></p></div>''')
A.append(casas()+'''<div class="wrap"><div class="lab">PASSO 2 · O ERRO</div><div class="bubble">“O que os pais me deram em vida já não entra na herança.”</div>
<div class="x"><i>✖</i>É o que muita gente pensa.</div><p>Entre filhos, a lei procura <b>a igualdade na partilha.</b></p></div>''')
A.append(casas(op=.1)+'''<div class="wrap"><div class="lab">PASSO 3 · A REGRA</div><h1>A doação <em>volta às contas.</em></h1>
<p>O filho que recebeu bens dos pais e quer herdar tem de os levar à partilha, para igualar os irmãos. <b>Chama-se colação.</b></p><div class="law">Código Civil, art. 2104.º, n.º 1</div></div>''')
A.append(casas(op=.1)+'''<div class="wrap"><div class="lab">PASSO 4 · ATENÇÃO</div><h1>Conta o valor <em>de hoje.</em></h1>
<div class="warn">A casa doada vale o que valer <b>à data da morte</b>, não o que dizia a escritura.</div>
<p>Leia a escritura: se os pais dispensaram a colação, as contas mudam.</p><div class="law">Código Civil, arts. 2109.º, n.º 1, e 2113.º, n.º 1</div></div>''')
A.append(photo('miguel-cover.jpg','center 30%')+'''<div class="bottom"><div class="lab">O DIREITO DELA</div>
<h1 style="font-size:56px">A Beatriz tinha direito a uma partilha igual. <em>A casa do irmão também entrava nas contas.</em></h1>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''')
for i,b in enumerate(A,1): P[f'1230-carrossel-{i}']=doc(CASA,b+hud(i,AA)+FOOT)
# ===== CARROSSEL B — Património / Teresa / divórcio e crédito =====
src2=src[src.index('PAT="""'):src.index('BP=[]')]
exec(src2)
exec(src[src.index("SF='"):src.index("VF=")])
BP=[]
BP.append(pslide(1,'''<div class="pbottom"><div class="tag">CRÉDITO À HABITAÇÃO · 24 NOV</div><div class="k" style="margin-top:6px">A HISTÓRIA DA TERESA</div>
<div class="t" style="font-size:62px">Divorciou-se. <i>O crédito da casa continuou em seu nome.</i></div></div>''','divcredito-mulher-anel.jpg','center 45%'))
BP.append(pslide(2,'''<div class="pw"><div class="k">O CONFLITO</div><div class="t">Dois apartamentos, <i>dois créditos.</i></div><div class="rule"></div>
<div class="b">Na partilha, o ex-marido ficou com um deles e com o empréstimo. Ficou escrito. Um ano depois, o banco escreveu à Teresa.</div></div>'''))
BP.append(pslide(3,'''<div class="pw"><div class="k">O ERRO COMUM</div><div class="rule" style="margin-top:30px"></div>
<div class="q">«A dívida passou para ele. Já não é comigo.»</div><div class="rule"></div>
<div class="b">O acordo vale entre os dois. <i style="color:#e3c167">O banco não o assinou.</i></div></div>'''))
BP.append(pslide(4,'''<div class="pw"><div class="k">A REGRA</div><div class="t">Sem o banco, <i>nada muda.</i></div><div class="rule"></div>
<div class="b">Quem passa uma dívida a outra pessoa só fica livre se o credor o declarar expressamente. Até lá, continua a responder por ela.</div>
<div class="ref">CÓDIGO CIVIL, ART. 595.º, N.º 2</div></div>'''))
BP.append(pslide(5,'''<div class="pw"><div class="k">ATENÇÃO</div><div class="t">Peça-o <i>por escrito.</i></div><div class="rule"></div>
<div class="b">Antes de assinar a partilha, negocie com o banco a saída do seu nome. Guarde a resposta junto da escritura.</div></div>'''))
BP.append(pslide(6,'''<div class="pbottom"><div class="k">O DIREITO DELA</div><div class="t" style="font-size:52px">A Teresa podia pedir ao banco que a libertasse. <i>E exigir ao ex-marido o que ele assumiu.</i></div>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''','miguel-cover.jpg','center 30%'))
for i,b in enumerate(BP,1): P[f'2000-carrossel-{i}']=doc(PAT,b+FOOT)
# ===== IMAGEM 10h30 — Pode ou não pode (férias alteradas) =====
KEY=""":root{--a1:#e3c167;--a2:#9fd8ff}"""
P['1030-imagem']=doc(KEY,'''<div class="photo" style="background-image:url(file://'''+F+'''ferias-mulher-mala.jpg);background-position:70% 30%;height:1350px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:300px;height:1050px;z-index:2;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d 32%)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:34px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">PODE OU NÃO PODE?</div>
<div style="position:absolute;top:56px;right:70px;z-index:5;font-family:Mono;font-size:26px;color:#0f1f3d;background:#9fd8ff;padding:8px 16px;transform:rotate(3deg)">FÉRIAS DE NATAL</div>
<div style="position:absolute;left:80px;right:80px;top:600px;z-index:3">
<h1 style="font-size:56px;padding-right:80px">A empresa pode mudar-me as férias que já estavam marcadas?</h1>
<div style="font-family:AB;font-size:96px;color:#e3c167;margin-top:14px">DEPENDE.</div>
<p style="font-size:33px;margin-top:8px">A lei só o admite por <b>exigências imperiosas</b> da empresa. E se a mudança lhe trouxer prejuízos, como uma viagem já paga, tem direito a ser indemnizado.</p>
<div class="law">Código do Trabalho, art. 243.º, n.º 1</div></div>'''+FOOT)
# ===== IMAGEM 18h00 — O Advogado comenta (TGV / expropriações) =====
NEWS=""":root{--a1:#e3c167;--a2:#9fd8ff}
.ln{font-size:31px;line-height:1.45;margin-top:16px;text-align:justify;hyphens:none}.ln b{color:#e3c167}"""
P['1800-imagem']=doc(NEWS,'''<div class="photo" style="background-image:url(file://'''+F+'''tgv-mulher-caixas.jpg);background-position:center 40%;height:560px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:280px;height:300px;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:34px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">O ADVOGADO COMENTA</div>
<div style="position:absolute;top:56px;right:70px;z-index:5;font-family:Mono;font-size:26px;color:#0f1f3d;background:#9fd8ff;padding:8px 16px;transform:rotate(3deg)">ALTA VELOCIDADE · 25 NOV</div>
<div style="position:absolute;left:80px;right:80px;top:470px;z-index:3">
<h1 style="font-size:54px">Linha do TGV no Porto: moradores têm de sair <em>até junho de 2027.</em></h1>
<div class="ln"><b>O que aconteceu:</b> os moradores afetados pela obra têm de deixar as casas até ao fim de junho de 2027, noticiou a Lusa.</div>
<div class="ln"><b>O que diz a lei:</b> uma expropriação só se faz mediante justa indemnização, pelo valor real e corrente do bem.</div>
<div class="ln"><b>Para si:</b> guarde escrituras, contratos e fotografias da casa.</div>
<div class="law">Constituição, art. 62.º, n.º 2 · Código das Expropriações, art. 23.º, n.º 1</div></div>'''+FOOT)
# ===== STORIES =====
VF='<div style="font-family:AB;font-size:50px;color:#0f1f3d;background:#e3c167;align-self:flex-start;padding:10px 24px">VERDADEIRO OU FALSO?</div>'
P['0700-story-1']=story(CASA,casas(1920),'''<div class="sticker" style="align-self:flex-start">CASAS · 24 NOV</div><h1 style="font-size:80px">As casas nunca valeram tanto. E a que os pais deram a um dos filhos?</h1><p style="font-size:44px;text-align:left">Na herança, conta ou não conta?</p>''')
P['0700-story-2']=story(CASA,casas(1920),VF+'''<h1 style="font-size:78px;margin-top:50px">“O que os pais deram a um filho em vida já não entra na herança.”</h1>''')
P['0700-story-3']=story(CASA,casas(1920),'''<div style="font-family:AB;font-size:130px;color:#ff7a6b">FALSO.</div><p style="font-size:46px;text-align:left">Em regra, o filho que quer herdar leva a doação à partilha. <b>E conta o valor à data da morte.</b></p><div class="law" style="font-size:30px">Código Civil, arts. 2104.º e 2109.º</div>''')
PS='<div class="frame"></div><div class="selo" style="top:150px">PATRIMÓNIO</div>'
P['1500-story-1']=story(PAT,PS,'''<div class="tag" style="align-self:flex-start">CRÉDITO À HABITAÇÃO</div><div class="t" style="font-size:80px">Divorciou-se e ele ficou com a casa e o crédito. <i>O banco sabe disso?</i></div>''')
P['1500-story-2']=story(PAT,PS,VF+'''<div class="q" style="font-size:66px;margin-top:60px">«Se a partilha passou a dívida para ele, o banco já não me pode exigir nada.»</div>''')
P['1500-story-3']=story(PAT,PS,'''<div class="t" style="font-size:120px;color:#e3c167">Falso.</div><div class="b" style="font-size:46px;margin-top:30px">Sem declaração expressa do banco, continua a responder pela dívida.</div><div class="ref">CÓDIGO CIVIL, ART. 595.º, N.º 2</div>''')
P['2100-story']=story(CASA,'','''<div class="sticker" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><h1 style="font-size:74px">O irmão recebeu uma casa em vida? <em>Na partilha, pode contar.</em></h1><p style="font-size:42px;text-align:left">Veja a história da Beatriz no post de hoje. Deixe a sua dúvida nos comentários do post.</p>''','colacao-album-maos.jpg','center')
P['2200-story']=story(PAT,'<div style="position:absolute;left:0;right:0;top:0;height:480px;background:linear-gradient(rgba(15,31,61,.92),rgba(15,31,61,0));z-index:2"></div><div class="selo" style="top:150px">PATRIMÓNIO</div>','''<div class="tag" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><div class="t" style="font-size:74px">Divórcio com crédito à habitação? <i>O banco tem uma palavra a dizer.</i></div><div class="b" style="font-size:42px;margin-top:24px;text-align:left">A história da Teresa está no post de hoje. Deixe a sua dúvida nos comentários do post.</div>''','divcredito-maos-anel.jpg','center')
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
