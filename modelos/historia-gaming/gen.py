from playwright.sync_api import sync_playwright
from PIL import Image
G='/usr/share/fonts/truetype/google-fonts/ofl/'
CSS=f"""
@font-face{{font-family:AB;src:url(file://{G}archivoblack/ArchivoBlack-Regular.ttf)}}
@font-face{{font-family:Mono;src:url(file://{G}anonymouspro/AnonymousPro-Bold.ttf)}}
@font-face{{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-Regular.otf);font-weight:400}}
@font-face{{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-SemiBold.otf);font-weight:600}}
@font-face{{font-family:Inter;src:url(file:///usr/share/fonts/opentype/inter/Inter-Bold.otf);font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:#0b0820;font-family:Inter;color:#f3eefc;position:relative;overflow:hidden}}
.glow1{{position:absolute;width:900px;height:900px;left:-300px;top:-250px;background:radial-gradient(circle,rgba(255,62,200,.30),transparent 65%)}}
.glow2{{position:absolute;width:900px;height:900px;right:-350px;top:380px;background:radial-gradient(circle,rgba(54,230,255,.22),transparent 65%)}}
.gsvg{{position:absolute;left:0;bottom:0;z-index:1}}
.grid{{position:absolute;left:-400px;right:-400px;bottom:-160px;height:620px;transform:perspective(520px) rotateX(62deg);transform-origin:bottom;
 background-image:linear-gradient(rgba(255,62,200,.55) 2px,transparent 2px),linear-gradient(90deg,rgba(255,62,200,.55) 2px,transparent 2px);background-size:90px 90px;
 -webkit-mask-image:linear-gradient(to top,#000 45%,transparent 100%);opacity:.9}}
.hud{{position:absolute;top:44px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:center;font-family:Mono;font-size:26px;letter-spacing:3px;color:#36e6ff;z-index:5;text-shadow:0 0 12px rgba(54,230,255,.7)}}
.bar{{display:flex;gap:6px;margin-left:16px}}.bar i{{width:34px;height:14px;border:2px solid #e3c167;display:block}}.bar i.on{{background:#e3c167;box-shadow:0 0 10px #e3c167}}
.lv{{display:flex;align-items:center}}
.wrap{{position:absolute;left:80px;right:80px;top:130px;bottom:150px;display:flex;flex-direction:column;justify-content:center;z-index:3}}
.lab{{align-self:flex-start;font-family:Mono;font-size:30px;letter-spacing:4px;color:#ff3ec8;text-shadow:0 0 14px rgba(255,62,200,.9)}}
h1{{font-family:AB;font-size:74px;line-height:1.08;margin-top:22px;color:#fff;text-shadow:0 0 22px rgba(255,62,200,.55)}}
h1 em{{font-style:normal;color:#e3c167;text-shadow:0 0 22px rgba(227,193,103,.6)}}
p{{font-size:37px;line-height:1.48;text-align:justify;hyphens:none;margin-top:30px}}
p b{{color:#36e6ff;font-weight:700}}
.law{{align-self:flex-start;display:inline-block;margin-top:26px;font-family:Mono;font-size:26px;color:#0b0820;background:#e3c167;padding:8px 16px;letter-spacing:1px}}
.card{{margin-top:34px;border:3px solid #36e6ff;border-radius:18px;padding:28px 34px;background:rgba(54,230,255,.07);box-shadow:0 0 30px rgba(54,230,255,.35),inset 0 0 30px rgba(54,230,255,.12);font-family:Mono;font-size:34px;line-height:1.7}}
.card span{{color:#36e6ff}} .card strong{{color:#e3c167}}
.bubble{{margin-top:34px;background:#fff;color:#0b0820;border-radius:26px;padding:36px 40px;font-family:AB;font-size:52px;line-height:1.18;position:relative;box-shadow:0 0 40px rgba(255,62,200,.5)}}
.bubble:after{{content:'';position:absolute;left:70px;bottom:-34px;border:18px solid transparent;border-top:20px solid #fff;border-left:22px solid #fff}}
.x{{margin-top:56px;display:flex;align-items:center;gap:22px;font-family:AB;font-size:46px;color:#ff4b6e;text-shadow:0 0 18px rgba(255,75,110,.8)}}
.x i{{font-style:normal;width:74px;height:74px;border:4px solid #ff4b6e;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:52px;box-shadow:0 0 18px rgba(255,75,110,.7)}}
.warn{{margin-top:34px;border:3px solid #e3c167;border-radius:18px;padding:28px 34px;background:rgba(227,193,103,.08);box-shadow:0 0 28px rgba(227,193,103,.35);font-size:35px;line-height:1.5;text-align:justify}}
.foot{{position:absolute;left:70px;right:70px;bottom:44px;display:flex;justify-content:space-between;font-weight:600;font-size:21px;letter-spacing:4px;color:#b9b2d6;z-index:5}}
.foot span:last-child{{color:#e3c167}}
.photo{{position:absolute;inset:0;background-size:cover;background-position:center}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,8,32,.35) 0%,rgba(11,8,32,0) 30%,rgba(11,8,32,.75) 58%,#0b0820 80%)}}
.bottom{{position:absolute;left:80px;right:80px;bottom:130px;z-index:3}}
.sticker{{position:absolute;right:0;top:-150px;transform:rotate(-8deg);font-family:AB;font-size:40px;color:#fff;padding:14px 26px;border:4px solid #ff3ec8;border-radius:14px;background:rgba(11,8,32,.55);box-shadow:0 0 26px #ff3ec8,inset 0 0 18px rgba(255,62,200,.6);text-shadow:0 0 14px #ff3ec8}}
.swipe{{margin-top:26px;font-family:Mono;font-size:30px;letter-spacing:4px;color:#36e6ff;text-shadow:0 0 12px rgba(54,230,255,.8)}}
.contact{{margin-top:22px;font-size:27px;line-height:1.6}}
.contact b{{color:#e3c167}}
.mini{{margin-top:16px;font-size:21px;color:#b9b2d6}}
svg{{display:block}}
"""
FOOT='<div style="position:absolute;left:0;right:0;bottom:0;height:120px;background:linear-gradient(to top,#0b0820 55%,rgba(11,8,32,0));z-index:4"></div><div class="foot"><span>MIGUEL COSTA GOMES · ADVOGADO</span><span>@MCG.ADVOGADO</span></div>'
def hud(n):
    bars=''.join(f'<i class="{"on" if k<=n else ""}"></i>' for k in range(1,7))
    return f'<div class="hud"><span>▶ UMA HISTÓRIA · FAMÍLIA</span><span class="lv">{n}/6<span class="bar">{bars}</span></span></div>'
