import os,sys
from playwright.sync_api import sync_playwright
from PIL import Image
src=open('/home/claude/mcg-imagens/modelos/dia-2026-11-22/gen.py').read()
head=src[:src.index('P={}')].replace("2026-11-22/","2026-11-28/").replace("build/d22/","build/d28/")
exec(head)
exec(src[src.index("SF='"):src.index("VF=")])
s26=open('/home/claude/mcg-imagens/modelos/dia-2026-11-26/gen.py').read()
exec(s26[s26.index('CASA="""'):s26.index("AA='")])
P={}
VF='<div style="font-family:AB;font-size:50px;color:#0f1f3d;background:#e3c167;align-self:flex-start;padding:10px 24px">VERDADEIRO OU FALSO?</div>'
# ===== CARROSSEL A — Catarina / violência no namoro (25 nov) =====
VD=""":root{--a1:#ffa25c;--a2:#ffb98a}
.sticker{background:#ff8a3d;color:#0f1f3d;border:4px solid #fff}
.log{margin-top:34px;align-self:center;width:640px;background:#f6f1e6;color:#0f1f3d;border-radius:28px;padding:30px 38px;box-shadow:0 18px 30px rgba(0,0,0,.35)}
.log .h{font-family:Mono;font-size:26px;letter-spacing:3px;color:#7a1f2b;margin-bottom:12px}
.log .l{display:flex;justify-content:space-between;font-family:Inter;font-weight:600;font-size:31px;padding:9px 0;border-bottom:1px solid rgba(15,31,61,.15)}
.log .l span:last-child{color:#7a1f2b}
.log .m{margin-top:16px;background:#0f1f3d;color:#fff;border-radius:20px;padding:16px 22px;font-size:30px;font-weight:600}"""
def ondas(h=1350,op=.18):
    c=''.join(f'<circle cx="980" cy="{170 if h==1350 else 260}" r="{r}" fill="none" stroke="#ff8a3d" stroke-width="3" opacity="{op*(1-i*.2)}"/>' for i,r in enumerate([60,120,180,240]))
    c+=''.join(f'<circle cx="90" cy="{h-260}" r="{r}" fill="none" stroke="#ffb98a" stroke-width="2" opacity="{op*.7*(1-i*.25)}"/>' for i,r in enumerate([50,100,150]))
    return f'<div class="deco"><svg width="1080" height="{h}">{c}</svg></div>'
