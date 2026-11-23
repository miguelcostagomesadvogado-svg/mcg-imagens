import os
from playwright.sync_api import sync_playwright
from PIL import Image
R='/home/claude/mcg-imagens'; F=R+'/fotos/'; OUT=R+'/2026-11-23/'; B='/home/claude/build/d23/'
G='/usr/share/fonts/truetype/google-fonts/ofl/'; PF='/home/claude/fonts/package/files/'
BASE=f"""
@font-face{{font-family:AB;src:url(file://{G}archivoblack/ArchivoBlack-Regular.ttf)}}
@font-face{{font-family:Mono;src:url(file://{G}anonymouspro/AnonymousPro-Bold.ttf)}}
@font-face{{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-Regular.otf);font-weight:400}}
@font-face{{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-SemiBold.otf);font-weight:600}}
@font-face{{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-Bold.otf);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;background:linear-gradient(170deg,#0f1f3d 0%,#172d5e 100%);font-family:Inter;color:#f3eefc;position:relative;overflow:hidden}}
.hud{{position:absolute;top:44px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:center;font-family:Mono;font-size:26px;letter-spacing:3px;color:var(--a2);z-index:5}}
.bar{{display:flex;gap:6px;margin-left:16px}}.bar i{{width:34px;height:14px;border:2px solid #e3c167;display:block}}.bar i.on{{background:#e3c167}}
.lv{{display:flex;align-items:center}}
.wrap{{position:absolute;left:80px;right:80px;top:130px;bottom:150px;display:flex;flex-direction:column;justify-content:center;z-index:3}}
.lab{{align-self:flex-start;font-family:Mono;font-size:30px;letter-spacing:4px;color:var(--a1)}}
h1{{font-family:AB;font-size:72px;line-height:1.08;margin-top:22px;color:#fff}}
h1 em{{font-style:normal;color:#e3c167}}
p{{font-size:37px;line-height:1.48;text-align:justify;hyphens:none;margin-top:30px}}
p b{{color:var(--a2);font-weight:700}}
.law{{align-self:flex-start;display:inline-block;margin-top:30px;font-family:Mono;font-size:26px;color:#0f1f3d;background:#e3c167;padding:8px 16px;letter-spacing:1px}}
.card{{margin-top:34px;border:3px solid var(--a2);border-radius:6px;padding:28px 34px;background:rgba(95,211,230,.06);font-family:Mono;font-size:33px;line-height:1.7}}
.card span{{color:var(--a2)}} .card strong{{color:#e3c167}}
.bubble{{margin-top:34px;background:#fff;color:#0f1f3d;border-radius:26px;padding:36px 40px;font-family:AB;font-size:50px;line-height:1.18;position:relative}}
.bubble:after{{content:'';position:absolute;left:70px;bottom:-34px;border:18px solid transparent;border-top:20px solid #fff;border-left:22px solid #fff}}
.x{{margin-top:56px;display:flex;align-items:center;gap:22px;font-family:AB;font-size:46px;color:#ff7a6b}}
.x i{{font-style:normal;width:74px;height:74px;border:4px solid #ff7a6b;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:52px}}
.warn{{margin-top:34px;border:3px solid #e3c167;border-radius:14px;padding:28px 34px;background:rgba(227,193,103,.08);font-size:35px;line-height:1.5;text-align:justify;hyphens:none}}
.warn b{{color:#e3c167}}
.foot{{position:absolute;left:70px;right:70px;bottom:44px;display:flex;justify-content:space-between;font-weight:600;font-size:21px;letter-spacing:4px;color:#b9c3dc;z-index:5}}
.foot span:last-child{{color:#e3c167}}
.photo{{position:absolute;inset:0;background-size:cover;background-position:center}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,31,61,.35) 0%,rgba(15,31,61,0) 28%,rgba(15,31,61,.78) 56%,#0f1f3d 80%)}}
.bottom{{position:absolute;left:80px;right:80px;bottom:130px;z-index:3}}
.sticker{{display:inline-block;transform:rotate(-4deg);font-family:AB;font-size:38px;padding:12px 24px;margin-bottom:18px}}
.swipe{{margin-top:26px;font-family:Mono;font-size:30px;letter-spacing:4px;color:var(--a2)}}
.contact{{margin-top:22px;font-size:27px;line-height:1.6}}
.contact b{{color:#e3c167}}
.mini{{margin-top:16px;font-size:22px;color:#b9c3dc}}
.deco{{position:absolute;inset:0;z-index:1;pointer-events:none}}
svg{{display:block}}
"""
FOOT='<div style="position:absolute;left:0;right:0;bottom:0;height:120px;background:linear-gradient(to top,#0f1f3d 55%,rgba(15,31,61,0));z-index:4"></div><div class="foot"><span>MIGUEL COSTA GOMES · ADVOGADO</span><span>@MCG.ADVOGADO</span></div>'
CONTACT='''<div class="contact"><b>Miguel Costa Gomes</b> · Advogado · C.P. 11209P<br>miguelcostagomes-11209P@adv.oa.pt · +351 960 225 890</div>'''
def doc(css,body,h=1350):
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE}{css} body{{height:{h}px}}</style></head><body>{body}</body></html>'
def photo(f,pos='center'):
    return f'<div class="photo" style="background-image:url(file://{F}{f});background-position:{pos}"></div><div class="shade"></div>'