def page(body,n,bg=True):
    deco='<div class="glow1"></div><div class="glow2"></div><svg class="gsvg" width="1080" height="380" viewBox="0 0 1080 380"><defs><linearGradient id="fd" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="380"><stop offset="0" stop-color="#ff3ec8" stop-opacity="0"/><stop offset=".55" stop-color="#ff3ec8" stop-opacity=".55"/><stop offset="1" stop-color="#ff3ec8" stop-opacity=".8"/></linearGradient></defs><g stroke="url(#fd)" stroke-width="2.2"><line x1="344" y1="0" x2="-1280" y2="380"/><line x1="358" y1="0" x2="-1150" y2="380"/><line x1="372" y1="0" x2="-1020" y2="380"/><line x1="386" y1="0" x2="-890" y2="380"/><line x1="400" y1="0" x2="-760" y2="380"/><line x1="414" y1="0" x2="-630" y2="380"/><line x1="428" y1="0" x2="-500" y2="380"/><line x1="442" y1="0" x2="-370" y2="380"/><line x1="456" y1="0" x2="-240" y2="380"/><line x1="470" y1="0" x2="-110" y2="380"/><line x1="484" y1="0" x2="20" y2="380"/><line x1="498" y1="0" x2="150" y2="380"/><line x1="512" y1="0" x2="280" y2="380"/><line x1="526" y1="0" x2="410" y2="380"/><line x1="540" y1="0" x2="540" y2="380"/><line x1="554" y1="0" x2="670" y2="380"/><line x1="568" y1="0" x2="800" y2="380"/><line x1="582" y1="0" x2="930" y2="380"/><line x1="596" y1="0" x2="1060" y2="380"/><line x1="610" y1="0" x2="1190" y2="380"/><line x1="624" y1="0" x2="1320" y2="380"/><line x1="638" y1="0" x2="1450" y2="380"/><line x1="652" y1="0" x2="1580" y2="380"/><line x1="666" y1="0" x2="1710" y2="380"/><line x1="680" y1="0" x2="1840" y2="380"/><line x1="694" y1="0" x2="1970" y2="380"/><line x1="708" y1="0" x2="2100" y2="380"/><line x1="722" y1="0" x2="2230" y2="380"/><line x1="736" y1="0" x2="2360" y2="380"/><line x1="0" y1="0" x2="1080" y2="0"/><line x1="0" y1="6" x2="1080" y2="6"/><line x1="0" y1="14" x2="1080" y2="14"/><line x1="0" y1="24" x2="1080" y2="24"/><line x1="0" y1="38" x2="1080" y2="38"/><line x1="0" y1="56" x2="1080" y2="56"/><line x1="0" y1="80" x2="1080" y2="80"/><line x1="0" y1="112" x2="1080" y2="112"/><line x1="0" y1="154" x2="1080" y2="154"/><line x1="0" y1="209" x2="1080" y2="209"/><line x1="0" y1="282" x2="1080" y2="282"/><line x1="0" y1="379" x2="1080" y2="379"/></g></svg>' if bg else ''
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{deco}{hud(n)}{body}{FOOT}</body></html>'
CTRL='''<svg width="420" height="250" viewBox="0 0 420 250" style="margin-top:40px;filter:drop-shadow(0 0 14px #ff3ec8)">
<path d="M110 40 H310 C370 40 405 110 412 175 C418 225 385 245 355 225 L300 180 H120 L65 225 C35 245 2 225 8 175 C15 110 50 40 110 40Z" fill="none" stroke="#ff3ec8" stroke-width="7"/>
<path d="M95 95 v50 M70 120 h50" stroke="#36e6ff" stroke-width="10" stroke-linecap="round"/>
<circle cx="310" cy="95" r="11" fill="#36e6ff"/><circle cx="340" cy="122" r="11" fill="#36e6ff"/><circle cx="280" cy="122" r="11" fill="#36e6ff"/><circle cx="310" cy="150" r="11" fill="#36e6ff"/>
<line x1="20" y1="20" x2="400" y2="235" stroke="#ff4b6e" stroke-width="9" stroke-linecap="round" opacity=".9"/></svg>'''
S=[]
S.append(page('''<div class="photo" style="background-image:url(capa.jpg);background-position:center 20%"></div><div class="shade"></div>
<div class="bottom"><div class="lab">A HISTÓRIA DA RITA</div>
<div class="sticker">GTA VI · 19 NOV</div>
<h1 style="font-size:70px">Saiu o GTA VI. Ele levou a PlayStation. <em>Mas a consola era dela.</em></h1>
<div class="swipe">DESLIZE ▶▶</div></div>''',1,bg=False))
S.append(page(f'''<div class="wrap"><div class="lab">NÍVEL 1 · O CONFLITO</div>
<h1>Saiu de casa <em>na semana do GTA VI.</em></h1>
<p>A Rita e o Pedro estiveram casados quatro anos, sem convenção antenupcial. Quando se separaram, ele saiu de casa <b>e levou a PlayStation</b>.</p>
{CTRL}</div>''',2))
S.append(page('''<div class="wrap"><div class="lab">NÍVEL 2 · O ERRO</div>
<div class="bubble">“Tudo o que entrou em casa durante o casamento é dos dois. A consola também.”</div>
<div class="x"><i>✖</i>É o que muita gente pensa.</div>
<p>Na maior parte das coisas, até é verdade. <b>Neste caso, não.</b></p></div>''',3))
S.append(page('''<div class="wrap"><div class="lab">NÍVEL 3 · A REGRA</div>
<h1>Prenda <em>não se divide.</em></h1>
<div class="card"><span>ITEM&nbsp;&nbsp;&nbsp;</span> PlayStation<br><span>ORIGEM </span> prenda de anos do irmão<br><span>CLASSE </span> <strong>bem próprio da Rita</strong></div>
<p>O que se compra durante o casamento é comum. Mas o que um dos cônjuges recebe <b>por doação</b>, depois de casar, é só seu e <b>não entra nas partilhas</b>.</p>
<div class="law">Código Civil, arts. 1722.º, n.º 1, al. b), e 1724.º</div></div>''',4))
S.append(page('''<div class="wrap"><div class="lab">NÍVEL 4 · ATENÇÃO</div>
<h1>Sem prova, <em>perde a vida extra.</em></h1>
<div class="warn">Na dúvida, a lei considera que os bens móveis são <b style="color:#e3c167">comuns</b>. Quem diz que uma coisa é só sua tem de o conseguir mostrar.</div>
<p>Guarde a mensagem de quem ofereceu, o talão ou a fotografia do dia da prenda.</p>
<div class="law">Código Civil, art. 1725.º</div></div>''',5))
S.append(page('''<div class="photo" style="background-image:url(fim.jpg);background-position:center 30%"></div><div class="shade"></div>
<div class="bottom"><div class="lab">MISSÃO CUMPRIDA</div>
<h1>A consola é da Rita. <em>De volta ao jogo.</em></h1>
<div class="contact"><b>Miguel Costa Gomes</b> · Advogado · C.P. 11209P<br>miguelcostagomes-11209P@adv.oa.pt · +351 960 225 890</div>
<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''',6,bg=False))
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
    pg=b.new_page(viewport={'width':1080,'height':1350})
    for i,h in enumerate(S,1):
        open(f's{i}.html','w').write(h); pg.goto(f'file:///home/claude/build/rita/s{i}.html'); pg.wait_for_timeout(700)
        pg.screenshot(path=f's{i}.png'); Image.open(f's{i}.png').convert('RGB').save(f'1100-carrossel-{i}.jpg',quality=92)
    b.close()
ims=[Image.open(f'1100-carrossel-{i}.jpg') for i in range(1,7)]
sh=Image.new('RGB',(1620,1350))
for k,im in enumerate(ims): sh.paste(im.resize((540,675)),((k%3)*540,(k//3)*675))
sh.save('sheet.jpg',quality=85)
