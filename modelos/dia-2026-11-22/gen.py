import os
from playwright.sync_api import sync_playwright
from PIL import Image
R='/home/claude/mcg-imagens'; F=R+'/fotos/'; OUT=R+'/2026-11-22/'; B='/home/claude/build/d22/'
G='/usr/share/fonts/truetype/google-fonts/ofl/'; PF='/home/claude/fonts/package/files/'
BASE=f"""
@font-face{{font-family:AB;src:url(file://{G}archivoblack/ArchivoBlack-Regular.ttf)}}
@font-face{{font-family:Mono;src:url(file://{G}anonymouspro/AnonymousPro-Bold.ttf)}}
@font-face{{font-family:PF;src:url(file://{PF}playfair-display-latin-400-normal.woff2);font-weight:400}}
@font-face{{font-family:PF;src:url(file://{PF}playfair-display-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:PF;src:url(file://{PF}playfair-display-latin-400-italic.woff2);font-style:italic}}
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
# ================= CARROSSEL A — Joana / PERSI (Euribor) =================
BANK=""":root{--a1:#5fd3e6;--a2:#5fd3e6}
.sticker{background:#ff7a6b;color:#0f1f3d;border:4px solid #fff}"""
def chart(h=1350,op=.5):
    o=1210 if h==1350 else 1570
    ys=[0,-18,-10,-45,-38,-75,-85,-110,-130]
    pts=' '.join(f"{60+120*i},{o+y}" for i,y in enumerate(ys))
    grid=''.join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}" stroke="#5fd3e6" stroke-width="1" opacity=".10"/>' for y in range(160,h,90))
    return f'<div class="deco"><svg width="1080" height="{h}">{grid}<polyline points="{pts}" fill="none" stroke="#ff7a6b" stroke-width="5" opacity="{op}"/><circle cx="1020" cy="{o-130}" r="10" fill="#ff7a6b" opacity="{op}"/></svg></div>'
AA='▲ PERGUNTA DA SEMANA'
CAL='''<svg width="760" height="190" viewBox="0 0 760 190" style="margin-top:40px;align-self:center"><rect x="10" y="40" width="740" height="12" rx="6" fill="rgba(95,211,230,.25)"/><rect x="250" y="40" width="250" height="12" rx="6" fill="#e3c167"/>
<circle cx="20" cy="46" r="16" fill="#ff7a6b"/><text x="6" y="110" text-anchor="start" font-family="Mono" font-size="28" fill="#ff7a6b">DIA 1</text>
<text x="375" y="110" text-anchor="middle" font-family="Mono" font-size="28" fill="#e3c167">DIA 31 A 60</text><text x="375" y="150" text-anchor="middle" font-family="Mono" font-size="24" fill="#f3eefc">ENTRA NO PERSI</text>
<text x="740" y="110" text-anchor="end" font-family="Mono" font-size="28" fill="#5fd3e6">TRIBUNAL?</text><text x="740" y="150" text-anchor="end" font-family="Mono" font-size="24" fill="#f3eefc">AINDA NÃO</text></svg>'''
A=[]
A.append(photo('persi-mulher-carta-cozinha.jpg','30% center')+'''<div class="bottom"><div class="sticker">EURIBOR · 20 NOV</div><div class="lab">PERGUNTA DA SEMANA</div>
<h1 style="font-size:62px">A Joana falhou uma prestação da casa. <em>A carta do banco trouxe uma boa notícia.</em></h1><div class="swipe">DESLIZE ▶▶</div></div>''')
A.append(chart()+'''<div class="wrap"><div class="lab">PASSO 1 · O CONFLITO</div><h1>217&nbsp;€ <em>só de juros.</em></h1>
<p>É quanto leva hoje, em média, a prestação da casa, diz o INE. Em novembro a Joana não conseguiu pagar tudo. <b>E ficou com medo do banco.</b></p></div>''')
A.append(chart()+'''<div class="wrap"><div class="lab">PASSO 2 · O ERRO</div><div class="bubble">“Falhei uma prestação. O banco vai pôr-me logo em tribunal.”</div>
<div class="x"><i>✖</i>É o que muita gente pensa.</div><p>Antes disso, a lei obriga o banco a <b>tentar um acordo consigo.</b></p></div>''')
A.append(chart(op=.25)+f'''<div class="wrap"><div class="lab">PASSO 3 · A REGRA</div><h1>Primeiro, <em>o PERSI.</em></h1>
<p style="margin-top:20px">Entre o 31.º e o 60.º dia de atraso, o banco tem de abrir consigo uma negociação: o PERSI. <b>Enquanto durar, não pode pôr ação em tribunal.</b></p>{CAL}<div class="law">DL n.º 227/2012, arts. 14.º, n.º 1, e 18.º, n.º 1</div></div>''')
A.append(chart(op=.25)+'''<div class="wrap"><div class="lab">PASSO 4 · ATENÇÃO</div><h1>Não fique <em>calada.</em></h1>
<div class="warn">O banco tem de a avisar por escrito, em <b>5&nbsp;dias</b>, de que entrou no PERSI. Responda, mostre as suas contas e proponha o que consegue pagar.</div>
<p>Guarde todas as cartas e todos os e-mails.</p><div class="law">DL n.º 227/2012, art. 14.º, n.º 4</div></div>''')
A.append(photo('persi-mulher-abraca-papeis.jpg','35% center')+'''<div class="bottom"><div class="lab">RESPOSTA</div>
<h1>A Joana negociou com o banco. <em>Tinha direito a isso antes de qualquer processo.</em></h1>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''')
for i,b in enumerate(A,1): P[f'1230-carrossel-{i}']=doc(BANK,b+hud(i,AA)+FOOT)
# ================= CARROSSEL B — Património / Teresa / herança europeia =================
PAT=""":root{--a1:#e3c167;--a2:#e3c167}
.selo{position:absolute;top:56px;left:0;right:0;text-align:center;z-index:6;font-family:Inter;font-weight:600;font-size:24px;letter-spacing:12px;color:#e3c167}
.selo:before,.selo:after{content:'';display:inline-block;width:90px;height:1px;background:#e3c167;vertical-align:middle;margin:0 24px}
.pn{position:absolute;top:104px;left:0;right:0;text-align:center;z-index:6;font-family:PF;font-style:italic;font-size:24px;color:#b9c3dc}
.frame{position:absolute;inset:34px;border:1px solid rgba(227,193,103,.45);z-index:2;pointer-events:none}
.pw{position:absolute;left:120px;right:120px;top:200px;bottom:190px;display:flex;flex-direction:column;justify-content:center;z-index:3}
.k{font-family:Inter;font-weight:600;font-size:24px;letter-spacing:6px;color:#e3c167}
.t{font-family:PF;font-weight:400;font-size:66px;line-height:1.15;color:#fff;margin-top:26px}
.t i{color:#e3c167}
.rule{width:120px;height:1px;background:#e3c167;margin:40px 0}
.b{font-size:36px;line-height:1.55;color:#e6e9f2;text-align:justify;hyphens:none}
.q{font-family:PF;font-style:italic;font-size:50px;line-height:1.3;color:#fff}
.ref{margin-top:44px;font-family:Inter;font-size:24px;letter-spacing:2px;color:#e3c167;border-top:1px solid rgba(227,193,103,.6);padding-top:16px;align-self:flex-start}
.tag{display:inline-block;font-family:Inter;font-weight:600;font-size:24px;letter-spacing:5px;color:#0f1f3d;background:#e3c167;padding:10px 20px;margin-bottom:22px}
.pbottom{position:absolute;left:110px;right:110px;bottom:140px;z-index:3}
.pshade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,31,61,.55) 0%,rgba(15,31,61,.05) 25%,rgba(15,31,61,.75) 55%,#0f1f3d 80%)}"""
def pslide(n,inner,ph=None,pos='center'):
    bg=f'<div class="photo" style="background-image:url(file://{F}{ph});background-position:{pos}"></div><div class="pshade"></div>' if ph else ''
    return bg+'<div class="frame"></div><div class="selo">PATRIMÓNIO</div>'+f'<div class="pn">{n} / 6</div>'+inner
BP=[]
BP.append(pslide(1,'''<div class="pbottom"><div class="tag">HERANÇAS · ESPANHA · 20 NOV</div><div class="k" style="margin-top:6px">A HISTÓRIA DA TERESA</div>
<div class="t" style="font-size:64px">Uma herança em dois países. <i>Que lei manda?</i></div></div>''','heranca-ue-mulher-blazer.jpg','60% center'))
BP.append(pslide(2,'''<div class="pw"><div class="k">O CONFLITO</div><div class="t">Um apartamento lá fora. <i>Uma quinta em Portugal.</i></div><div class="rule"></div>
<div class="b">O pai da Teresa vivia há trinta anos noutro país da União Europeia. Deixou lá a casa e uma conta. Cá, a quinta da família.</div></div>'''))
BP.append(pslide(3,'''<div class="pw"><div class="k">O ERRO COMUM</div><div class="rule" style="margin-top:30px"></div>
<div class="q">«A quinta é em Portugal. A herança segue a lei portuguesa.»</div><div class="rule"></div>
<div class="b">Esta semana, em Espanha, uma herança de estrangeiros parou no registo por causa da lei escolhida. <i style="color:#e3c167">A lei aplicável não é um pormenor.</i></div></div>'''))
BP.append(pslide(4,'''<div class="pw"><div class="k">A REGRA</div><div class="t">Conta o país onde <i>vivia.</i></div><div class="rule"></div>
<div class="b">Em regra, toda a herança segue a lei do país onde a pessoa tinha residência habitual quando morreu. E são os tribunais desse país que, em regra, decidem a herança.</div>
<div class="ref">REGULAMENTO (UE) N.º 650/2012, ARTS. 4.º E 21.º, N.º 1</div></div>'''))
BP.append(pslide(5,'''<div class="pw"><div class="k">ATENÇÃO</div><div class="t">Pode decidir <i>em vida.</i></div><div class="rule"></div>
<div class="b">Quem tem nacionalidade portuguesa pode escolher que seja a lei portuguesa a regular toda a sucessão. É uma decisão a tomar com tempo.</div>
<div class="ref">REGULAMENTO (UE) N.º 650/2012, ART. 22.º, N.º 1</div></div>'''))
BP.append(pslide(6,'''<div class="pbottom"><div class="k">O DIREITO DELA</div><div class="t" style="font-size:56px">A Teresa soube a tempo que lei se aplicava. <i>Nada ficou ao acaso.</i></div>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''','heranca-ue-mulher-mala.jpg','55% center'))
for i,b in enumerate(BP,1): P[f'2000-carrossel-{i}']=doc(PAT,b+FOOT)
# ================= IMAGEM 10h30 — Pode ou não pode (imagem de menores) =================
SCH=""":root{--a1:#e3c167;--a2:#ffb3c7}"""
POLA='<div class="deco"><div style="position:absolute;right:70px;top:560px;width:150px;height:170px;background:#f3eefc;transform:rotate(8deg);padding:12px 12px 40px;box-shadow:0 10px 20px rgba(0,0,0,.3)"><div style="width:100%;height:100%;background:#172d5e;display:flex;align-items:center;justify-content:center;font-family:AB;font-size:60px;color:#ffb3c7">?</div></div></div>'
P['1030-imagem']=doc(SCH,'''<div class="photo" style="background-image:url(file://'''+F+'''imagem-mae-fotografa-filha.jpg);background-position:center 30%;height:720px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:420px;height:320px;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d)"></div>'''+POLA+'''
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:34px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">PODE OU NÃO PODE?</div>
<div style="position:absolute;top:56px;right:70px;z-index:5;font-family:Mono;font-size:26px;color:#0f1f3d;background:#ffb3c7;padding:8px 16px;transform:rotate(3deg)">FESTAS DE NATAL</div>
<div style="position:absolute;left:80px;right:80px;top:640px;z-index:3">
<h1 style="font-size:56px;padding-right:150px">A escola pode pôr fotos da minha filha nas redes sociais sem me perguntar?</h1>
<div style="font-family:AB;font-size:96px;color:#e3c167;margin-top:18px">NÃO PODE.</div>
<p style="font-size:33px;margin-top:10px">O retrato de uma pessoa não pode ser exposto sem o consentimento dela. Sendo menor, quem autoriza são <b>os pais.</b></p>
<div class="law">Código Civil, art. 79.º, n.º 1</div></div>'''+FOOT)
# ================= IMAGEM 18h00 — Mito vs Facto (alimentos aos pais) =================
FAM=""":root{--a1:#e3c167;--a2:#f1d9a8}"""
P['1800-imagem']=doc(FAM,'''<div class="photo" style="background-image:url(file://'''+F+'''pais-idosos-maos.jpg);background-position:center 40%;height:680px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:380px;height:320px;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:34px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">MITO VS. FACTO</div>
<div style="position:absolute;left:80px;right:80px;top:600px;z-index:3">
<div style="display:flex;align-items:center;gap:20px"><span style="font-family:AB;font-size:34px;color:#ff7a6b;border:3px solid #ff7a6b;padding:4px 14px">MITO</span><span style="font-size:36px;text-decoration:line-through;color:#b9c3dc">“Os filhos não têm obrigação nenhuma para com os pais.”</span></div>
<div style="font-family:AB;font-size:34px;color:#0f1f3d;background:#e3c167;padding:6px 16px;display:inline-block;margin-top:44px">FACTO</div>
<h1 style="font-size:58px">Se os pais precisarem, os filhos podem ter de lhes <em>prestar alimentos.</em></h1>
<p style="font-size:33px">Na lei, os filhos vêm logo a seguir ao cônjuge na lista de quem deve ajudar.</p>
<div class="law">Código Civil, art. 2009.º, n.º 1</div></div>'''+FOOT)
# ================= STORIES =================
SF='<div style="position:absolute;left:0;right:0;bottom:250px;text-align:center;font-size:26px;letter-spacing:2px;color:#b9c3dc;z-index:5;font-weight:600">@mcg.advogado · Miguel Costa Gomes · Advogado</div>'
def story(css,deco,inner,ph=None,pos='center'):
    bg=(f'<div class="photo" style="background-image:url(file://{F}{ph});background-position:{pos}"></div><div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,31,61,.2) 0%,rgba(15,31,61,.1) 30%,rgba(15,31,61,.85) 58%,#0f1f3d 78%)"></div>' if ph else '')
    return doc(css,bg+deco+f'<div style="position:absolute;left:90px;right:90px;top:250px;bottom:340px;display:flex;flex-direction:column;justify-content:{"flex-end" if ph else "center"};z-index:3">{inner}</div>'+SF,1920)
VF='<div style="font-family:AB;font-size:50px;color:#0f1f3d;background:#e3c167;align-self:flex-start;padding:10px 24px">VERDADEIRO OU FALSO?</div>'
P['0700-story-1']=story(BANK,chart(1920),'''<div class="sticker" style="align-self:flex-start">EURIBOR · 20 NOV</div><h1 style="font-size:80px">A Euribor a 6 meses chegou aos 3,071%.</h1><p style="font-size:44px;text-align:left">A prestação da casa sobe. E se um mês não der para pagar?</p>''')
P['0700-story-2']=story(BANK,chart(1920),VF+'''<h1 style="font-size:80px;margin-top:50px">“Se falhar uma prestação, o banco pode pôr-me logo em tribunal.”</h1>''')
P['0700-story-3']=story(BANK,chart(1920),'''<div style="font-family:AB;font-size:130px;color:#ff7a6b">FALSO.</div><p style="font-size:46px;text-align:left">Entre o 31.º e o 60.º dia de atraso, o banco tem de a integrar no PERSI. <b>Enquanto durar, não pode pôr ação em tribunal.</b></p><div class="law" style="font-size:30px">DL n.º 227/2012, arts. 14.º e 18.º</div>''')
PS='<div class="frame"></div><div class="selo" style="top:150px">PATRIMÓNIO</div>'
P['1500-story-1']=story(PAT,PS,'''<div class="tag" style="align-self:flex-start">HERANÇAS SEM FRONTEIRAS</div><div class="t" style="font-size:80px">Uma casa em Portugal. Uma conta lá fora. <i>Que lei se aplica à herança?</i></div>''')
P['1500-story-2']=story(PAT,PS,VF+'''<div class="q" style="font-size:72px;margin-top:60px">«Se a casa é em Portugal, a herança segue sempre a lei portuguesa.»</div>''')
P['1500-story-3']=story(PAT,PS,'''<div class="t" style="font-size:120px;color:#e3c167">Falso.</div><div class="b" style="font-size:46px;margin-top:30px">Em regra, toda a herança segue a lei do país onde a pessoa tinha residência habitual quando morreu.</div><div class="ref">REGULAMENTO (UE) N.º 650/2012, ART. 21.º, N.º 1</div>''')
P['2100-story']=story(BANK,'','''<div class="sticker" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><h1 style="font-size:76px">Falhou uma prestação da casa? <em>O banco não pode ir logo para tribunal.</em></h1><p style="font-size:42px;text-align:left">Veja a história da Joana no post de hoje. Deixe a sua dúvida nos comentários do post.</p>''','persi-mulher-mesa-pequeno-almoco.jpg','30% center')
P['2200-story']=story(PAT,'<div class="selo" style="top:150px">PATRIMÓNIO</div>','''<div class="tag" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><div class="t" style="font-size:76px">Herança com bens em dois países. <i>Qual é a lei que manda?</i></div><div class="b" style="font-size:42px;margin-top:24px;text-align:left">A história da Teresa está no post de hoje. Deixe a sua dúvida nos comentários do post.</div>''','heranca-ue-mulher-documentos.jpg','40% center')
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