def hud(n,area):
    bars=''.join(f'<i class="{"on" if k<=n else ""}"></i>' for k in range(1,7))
    return f'<div class="hud"><span>{area}</span><span class="lv">{n}/6<span class="bar">{bars}</span></span></div>'
P={}
# ================= CARROSSEL A — Carla / armazém Black Friday / presunção art. 10.º =================
BOX=""":root{--a1:#ff9f43;--a2:#ffc27a}
.sticker{background:#ff9f43;color:#0f1f3d;border:4px solid #fff}
.tape{position:absolute;left:-60px;right:-60px;height:46px;background:repeating-linear-gradient(90deg,#ff9f43 0 120px,#f7b267 120px 240px);opacity:.9;transform:rotate(-4deg);z-index:2;display:flex;align-items:center;justify-content:center;font-family:Mono;font-size:22px;letter-spacing:8px;color:#0f1f3d}
.label{margin-top:34px;background:#f3eefc;color:#0f1f3d;border-radius:6px;padding:26px 30px;font-family:Mono;font-size:28px;line-height:1.6;display:flex;gap:28px;align-items:center}
.label b{font-family:AB;font-size:34px}
.badge{display:flex;gap:30px;align-items:center;margin-top:10px;background:#f3eefc;color:#0f1f3d;border-radius:18px;padding:24px;width:640px}
.badge .ph{width:170px;height:200px;border-radius:10px;background-size:cover;background-position:30% 20%}
.badge .n{font-family:AB;font-size:44px}.badge .r{font-family:Mono;font-size:24px;color:#3b4b70;margin-top:8px;line-height:1.5}"""
def barcode(w=300,h=90,c='#0f1f3d'):
    import random; random.seed(w+h); x=0; r=''
    while x<w:
        bw=random.choice([3,3,5,7]); r+=f'<rect x="{x}" y="0" width="{bw}" height="{h}" fill="{c}"/>'; x+=bw+random.choice([3,4,6])
    return f'<svg width="{w}" height="{h}">{r}</svg>'
def boxes(h=1350,op=.18):
    r=''
    for (x,y,s) in [(820,h-470,150),(930,h-560,110),(760,h-330,190),(40,h-300,120)]:
        r+=f'<g opacity="{op}"><rect x="{x}" y="{y}" width="{s}" height="{s*.8}" fill="none" stroke="#ff9f43" stroke-width="4"/><line x1="{x+s/2}" y1="{y}" x2="{x+s/2}" y2="{y+s*.8}" stroke="#ff9f43" stroke-width="10"/></g>'
    return f'<div class="deco"><svg width="1080" height="{h}">{r}</svg></div>'
