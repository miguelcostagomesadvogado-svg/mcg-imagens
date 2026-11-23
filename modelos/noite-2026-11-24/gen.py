"""Conteúdos noturnos MCG (plano 24 h) — semana de 24 a 30 nov. 2026.
00h30: imagem para portugueses no estrangeiro (Américas). 03h30: Story de interação.
Reutiliza o estilo (BASE, FOOT, doc, story) de modelos/dia-2026-11-23/gen.py."""
import os, json
from playwright.sync_api import sync_playwright
from PIL import Image
R = '/home/claude/mcg-imagens'
src = open(R + '/modelos/dia-2026-11-23/gen.py').read()
exec(src[:src.index('P={}')])  # BASE, FOOT, CONTACT, doc, photo, ...
SF = '<div style="position:absolute;left:0;right:0;bottom:250px;text-align:center;font-size:26px;letter-spacing:2px;color:#b9c3dc;z-index:5;font-weight:600">@mcg.advogado · Miguel Costa Gomes · Advogado</div>'
CSS = """:root{--a1:#e3c167;--a2:#f1d9a8}"""
STARS = '<div class="deco"><svg width="1080" height="1920">' + ''.join(
    f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity="{o}"/>' for x, y, r, o in
    [(120,180,3,.5),(300,90,2,.4),(520,210,2,.35),(760,130,3,.5),(950,260,2,.4),(860,520,2,.3),(80,640,2,.3),
     (200,1500,3,.35),(980,1420,2,.3),(640,1700,2,.25),(400,1250,2,.2),(1000,900,3,.3)]) + \
    '<path d="M880 300 a90 90 0 1 0 60 160 a72 72 0 1 1 -60 -160z" fill="#e3c167" opacity=".85"/></svg></div>'

def imagem(foto, pos, tema, titulo, destaque, texto):
    return doc(CSS, f'''<div class="photo" style="background-image:url(file://{F}{foto});background-position:{pos};height:720px;bottom:auto"></div>
<div style="position:absolute;left:0;right:0;top:420px;height:320px;background:linear-gradient(to bottom,rgba(19,38,76,0),#13264c)"></div>
<div style="position:absolute;top:50px;left:70px;z-index:5;font-family:AB;font-size:32px;background:#e3c167;color:#0f1f3d;padding:10px 22px;letter-spacing:1px">PORTUGUESES NO MUNDO</div>
<div style="position:absolute;top:56px;right:70px;z-index:5;font-family:Mono;font-size:26px;color:#0f1f3d;background:#f1d9a8;padding:8px 16px;transform:rotate(3deg)">{tema}</div>
<div style="position:absolute;left:80px;right:80px;top:610px;z-index:3">
<h1 style="font-size:54px">{titulo}</h1>
<div style="font-family:AB;font-size:64px;color:#e3c167;margin-top:14px;line-height:1.1">{destaque}</div>
<p style="font-size:33px;margin-top:18px">{texto}</p></div>''' + FOOT)

def story(afirmacao, nota):
    inner = f'''<div style="font-family:AB;font-size:34px;color:#0f1f3d;background:#e3c167;align-self:flex-start;padding:10px 22px;letter-spacing:1px">VERDADEIRO OU FALSO?</div>
<h1 style="font-size:84px;margin-top:44px">“{afirmacao}”</h1>
<div style="margin-top:40px;font-family:Mono;font-size:32px;letter-spacing:3px;color:#e3c167">A RESPOSTA ESTÁ NO POST DESTA NOITE ▶</div>'''
    return doc(CSS, STARS + f'<div style="position:absolute;left:90px;right:90px;top:250px;bottom:340px;display:flex;flex-direction:column;justify-content:center;z-index:3">{inner}</div>' + SF, 1920)

C = json.load(open(R + '/modelos/noite-2026-11-24/conteudos.json'))
os.makedirs('/home/claude/build/noite/', exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files'])
    pg = b.new_page()
    for c in C:
        out = R + '/' + c['dia'] + '/'; os.makedirs(out, exist_ok=True)
        for k, h, H in [('0030-imagem', imagem(*c['img']), 1350), ('0330-story', story(*c['story']), 1920)]:
            pg.set_viewport_size({'width': 1080, 'height': H})
            fn = f"/home/claude/build/noite/{c['dia']}-{k}.html"; open(fn, 'w').write(h); pg.goto('file://' + fn); pg.wait_for_timeout(500)
            pg.screenshot(path=fn + '.png'); Image.open(fn + '.png').convert('RGB').save(out + k + '.jpg', quality=92)
    b.close()
print('ok', len(C))