AA='PENAL · 25 NOV'
A=[]
A.append(photo('vd-mulher-telefone-escuro.jpg','45% 30%')+'''<div class="bottom"><div class="sticker" style="margin-bottom:44px">DIA CONTRA A VIOLÊNCIA · 25 NOV</div><div class="lab">A HISTÓRIA DA CATARINA</div>
<h1 style="font-size:64px">O namoro acabou há três meses. <em>As chamadas não.</em></h1><div class="swipe">DESLIZE ▶▶</div></div>''')
A.append(ondas()+'''<div class="wrap"><div class="lab">PASSO 1 · O CONFLITO</div><h1>Todas as noites, <em>o mesmo nome.</em></h1>
<div class="log"><div class="h">CHAMADAS PERDIDAS</div><div class="l"><span>Ele</span><span>23:47</span></div><div class="l"><span>Ele</span><span>00:12</span></div><div class="l"><span>Ele</span><span>01:05</span></div><div class="m">“Se não atendes, vou aí.”</div></div>
<p>Insultos, ameaças, mensagens às amigas dela. <b>Nunca viveram juntos.</b></p></div>''')
A.append(ondas()+'''<div class="wrap"><div class="lab">PASSO 2 · O ERRO</div><div class="bubble">“Nunca vivemos juntos. Isto não é violência doméstica.”</div>
<div class="x"><i>✖</i>É o que muita gente pensa.</div><p>E é por causa desta ideia que muitas mulheres <b>ficam caladas.</b></p></div>''')
A.append(ondas(op=.1)+'''<div class="wrap"><div class="lab">PASSO 3 · A REGRA</div><h1>O namoro <em>também conta.</em></h1>
<p>Maus tratos físicos ou psíquicos a quem é ou foi namorada do agressor são violência doméstica, <b>mesmo sem viverem juntos.</b> Ameaças e insultos repetidos entram aqui.</p><div class="law">Código Penal, art. 152.º, n.º 1, al. b)</div></div>''')
A.append(ondas(op=.1)+'''<div class="wrap"><div class="lab">PASSO 4 · ATENÇÃO</div><h1>Não apague <em>nada.</em></h1>
<div class="warn">Guarde o registo de chamadas e faça capturas de ecrã das mensagens, com data e hora. <b>É a sua prova.</b></div>
<p>É um crime público. O processo avança mesmo sem queixa da vítima e qualquer pessoa o pode denunciar.</p></div>''')
A.append(photo('vd-mulher-telefone-escuro-2.jpg','45% 25%')+'''<div class="bottom"><div class="lab">O DIREITO DELA</div>
<h1 style="font-size:56px">A Catarina tinha direito a viver em paz. <em>O que ele fazia era crime.</em></h1>'''+CONTACT+'''<div class="mini">Em perigo, ligue 112. Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''')
for i,b in enumerate(A,1): P[f'1230-carrossel-{i}']=doc(VD,b+hud(i,AA)+FOOT)
# ===== CARROSSEL B — Isabel / direito de habitação da viúva =====
CASA2=CASA+'.card .l span{color:#0f1f3d}.card .l span:last-child{text-align:right}.card .up span{color:#7a1f2b}'
BB='HERANÇAS · CASA DE FAMÍLIA'
B2=[]
B2.append(photo('viuva-senhora-sofa.jpg','58% 30%')+'''<div class="bottom"><div class="sticker" style="margin-bottom:44px">HERANÇAS PARADAS · CASA DE FAMÍLIA</div><div class="lab">A HISTÓRIA DA ISABEL</div>
<h1 style="font-size:62px">Ficou viúva. <em>Os filhos dele querem vender a casa.</em></h1><div class="swipe">DESLIZE ▶▶</div></div>''')
B2.append(casas()+'''<div class="wrap"><div class="lab">PASSO 1 · O CONFLITO</div><h1>31 anos <em>na mesma casa.</em></h1>
<div class="card"><div class="l"><b>CASA DE MORADA</b><b>DESDE 1995</b></div><div class="l"><span>DONO</span><span>O MARIDO</span></div><div class="l up"><span>HERDEIROS</span><span>ISABEL + 2 FILHOS DELE</span></div></div>
<p>A casa já era do marido antes de casarem. Ele morreu em março. <b>Os enteados dizem que ela tem de sair.</b></p></div>''')
B2.append(casas()+'''<div class="wrap"><div class="lab">PASSO 2 · O ERRO</div><div class="bubble">“A casa era do pai. A viúva não tem nada a dizer.”</div>
<div class="x"><i>✖</i>É o que muita gente pensa.</div><p>A viúva é herdeira. E a lei protege <b>a casa onde o casal vivia.</b></p></div>''')
B2.append(casas(op=.1)+'''<div class="wrap"><div class="lab">PASSO 3 · A REGRA</div><h1>Pode pedir <em>para ficar.</em></h1>
<p>Na partilha, quem fica viúvo pode pedir o <b>direito de habitação</b> da casa de morada de família e o direito de uso do recheio.</p><div class="law">Código Civil, art. 2103.º-A, n.º 1</div></div>''')
B2.append(casas(op=.1)+'''<div class="wrap"><div class="lab">PASSO 4 · ATENÇÃO</div><h1>Faça bem <em>as contas.</em></h1>
<div class="warn">Se esse direito valer mais do que a parte dela na herança, <b>paga a diferença</b> aos outros herdeiros.</div>
<p>E se deixar de viver lá mais de um ano, em regra perde-o.</p><div class="law">Código Civil, art. 2103.º-A, n.ºs 1 e 2</div></div>''')
B2.append(photo('miguel-cover.jpg','center 30%')+'''<div class="bottom"><div class="lab">O DIREITO DELA</div>
<h1 style="font-size:56px">A Isabel podia pedir para ficar <em>na casa onde viveu 31 anos.</em></h1>'''+CONTACT+'''<div class="mini">Guarde e partilhe. Caso ilustrativo, com nome fictício.</div></div>''')
for i,b in enumerate(B2,1): P[f'2000-carrossel-{i}']=doc(CASA2,b+hud(i,BB)+FOOT)
# ===== IMAGEM 10h30 — Pode ou não pode (marquise) =====
KEY=""":root{--a1:#e3c167;--a2:#9fd8ff}"""
P['1030-imagem']=doc(KEY,'''<div class="photo" style="background-image:url(file://'''+F+'''marquise-varandas-fechadas.jpg);background-position:62% 40%;height:760px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:400px;height:380px;z-index:2;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d 85%)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:34px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">PODE OU NÃO PODE?</div>
<div style="position:absolute;top:56px;right:70px;z-index:5;font-family:Mono;font-size:26px;color:#0f1f3d;background:#9fd8ff;padding:8px 16px;transform:rotate(3deg)">CONDOMÍNIO</div>
<div style="position:absolute;left:80px;right:80px;top:620px;z-index:3">
<h1 style="font-size:54px;padding-right:40px">O vizinho pode fechar a varanda com uma marquise sem perguntar a ninguém?</h1>
<div style="font-family:AB;font-size:92px;color:#e3c167;margin-top:10px">DEPENDE.</div>
<p style="font-size:32px;margin-top:6px">Se a marquise mudar a linha arquitetónica ou o arranjo estético do prédio, precisa de <b>autorização prévia da assembleia</b>, aprovada por dois terços do valor total do prédio.</p>
<div class="law">Código Civil, art. 1422.º, n.º 2, al. a), e n.º 3</div></div>'''+FOOT)
# ===== IMAGEM 18h00 — Portugueses no estrangeiro (usucapião) =====
FORA=""":root{--a1:#e3c167;--a2:#9fd0ff}
.ln{font-size:31px;line-height:1.45;margin-top:16px;text-align:justify;hyphens:none}.ln b{color:#e3c167}"""
P['1800-imagem']=doc(FORA,'''<div class="photo" style="background-image:url(file://'''+F+'''terreno-mulher-portao.jpg);background-position:center 62%;height:620px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:330px;height:300px;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:32px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">PORTUGUESES NO ESTRANGEIRO</div>
<div style="position:absolute;left:80px;right:80px;top:520px;z-index:3">
<div class="lab" style="color:#9fd0ff">TERRENO EM PORTUGAL</div>
<h1 style="font-size:54px">Alguém usa o seu terreno há anos? <em>O tempo conta.</em></h1>
<div class="ln"><b>O risco:</b> quem usa um terreno como dono, à vista de todos, pode ficar com ele por usucapião. Sem registo, ao fim de 15 anos (boa-fé) ou 20 (má-fé).</div>
<div class="ln"><b>O cuidado:</b> quem o usa só porque você deixa não fica dono por isso. Ponha a autorização por escrito.</div>
<div class="ln"><b>Sem vir a Portugal:</b> confirme online o registo e a caderneta.</div>
<div class="law">Código Civil, arts. 1287.º, 1296.º e 1253.º, al. b)</div></div>'''+FOOT)
# ===== STORIES =====
P['0700-story-1']=story(VD,ondas(1920),'''<div class="sticker" style="align-self:flex-start">25 NOV</div><h1 style="font-size:80px">O namoro acabou. As chamadas e as ameaças continuaram.</h1><p style="font-size:44px;text-align:left">Isto pode ser crime?</p>''')
P['0700-story-2']=story(VD,ondas(1920),VF+'''<h1 style="font-size:76px;margin-top:50px">“Se nunca viveram juntos, não é violência doméstica.”</h1>''')
P['0700-story-3']=story(VD,ondas(1920),'''<div style="font-family:AB;font-size:130px;color:#ff8a3d">FALSO.</div><p style="font-size:46px;text-align:left">O namoro, atual ou passado, também conta. <b>Mesmo sem viverem juntos.</b></p><div class="law" style="font-size:30px">Código Penal, art. 152.º, n.º 1, al. b)</div>''')
P['1500-story-1']=story(CASA2,casas(1920),'''<div class="sticker" style="align-self:flex-start">CASA DE FAMÍLIA</div><h1 style="font-size:80px">Ficou viúva. Os filhos dele querem vender a casa.</h1><p style="font-size:44px;text-align:left">Tem de sair?</p>''')
P['1500-story-2']=story(CASA2,casas(1920),VF+'''<h1 style="font-size:76px;margin-top:50px">“A casa era do marido. A viúva tem de sair.”</h1>''')
P['1500-story-3']=story(CASA2,casas(1920),'''<div style="font-family:AB;font-size:130px;color:#ff7a6b">FALSO.</div><p style="font-size:46px;text-align:left">Na partilha, pode pedir o <b>direito de habitação</b> da casa de morada de família.</p><div class="law" style="font-size:30px">Código Civil, art. 2103.º-A, n.º 1</div>''')
P['2100-story']=story(VD,'','''<div class="sticker" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><h1 style="font-size:72px">Um ex-namorado que não a deixa em paz? <em>Pode ser crime.</em></h1><p style="font-size:42px;text-align:left">Veja a história da Catarina no post de hoje. Deixe a sua dúvida nos comentários do post.</p>''','vd-mulher-mao-rosto.jpg','35% center')
P['2200-story']=story(CASA2,'','''<div class="sticker" style="align-self:flex-start">NOVA PUBLICAÇÃO</div><h1 style="font-size:72px">Ficou viúva e querem vender a casa? <em>A lei protege-a.</em></h1><p style="font-size:42px;text-align:left">A história da Isabel está no post de hoje. Deixe a sua dúvida nos comentários do post.</p>''','viuva-alianca-mao.jpg','center')
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