AA='▲ ACIDENTE DE TRABALHO'
A=[]
A.append(photo('lesao-mulher-palete.jpg','40% 30%')+'''<div class="bottom"><div class="sticker">BLACK FRIDAY · 27 NOV</div><div class="lab">A HISTÓRIA DA CARLA</div>
<h1 style="font-size:64px">Semana de Black Friday no armazém. <em>A Carla não caiu. Mas ficou a doer.</em></h1><div class="swipe">DESLIZE ▶▶</div></div>''')
A.append(boxes()+'''<div class="wrap"><div class="lab">PASSO 1 · O CONFLITO</div><h1>Caixas e mais <em>caixas.</em></h1>
<p>A Black Friday é na sexta e as encomendas não param. A meio do turno, a Carla levantou uma caixa e sentiu uma dor forte nas costas. <b>Não houve queda nem testemunhas.</b></p>
<div class="label"><div><b>ENCOMENDA 27/11</b><br>PESO: 18&nbsp;KG · TURNO: 14H–22H</div><div style="margin-left:auto">'''+barcode(200,80)+'''</div></div></div>''')
A.append(boxes()+'''<div class="wrap"><div class="lab">PASSO 2 · O ERRO</div><div class="bubble">“Não caí e ninguém viu. Isto não é acidente de trabalho.”</div>
<div class="x"><i>✖</i>É o que muita gente pensa.</div><p>E continua a trabalhar com dores, <b>sem dizer nada a ninguém.</b></p></div>''')
A.append(boxes(op=.1)+'''<div class="wrap"><div class="lab">PASSO 3 · A REGRA</div><h1>No local e no horário: <em>presume-se.</em></h1>
<p>Se a lesão é constatada no local e no tempo de trabalho, a lei presume que resulta de acidente de trabalho. <b>Quem disser que não foi do trabalho é que tem de o provar.</b></p>
<div class="law">Lei n.º 98/2009, art. 10.º, n.º 1</div></div>''')
A.append(boxes(op=.1)+'''<div class="wrap"><div class="lab">PASSO 4 · ATENÇÃO</div><h1>O tempo <em>conta.</em></h1>
<div class="warn">Se a lesão só se manifestar mais tarde, <b>a prova passa a ser sua:</b> tem de mostrar que veio do acidente.</div>
<p>Avise logo a chefia, peça que fique registado e vá ao médico no mesmo dia.</p><div class="law">Lei n.º 98/2009, art. 10.º, n.º 2</div></div>''')
A.append(f'''<div class="tape" style="top:150px">FRÁGIL · MANUSEAR COM CUIDADO · FRÁGIL</div><div class="wrap" style="top:240px"><div class="badge"><div class="ph" style="background-image:url(file://{F}lesao-mulher-palete.jpg)"></div><div><div class="n">CARLA</div><div class="r">ARMAZÉM · TURNO DA TARDE<br>SINISTRADA</div><div style="margin-top:14px">{barcode(260,50)}</div></div></div>
<div class="lab" style="margin-top:44px">O DIREITO DELA</div><h1 style="font-size:58px">A Carla foi tratada como sinistrada. <em>Era isso que a lei lhe dava.</em></h1>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''')
for i,b in enumerate(A,1): P[f'1230-carrossel-{i}']=doc(BOX,b+hud(i,AA)+FOOT)
# ================= CARROSSEL B — Daniela / Natal / incumprimento art. 41.º RGPTC =================
XM=""":root{--a1:#e3c167;--a2:#ff8a8a}
.sticker{background:#c8414b;color:#fff;border:4px solid #e3c167}
.cal{margin-top:34px;display:flex;gap:22px}
.cal div{width:200px;border-radius:14px;overflow:hidden;background:#f3eefc;color:#0f1f3d;text-align:center}
.cal div span{display:block;background:#c8414b;color:#fff;font-family:Mono;font-size:24px;padding:8px;letter-spacing:3px}
.cal div b{display:block;font-family:AB;font-size:80px;padding:6px 0}
.cal div i{display:block;font-style:normal;font-family:Mono;font-size:22px;padding-bottom:12px}"""
def lights(top=0,h=1350,op=1):
    cols=['#e3c167','#ff8a8a','#7fd1a8','#e3c167','#8ec5ff']
    pts=[]; r=''
    import math
    for i in range(0,1100,10): pts.append(f'{i},{top+40+28*math.sin(i/170)}')
    r+=f'<polyline points="{" ".join(pts)}" fill="none" stroke="#b9c3dc" stroke-width="2" opacity=".6"/>'
    for k,i in enumerate(range(30,1080,75)):
        y=top+40+28*math.sin(i/170)+16; c=cols[k%5]
        r+=f'<circle cx="{i}" cy="{y}" r="22" fill="{c}" opacity=".18"/><ellipse cx="{i}" cy="{y}" rx="9" ry="13" fill="{c}"/>'
    return f'<div class="deco" style="opacity:{op}"><svg width="1080" height="{h}">{r}</svg></div>'
