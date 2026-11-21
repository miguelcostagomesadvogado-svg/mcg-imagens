import os
from playwright.sync_api import sync_playwright
from PIL import Image
R='/home/claude/mcg-imagens'; F=R+'/fotos/'; OUT=R+'/2026-11-21/'
G='/usr/share/fonts/truetype/google-fonts/ofl/'
BASE=f"""
@font-face{{font-family:AB;src:url(file://{G}archivoblack/ArchivoBlack-Regular.ttf)}}
@font-face{{font-family:Mono;src:url(file://{G}anonymouspro/AnonymousPro-Bold.ttf)}}
@font-face{{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-Regular.otf);font-weight:400}}
@font-face{{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-SemiBold.otf);font-weight:600}}
@font-face{{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-Bold.otf);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;background:linear-gradient(170deg,#0f1f3d 0%,#14295a 100%);font-family:Inter;color:#f3eefc;position:relative;overflow:hidden}}
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
.card{{margin-top:34px;border:3px solid var(--a2);border-radius:6px;padding:28px 34px;background:rgba(241,230,200,.06);font-family:Mono;font-size:33px;line-height:1.7}}
.card span{{color:var(--a2)}} .card strong{{color:#e3c167}}
.bubble{{margin-top:34px;background:#fff;color:#0f1f3d;border-radius:26px;padding:36px 40px;font-family:AB;font-size:50px;line-height:1.18;position:relative}}
.bubble:after{{content:'';position:absolute;left:70px;bottom:-34px;border:18px solid transparent;border-top:20px solid #fff;border-left:22px solid #fff}}
.x{{margin-top:56px;display:flex;align-items:center;gap:22px;font-family:AB;font-size:46px;color:#ff6b5e}}
.x i{{font-style:normal;width:74px;height:74px;border:4px solid #ff6b5e;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:52px}}
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
# ---------- universos ----------
GAL=""":root{--a1:#e3c167;--a2:#f1e6c8}
.sticker{background:#c0392b;color:#fff;border:4px solid #f1e6c8;box-shadow:0 8px 0 rgba(0,0,0,.25)}
.spot{position:absolute;width:700px;height:900px;top:-200px;left:190px;background:radial-gradient(ellipse at top,rgba(241,230,200,.16),transparent 62%)}"""
GALDECO='<div class="deco"><div class="spot"></div><svg width="1080" height="1350" style="position:absolute;inset:0"><rect x="22" y="22" width="1036" height="1306" fill="none" stroke="#e3c167" stroke-width="3" opacity=".55"/><rect x="34" y="34" width="1012" height="1282" fill="none" stroke="#e3c167" stroke-width="1" opacity=".4"/></svg></div>'
RAIN=""":root{--a1:#ff9a3c;--a2:#8fd3ff}
.sticker{background:#ff8a1f;color:#0f1f3d;border:4px solid #fff}"""
def raindeco(h=1350):
    import random; random.seed(7)
    ls=''.join(f'<line x1="{x}" y1="{y}" x2="{x-14}" y2="{y+46}" stroke="#8fd3ff" stroke-width="2.4" opacity="{o}"/>' for x,y,o in [(random.randint(0,1100),random.randint(-40,h),random.choice([.18,.25,.35])) for _ in range(110)])
    return f'<div class="deco"><svg width="1080" height="{h}">{ls}</svg></div>'
PKG=""":root{--a1:#e3c167;--a2:#f1d9a8}"""
FORA=""":root{--a1:#e3c167;--a2:#9fd0ff}"""
FOOT='<div style="position:absolute;left:0;right:0;bottom:0;height:120px;background:linear-gradient(to top,#0f1f3d 55%,rgba(15,31,61,0));z-index:4"></div><div class="foot"><span>MIGUEL COSTA GOMES · ADVOGADO</span><span>@MCG.ADVOGADO</span></div>'
def hud(n,area):
    bars=''.join(f'<i class="{"on" if k<=n else ""}"></i>' for k in range(1,7))
    return f'<div class="hud"><span>{area}</span><span class="lv">{n}/6<span class="bar">{bars}</span></span></div>'
def doc(css,body,h=1350):
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE}{css} body{{height:{h}px}}</style></head><body>{body}</body></html>'
def photo(f,pos='center'):
    return f'<div class="photo" style="background-image:url(file://{F}{f});background-position:{pos}"></div><div class="shade"></div>'
CONTACT='''<div class="contact"><b>Miguel Costa Gomes</b> · Advogado · C.P. 11209P<br>miguelcostagomes-11209P@adv.oa.pt · +351 960 225 890</div>'''
P={}
# ================= CARROSSEL A — Clara / arte falsa (penal) =================
AA='▣ UMA HISTÓRIA · PENAL'
FRAME='''<svg width="380" height="300" viewBox="0 0 380 300" style="margin-top:44px;align-self:center"><rect x="10" y="10" width="360" height="280" fill="none" stroke="#e3c167" stroke-width="16"/><rect x="34" y="34" width="312" height="232" fill="rgba(241,230,200,.08)" stroke="#e3c167" stroke-width="3"/><text x="190" y="190" text-anchor="middle" font-family="AB" font-size="140" fill="#f1e6c8">?</text><g transform="rotate(-14 250 230)"><rect x="170" y="200" width="200" height="64" fill="none" stroke="#e8564b" stroke-width="6"/><text x="270" y="246" text-anchor="middle" font-family="AB" font-size="40" fill="#e8564b">CÓPIA</text></g></svg>'''
A=[]
A.append(photo('falso-mulher-quadro-parede.jpg','center 25%')+'''<div class="bottom"><div class="sticker">ARTE FALSA · 19 NOV</div><div class="lab">A HISTÓRIA DA CLARA</div>
<h1 style="font-size:68px">A PJ apanhou um falsificador de arte. <em>E a Clara olhou para a parede.</em></h1><div class="swipe">DESLIZE ▶▶</div></div>''')
A.append(GALDECO+f'''<div class="wrap"><div class="lab">SALA 1 · O CONFLITO</div><h1>Pagou 2.400&nbsp;€ <em>por um quadro “assinado”.</em></h1>
<p>Comprou-o a um vendedor online, com certificado e tudo. Esta semana pediu uma avaliação. A resposta: <b>é uma cópia.</b></p>{FRAME}</div>''')
A.append(GALDECO+'''<div class="wrap"><div class="lab">SALA 2 · O ERRO</div><div class="bubble">“Foi um mau negócio. Não há nada a fazer.”</div>
<div class="x"><i>✖</i>É o que muita gente pensa.</div><p>Quem engana de propósito para ficar com o seu dinheiro <b>pode estar a cometer um crime.</b></p></div>''')
A.append(GALDECO+'''<div class="wrap"><div class="lab">SALA 3 · A REGRA</div><h1>Enganar para lucrar <em>tem nome: burla.</em></h1>
<div class="card"><span>OBRA&nbsp;&nbsp;&nbsp;&nbsp;</span> cópia<br><span>VENDIDA </span> como original<br><span>CRIME&nbsp;&nbsp;&nbsp;</span> <strong>burla</strong></div>
<p>Na burla simples, o processo só avança <b>se a vítima fizer queixa.</b></p><div class="law">Código Penal, art. 217.º</div></div>''')
A.append(GALDECO+'''<div class="wrap"><div class="lab">SALA 4 · ATENÇÃO</div><h1>A queixa <em>tem prazo.</em></h1>
<div class="warn">São <b>6&nbsp;meses</b> a contar do dia em que soube do engano e de quem o fez. No mesmo processo pode pedir uma indemnização pelo prejuízo.</div>
<p>Guarde o anúncio, as mensagens e o comprovativo do pagamento.</p><div class="law">Código Penal, art. 115.º, n.º 1 · CPP, art. 71.º</div></div>''')
A.append(photo('miguel-cover.jpg','center 20%')+'''<div class="bottom"><div class="lab">FIM DA VISITA</div>
<h1>A Clara fez queixa a tempo. <em>O direito estava do lado dela.</em></h1>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''')
for i,b in enumerate(A,1): P[f'1230-carrossel-{i}']=doc(GAL,b+hud(i,AA)+FOOT)
# ================= CARROSSEL B — Helena / herança (chuva) =================
BB='☂ UMA HISTÓRIA · HERANÇAS'
HOUSE='''<svg width="420" height="300" viewBox="0 0 420 300" style="margin-top:44px;align-self:center"><path d="M40 140 L210 20 L380 140" fill="none" stroke="#e3c167" stroke-width="12" stroke-linejoin="round"/><rect x="80" y="135" width="260" height="150" fill="none" stroke="#e3c167" stroke-width="10"/><rect x="185" y="200" width="50" height="85" fill="#e3c167"/><path d="M150 150 q8 16 0 22 q-8 -6 0 -22z M270 165 q8 16 0 22 q-8 -6 0 -22z M215 120 q8 16 0 22 q-8 -6 0 -22z" fill="#8fd3ff"/><text x="300" y="70" font-family="AB" font-size="54" fill="#ff8a1f">!</text></svg>'''
B=[]
B.append(photo('chuva-mulher-retrato.jpg','center 35%')+'''<div class="bottom"><div class="sticker">AVISO LARANJA · 21 NOV</div><div class="lab">A HISTÓRIA DA HELENA</div>
<h1 style="font-size:66px">Chuva forte em oito distritos. <em>E a casa da herança a meter água.</em></h1><div class="swipe">DESLIZE ▶▶</div></div>''')
B.append(raindeco()+f'''<div class="wrap"><div class="lab">ALERTA 1 · O CONFLITO</div><h1>Seis anos <em>sem partilhas.</em></h1>
<p>A mãe da Helena morreu em 2020. A casa ficou para ela e para os dois irmãos. Ninguém tratou de nada. Hoje, com a chuva, <b>a água entrou pela sala.</b></p>{HOUSE}</div>''')
B.append(raindeco()+'''<div class="wrap"><div class="lab">ALERTA 2 · O ERRO</div><div class="bubble">“Enquanto o meu irmão não quiser, a casa fica assim.”</div>
<div class="x"><i>✖</i>É o que muita gente pensa.</div><p>Ninguém é obrigado a ficar preso a uma herança <b>para sempre.</b></p></div>''')
B.append(raindeco()+'''<div class="wrap"><div class="lab">ALERTA 3 · A REGRA</div><h1>Pode exigir <em>a partilha.</em></h1>
<div class="card"><span>HERDEIROS</span> 3<br><span>ACORDO&nbsp;&nbsp;&nbsp;</span> não há<br><span>DIREITO&nbsp;&nbsp;</span> <strong>pedir a partilha</strong></div>
<p>Qualquer herdeiro pode pedir a partilha quando quiser. <b>Sem acordo, faz-se inventário.</b></p><div class="law">Código Civil, art. 2101.º, n.º 1</div></div>''')
B.append(raindeco()+'''<div class="wrap"><div class="lab">ALERTA 4 · ATENÇÃO</div><h1>Até à partilha, <em>quem administra é o cabeça de casal.</em></h1>
<div class="warn">Avise-o <b>por escrito</b> dos estragos e peça que se trate do telhado.</div>
<p>Fotografe a infiltração hoje e guarde os orçamentos.</p><div class="law">Código Civil, art. 2079.º</div></div>''')
B.append(photo('miguel-cover.jpg','center 20%')+'''<div class="bottom"><div class="lab">DEPOIS DA TEMPESTADE</div>
<h1>A Helena pediu a partilha. <em>A casa deixou de estar parada.</em></h1>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''')
for i,b in enumerate(B,1): P[f'2000-carrossel-{i}']=doc(RAIN,b+hud(i,BB)+FOOT)
# ================= IMAGEM 10h30 — Pode ou não pode =================
TAPE='<div class="deco"><div style="position:absolute;left:-60px;top:250px;width:1300px;height:64px;background:repeating-linear-gradient(90deg,rgba(227,193,103,.9) 0 120px,rgba(227,193,103,.75) 120px 124px);transform:rotate(-6deg);opacity:.9"></div></div>'
P['1030-imagem']=doc(PKG,'''<div class="photo" style="background-image:url(file://'''+F+'''devolve-mulher-cadeira.jpg);background-position:center 30%;height:720px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:420px;height:320px;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:34px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">PODE OU NÃO PODE?</div>
<div style="position:absolute;top:56px;right:70px;z-index:5;font-family:Mono;font-size:26px;color:#0f1f3d;background:#f1d9a8;padding:8px 16px;transform:rotate(3deg)">COMPRAS DE NATAL</div>
<div style="position:absolute;left:80px;right:80px;top:640px;z-index:3">
<h1 style="font-size:58px">Comprei online, chegou há uma semana e já não quero. A loja pode recusar a devolução?</h1>
<div style="font-family:AB;font-size:96px;color:#e3c167;margin-top:18px">NÃO PODE.</div>
<p style="font-size:33px;margin-top:10px">Nas compras à distância tem <b>14&nbsp;dias</b> para desistir, sem dar motivo. Há exceções, como artigos feitos à medida.</p>
<div class="law">DL n.º 24/2014, art. 10.º, n.º 1</div></div>'''+FOOT)
# ================= IMAGEM 18h00 — Portugueses no estrangeiro =================
PLANE='<div class="deco"><svg width="1080" height="1350"><path d="M60 520 C 320 380, 700 420, 1020 260" fill="none" stroke="#9fd0ff" stroke-width="4" stroke-dasharray="14 14" opacity=".6"/><text x="990" y="275" font-size="56" fill="#9fd0ff" transform="rotate(-20 1000 260)">✈</text></svg></div>'
P['1800-imagem']=doc(FORA,'''<div class="photo" style="background-image:url(file://'''+F+'''fora-mulher-telefone-hotel.jpg);background-position:72% center;height:700px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:380px;height:340px;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d)"></div>'''+PLANE+'''
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:32px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">PORTUGUESES NO ESTRANGEIRO</div>
<div style="position:absolute;left:80px;right:80px;top:650px;z-index:3">
<div class="lab" style="color:#9fd0ff">CASA ARRENDADA EM PORTUGAL</div>
<h1 style="font-size:62px">O inquilino deixou de pagar <em>e você vive lá fora?</em></h1>
<p style="font-size:34px">Pode tratar disto <b>sem vir a Portugal.</b> Para estes casos existe o procedimento especial de despejo, e com uma procuração sua o advogado trata de tudo cá.</p>
<div class="law">NRAU (Lei n.º 6/2006), arts. 15.º e seg.</div></div>'''+FOOT)
# ================= STORIES 1080x1920 =================
SF='<div style="position:absolute;left:0;right:0;bottom:250px;text-align:center;font-size:26px;letter-spacing:2px;color:#b9c3dc;z-index:5;font-weight:600">@mcg.advogado · Miguel Costa Gomes · Advogado</div>'
def story(css,deco,inner,ph=None,pos='center'):
    bg=(f'<div class="photo" style="background-image:url(file://{F}{ph});background-position:{pos}"></div><div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,31,61,.2) 0%,rgba(15,31,61,.1) 30%,rgba(15,31,61,.85) 58%,#0f1f3d 78%)"></div>' if ph else '')
    return doc(css,bg+deco+f'<div style="position:absolute;left:90px;right:90px;top:250px;bottom:340px;display:flex;flex-direction:column;justify-content:{"flex-end" if ph else "center"};z-index:3">{inner}</div>'+SF,1920)
GALS='<div class="deco"><div class="spot"></div><svg width="1080" height="1920" style="position:absolute;inset:0"><rect x="22" y="22" width="1036" height="1876" fill="none" stroke="#e3c167" stroke-width="3" opacity=".55"/></svg></div>'
VF='<div style="font-family:AB;font-size:50px;color:#0f1f3d;background:#e3c167;align-self:flex-start;padding:10px 24px">VERDADEIRO OU FALSO?</div>'
P['0700-story-1']=story(GAL,GALS,'''<div class="sticker" style="align-self:flex-start">ARTE FALSA · 19 NOV</div><h1 style="font-size:78px">A PJ deteve em Lisboa um suspeito de falsificar quadros de artistas famosos.</h1><p style="font-size:44px;text-align:left">E se a cópia estiver pendurada na sua sala?</p>''')
P['0700-story-2']=story(GAL,GALS,VF+'''<h1 style="font-size:80px;margin-top:50px">“Venderam-me uma cópia como original. Foi só um mau negócio, não há crime.”</h1>''')
P['0700-story-3']=story(GAL,GALS,'''<div style="font-family:AB;font-size:130px;color:#e8564b">FALSO.</div><p style="font-size:46px;text-align:left">Enganar de propósito para ficar com o seu dinheiro pode ser burla. Na burla simples, a queixa tem de ser feita em <b>6&nbsp;meses.</b></p><div class="law" style="font-size:32px">Código Penal, arts. 115.º e 217.º</div>''')
P['1500-story-1']=story(RAIN,raindeco(1920),'''<div class="sticker" style="align-self:flex-start">AVISO LARANJA · 21 NOV</div><h1 style="font-size:80px">Oito distritos com chuva forte hoje.</h1><p style="font-size:46px;text-align:left">E aquela casa de família que ninguém partilha, <b>quem trata do telhado?</b></p>''')
P['1500-story-2']=story(RAIN,raindeco(1920),VF+'''<h1 style="font-size:80px;margin-top:50px">“Se um irmão não quiser, a herança fica por partilhar para sempre.”</h1>''')
P['1500-story-3']=story(RAIN,raindeco(1920),'''<div style="font-family:AB;font-size:130px;color:#ff8a1f">FALSO.</div><p style="font-size:46px;text-align:left">Qualquer herdeiro pode exigir a partilha quando quiser. <b>Sem acordo, faz-se inventário.</b></p><div class="law" style="font-size:32px">Código Civil, art. 2101.º, n.º 1</div>''')
P['2100-story']=story(GAL,'','''<div class="sticker" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><h1 style="font-size:76px">A Clara pagou 2.400&nbsp;€ <em>por um quadro falso.</em></h1><p style="font-size:42px;text-align:left">Veja o que a lei diz no post de hoje. Deixe a sua dúvida nos comentários do post.</p>''','falso-mulher-museu.jpg','center 35%')
P['2200-story']=story(RAIN,'','''<div class="sticker" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><h1 style="font-size:76px">A casa da herança da Helena <em>meteu água.</em></h1><p style="font-size:42px;text-align:left">Saiba o que pode fazer no post de hoje. Deixe a sua dúvida nos comentários do post.</p>''','chuva-mulher-janela.jpg','center 30%')
os.makedirs(OUT,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
    pg=b.new_page()
    for k,h in P.items():
        H=1920 if 'story' in k else 1350
        pg.set_viewport_size({'width':1080,'height':H})
        fn=f'/home/claude/build/d21/{k}.html'; open(fn,'w').write(h); pg.goto('file://'+fn); pg.wait_for_timeout(500)
        pg.screenshot(path=f'/home/claude/build/d21/{k}.png'); Image.open(f'/home/claude/build/d21/{k}.png').convert('RGB').save(OUT+k+'.jpg',quality=92)
    b.close()
print('ok',len(P))
