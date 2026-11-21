import os
from playwright.sync_api import sync_playwright
from PIL import Image
R='/home/claude/mcg-imagens'; F=R+'/fotos/'
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

PKG=""":root{--a1:#e3c167;--a2:#f1d9a8}"""
FOOT='<div style="position:absolute;left:0;right:0;bottom:0;height:120px;background:linear-gradient(to top,#0f1f3d 55%,rgba(15,31,61,0));z-index:4"></div><div class="foot"><span>MIGUEL COSTA GOMES · ADVOGADO</span><span>@MCG.ADVOGADO</span></div>'
def doc(css,body,h=1350):
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{BASE}{css} body{{height:{h}px}}</style></head><body>{body}</body></html>'

def pode(foto,pos,pergunta,veredicto,texto,lei,qsize=58,ph=720,top=620):
    return doc(PKG,f'''<div class="photo" style="background-image:url(file://{F}{foto});background-size:1080px auto;background-position:{pos};height:{ph}px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:{ph-260}px;height:280px;background:linear-gradient(to bottom,rgba(15,31,61,0),#0f1f3d)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:34px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">PODE OU NÃO PODE?</div>
<div style="position:absolute;top:56px;right:70px;z-index:5;font-family:Mono;font-size:26px;color:#0f1f3d;background:#f1d9a8;padding:8px 16px;transform:rotate(3deg)">PERGUNTA DE UM SEGUIDOR</div>
<div style="position:absolute;left:80px;right:80px;top:{top}px;z-index:3">
<h1 style="font-size:{qsize}px">{pergunta}</h1>
<div style="font-family:AB;font-size:96px;color:#e3c167;margin-top:18px">{veredicto}</div>
<p style="font-size:33px;margin-top:10px">{texto}</p>
<div class="law">{lei}</div></div>'''+FOOT)
P={
 '2026-11-22/1330-imagem': pode('ruido-mulher-cama-escuro.jpg','center 30%',
   'Os vizinhos foram de férias e os filhos fazem festas até de madrugada. Posso fazer queixa?','PODE.',
   'Entre as <b>23h e as 7h</b>, a polícia pode mandar parar o barulho de imediato. Menores sozinhos ou em risco? Qualquer pessoa pode avisar a CPCJ.',
   'DL n.º 9/2007, art. 24.º',56),
 '2026-11-23/1330-imagem': pode('garantia-mulher-desportivo-amarelo.jpg','0 -580px',
   'Revisão do Porsche numa oficina Mercedes. A marca pode tirar-me a garantia?','NÃO PODE.',
   'Revisões fora da rede oficial não fazem perder a garantia, se cumprir as <b>especificações do fabricante</b>. As reparações em garantia fazem-se na marca.',
   'Regras UE da concorrência · Reg. (UE) 461/2010',56,ph=842,top=700),
}
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
    pg=b.new_page(); pg.set_viewport_size({'width':1080,'height':1350})
    for k,h in P.items():
        os.makedirs(R+'/'+k.split('/')[0],exist_ok=True)
        fn='/home/claude/build/seg/'+k.replace('/','_')+'.html'; open(fn,'w').write(h); pg.goto('file://'+fn); pg.wait_for_timeout(600)
        pg.screenshot(path=fn+'.png'); Image.open(fn+'.png').convert('RGB').save(R+'/'+k+'.jpg',quality=92)
    b.close()
print('ok')