def snow(h=1350):
    import random; random.seed(h); r=''.join(f'<circle cx="{random.randint(0,1080)}" cy="{random.randint(150,h)}" r="{random.choice([2,3,4])}" fill="#fff" opacity="{random.choice([.15,.25,.35])}"/>' for _ in range(70))
    return f'<div class="deco"><svg width="1080" height="{h}">{r}</svg></div>'
BA='★ FAMÍLIA'
BL=[]
BL.append(photo('natal-mae-filha-cama2.jpg','40% 25%')+'''<div class="bottom"><div class="sticker">NATAL · 25 DEZ</div><div class="lab">A HISTÓRIA DA DANIELA</div>
<h1 style="font-size:62px">Este ano, o Natal é com a mãe. <em>O pai diz que não entrega a filha.</em></h1><div class="swipe">DESLIZE ▶▶</div></div>''')
BL.append(snow()+lights(110,op=.9)+'''<div class="wrap" style="top:220px"><div class="lab">PASSO 1 · O CONFLITO</div><h1>Está no <em>acordo.</em></h1>
<p>A Daniela e o ex-marido têm um acordo de responsabilidades parentais, homologado em tribunal. O Natal é alternado e este ano é dela. <b>Ele já avisou que a filha fica com ele.</b></p>
<div class="cal"><div><span>DEZ</span><b>24</b><i>COM A MÃE</i></div><div><span>DEZ</span><b>25</b><i>COM A MÃE</i></div></div></div>''')
BL.append(snow()+lights(110,op=.9)+'''<div class="wrap" style="top:220px"><div class="lab">PASSO 2 · O ERRO</div><div class="bubble">“Se ele não entregar a menina, não há nada a fazer.”</div>
<div class="x"><i>✖</i>É o que muita gente pensa.</div><p>Um acordo homologado não é um conselho. <b>É para cumprir.</b></p></div>''')
BL.append(snow()+lights(110,op=.5)+'''<div class="wrap" style="top:220px"><div class="lab">PASSO 3 · A REGRA</div><h1>Não cumprir <em>tem custos.</em></h1>
<p>Se um dos pais não cumprir o acordado, o outro pode pedir ao tribunal que faça cumprir o acordo. <b>Pode haver multa até 20&nbsp;UC e indemnização.</b></p>
<div class="law">Lei n.º 141/2015 (RGPTC), art. 41.º, n.º 1</div></div>''')
BL.append(snow()+lights(110,op=.5)+'''<div class="wrap" style="top:220px"><div class="lab">PASSO 4 · ATENÇÃO</div><h1>Prova, <em>sem guerra.</em></h1>
<div class="warn">Não vá buscar a criança à força nem a ponha no meio da discussão. <b>Guarde o acordo e as mensagens</b> em que ele recusa a entrega.</div>
<p>Quanto mais cedo agir, mais tempo há para o tribunal decidir.</p></div>''')
BL.append(photo('natal-mae-filha-cama.jpg','40% 20%')+lights(80,op=.8)+'''<div class="bottom"><div class="lab">O DIREITO DELA</div>
<h1 style="font-size:56px">A Daniela fez valer o acordo. <em>Este Natal, a filha passou-o com a mãe.</em></h1>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''')
for i,b in enumerate(BL,1): P[f'2000-carrossel-{i}']=doc(XM,b+hud(i,BA)+FOOT)
# ================= IMAGEM 10h30 — Pode ou não pode (legítima) =================
HER=""":root{--a1:#e3c167;--a2:#f1d9a8}"""
P['1030-imagem']=doc(HER,'''<div class="photo" style="background-image:url(file://'''+F+'''legitima-mae-filha-abraco.jpg);background-position:center 35%;height:700px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:400px;height:320px;background:linear-gradient(to bottom,rgba(19,38,76,0),#13264c)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:34px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">PODE OU NÃO PODE?</div>
<div style="position:absolute;top:56px;right:70px;z-index:5;font-family:Mono;font-size:26px;color:#0f1f3d;background:#f1d9a8;padding:8px 16px;transform:rotate(3deg)">HERANÇAS</div>
<div style="position:absolute;left:80px;right:80px;top:600px;z-index:3">
<h1 style="font-size:56px">Posso deixar a casa toda só a uma das minhas filhas?</h1>
<div style="font-family:AB;font-size:96px;color:#e3c167;margin-top:14px">DEPENDE.</div>
<p style="font-size:33px;margin-top:8px">Com dois ou mais filhos, dois terços da herança são deles por lei: a legítima. <b>A casa só vai toda para uma filha se couber no terço que sobra.</b></p>
<div class="law">Código Civil, arts. 2156.º e 2159.º</div></div>'''+FOOT)
# ================= IMAGEM 18h00 — O Advogado comenta (álcool) =================
RD=""":root{--a1:#e3c167;--a2:#8ec5ff}"""
P['1800-imagem']=doc(RD,'''<div class="photo" style="background-image:url(file://'''+F+'''alcool-mulher-conduz-reflexo.jpg);background-position:center 45%;height:700px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:400px;height:320px;background:linear-gradient(to bottom,rgba(19,38,76,0),#13264c)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:34px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">O ADVOGADO COMENTA</div>
<div style="position:absolute;top:56px;right:70px;z-index:5;font-family:Mono;font-size:26px;color:#0f1f3d;background:#8ec5ff;padding:8px 16px;transform:rotate(3deg)">GNR + PSP · 21 NOV</div>
<div style="position:absolute;left:80px;right:80px;top:590px;z-index:3">
<div style="display:flex;align-items:baseline;gap:22px"><span style="font-family:AB;font-size:150px;color:#e3c167;line-height:1">333</span><span style="font-family:AB;font-size:44px;line-height:1.15">detidos por álcool ao volante numa semana.</span></div>
<p style="font-size:33px;margin-top:22px">E quem pensa em recusar o teste deve saber: <b>recusar é crime de desobediência.</b> Nos jantares de Natal, quem bebe não conduz.</p>
<div class="law">Código da Estrada, art. 152.º, n.ºs 1 e 3</div></div>'''+FOOT)
# ================= STORIES =================
SF='<div style="position:absolute;left:0;right:0;bottom:250px;text-align:center;font-size:26px;letter-spacing:2px;color:#b9c3dc;z-index:5;font-weight:600">@mcg.advogado · Miguel Costa Gomes · Advogado</div>'
def story(css,deco,inner,ph=None,pos='center'):
    bg=(f'<div class="photo" style="background-image:url(file://{F}{ph});background-position:{pos}"></div><div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,31,61,.2) 0%,rgba(15,31,61,.1) 30%,rgba(15,31,61,.85) 58%,#0f1f3d 78%)"></div>' if ph else '')
    return doc(css,bg+deco+f'<div style="position:absolute;left:90px;right:90px;top:250px;bottom:340px;display:flex;flex-direction:column;justify-content:{"flex-end" if ph else "center"};z-index:3">{inner}</div>'+SF,1920)
VF='<div style="font-family:AB;font-size:50px;color:#0f1f3d;background:#e3c167;align-self:flex-start;padding:10px 24px">VERDADEIRO OU FALSO?</div>'
P['0700-story-1']=story(BOX,boxes(1920),'''<div class="sticker" style="align-self:flex-start">BLACK FRIDAY · 27 NOV</div><h1 style="font-size:80px">Semana de Black Friday. Nos armazéns, ninguém para.</h1><p style="font-size:44px;text-align:left">Uma dor nas costas a meio do turno. É acidente de trabalho?</p>''')
P['0700-story-2']=story(BOX,boxes(1920),VF+'''<h1 style="font-size:80px;margin-top:50px">“Se não caí e ninguém viu, não é acidente de trabalho.”</h1>''')
P['0700-story-3']=story(BOX,boxes(1920),'''<div style="font-family:AB;font-size:130px;color:#ff9f43">FALSO.</div><p style="font-size:46px;text-align:left">A lesão constatada no local e no tempo de trabalho <b>presume-se consequência de acidente de trabalho.</b></p><div class="law" style="font-size:30px">Lei n.º 98/2009, art. 10.º, n.º 1</div>''')
P['1500-story-1']=story(XM,snow(1920)+lights(260,1920),'''<div class="sticker" style="align-self:flex-start">NATAL · 25 DEZ</div><h1 style="font-size:80px">Pais separados. O acordo diz que o Natal é seu. <em>E o outro não cumpre.</em></h1>''')
P['1500-story-2']=story(XM,snow(1920)+lights(260,1920),VF+'''<h1 style="font-size:80px;margin-top:50px">“Se o pai não entregar a filha no Natal, não há nada a fazer.”</h1>''')
P['1500-story-3']=story(XM,snow(1920)+lights(260,1920),'''<div style="font-family:AB;font-size:130px;color:#ff8a8a">FALSO.</div><p style="font-size:46px;text-align:left">O outro progenitor pode pedir ao tribunal que faça cumprir o acordo. <b>Pode haver multa até 20&nbsp;UC e indemnização.</b></p><div class="law" style="font-size:30px">Lei n.º 141/2015 (RGPTC), art. 41.º, n.º 1</div>''')
P['2100-story']=story(BOX,'','''<div class="sticker" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><h1 style="font-size:76px">Dor nas costas a meio do turno? <em>Pode ser acidente de trabalho.</em></h1><p style="font-size:42px;text-align:left">Veja a história da Carla no post de hoje. Deixe a sua dúvida nos comentários do post.</p>''','lesao-mulher-armazem-caixas.jpg','70% center')
CX=""":root{--a1:#e3c167;--a2:#e3c167}"""
QM='<div class="deco"><svg width="1080" height="1920">'+''.join(f'<text x="{x}" y="{y}" font-family="AB" font-size="{s}" fill="#e3c167" opacity="{o}">?</text>' for x,y,s,o in [(760,520,260,.18),(120,1500,200,.12),(850,1380,140,.2),(60,700,120,.1)])+'</svg></div>'
P['2130-story-caixinha']=story(CX,QM,'''<div style="font-family:AB;font-size:34px;color:#0f1f3d;background:#e3c167;align-self:flex-start;padding:10px 22px;letter-spacing:1px">CAIXINHA DE PERGUNTAS</div><h1 style="font-size:96px;margin-top:40px">Caixinha de <em>perguntas</em></h1><p style="font-size:46px;text-align:left">Tem uma dúvida sobre os seus direitos? Escreva-a nos comentários da publicação das 20h00 de hoje. <b>As melhores têm resposta no domingo.</b></p>''')
P['2200-story']=story(XM,lights(260,1920,.8),'''<div class="sticker" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><h1 style="font-size:76px">O acordo diz que o Natal é seu? <em>É para cumprir.</em></h1><p style="font-size:42px;text-align:left">Veja a história da Daniela no post de hoje. Deixe a sua dúvida nos comentários do post.</p>''','natal-mae-filha-chao.jpg','55% center')
os.makedirs(OUT,exist_ok=True); os.makedirs(B,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
    pg=b.new_page()
    for k,h in P.items():
        H=1920 if 'story' in k else 1350
        pg.set_viewport_size({'width':1080,'height':H})
        fn=B+k+'.html'; open(fn,'w').write(h); pg.goto('file://'+fn); pg.wait_for_timeout(600)
        pg.screenshot(path=B+k+'.png'); Image.open(B+k+'.png').convert('RGB').save(OUT+k+'.jpg',quality=92)
    b.close()
print('ok',len(P))
