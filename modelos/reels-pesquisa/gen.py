#!/usr/bin/env python3
"""Série de Reels "Como trabalho": pesquisa no telemóvel -> resultado MCG -> passo a passo
depois do contacto -> fecho. 1080x1920, 30 fps, 17 s, sem som (a música junta-se no Instagram).
Uso: python3 gen.py config.json saida.mp4   (config: ver series.json)"""
import sys, json, math, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR = 1080, 1920, 30, 23.0
NAVY = (15, 31, 61); NAVY2 = (22, 44, 84); GOLD = (201, 162, 74); CREAM = (244, 239, 230)
INTER = '/usr/share/fonts/opentype/inter/'
def F(w, s): return ImageFont.truetype(INTER + {'r': 'Inter-Regular.otf', 's': 'Inter-SemiBold.otf', 'b': 'Inter-Bold.otf', 'd': 'InterDisplay-Bold.otf'}[w], s)
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def seg(t, a, b): return ease((t - a) / (b - a))

def cover(path, fy=0.35, zoom=1.0):
    im = Image.open(path).convert('RGB')
    s = max(W / im.width, H / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2; y = int((im.height - H) * fy)
    return im.crop((x, y, x + W, y + H))

def vgrad(h, top, bot, a0, a1, pw=1.0):
    g = np.linspace(0, 1, h)[:, None] ** pw
    rgb = np.array(top) * (1 - g) + np.array(bot) * g
    a = (a0 * (1 - g) + a1 * g) * 255
    arr = np.concatenate([np.repeat(rgb[:, None, :], W, 1), np.repeat(a[:, None, :], W, 1)], 2)
    return Image.fromarray(arr.astype('uint8'), 'RGBA')

def rr(d, box, r, **k): d.rounded_rectangle(box, r, **k)

_EMO = {}
def emoji(ch, size):
    if (ch, size) not in _EMO:
        f = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
        im = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
        im = im.crop(im.getbbox()); _EMO[(ch, size)] = im.resize((size, round(im.height * size / im.width)), Image.LANCZOS)
    return _EMO[(ch, size)]

def pill(draw, cx, y, text, font, pad=(34, 16)):
    tw = draw.textlength(text, font=font)
    w = tw + pad[0] * 2 + 46; h = font.size + pad[1] * 2
    x0 = cx - w / 2
    rr(draw, (x0, y, x0 + w, y + h), h / 2, fill=NAVY + (240,), outline=GOLD, width=3)
    draw.text((x0 + pad[0], y + pad[1] - 3), text, font=font, fill=GOLD)
    ax = x0 + pad[0] + tw + 16; ay = y + h / 2  # seta dourada
    draw.line((ax, ay, ax + 26, ay), fill=GOLD, width=5)
    draw.polygon([(ax + 30, ay), (ax + 18, ay - 11), (ax + 18, ay + 11)], fill=GOLD)

def wrap(draw, text, font, maxw):
    out, line = [], ''
    for w in text.split():
        t = (line + ' ' + w).strip()
        if draw.textlength(t, font=font) <= maxw: line = t
        else: out.append(line); line = w
    out.append(line); return out

def miguel_navy():
    a = np.asarray(Image.open(os.path.join(REPO, 'fotos/miguel-cover.jpg')).convert('RGB')).astype(float)
    L = a.mean(2, keepdims=True); c = a.max(2, keepdims=True) - a.min(2, keepdims=True)
    w = np.clip((85 - L) / 60, 0, 1) * np.clip(1 - c / 45, 0, 1)
    return Image.fromarray(np.clip(a + w * (np.array(NAVY, float) - 13), 0, 255).astype('uint8'))

class Reel:
    def __init__(s, cfg):
        s.c = cfg
        s.photo = cover(os.path.join(REPO, cfg['foto']), cfg.get('foco_y', 0.3), 1.12)
        s.shade = vgrad(H, (0, 0, 0), NAVY, 0.12, 0.9, 2.2)
        s.by = cfg.get('barra_y', 880)
        s.navybg = vgrad(H, NAVY2, NAVY, 1, 1).convert('RGB')
        pf = miguel_navy().crop((0, 40, 1080, 1010)); s.perfil = pf.resize((620, round(pf.height * 620 / pf.width)), Image.LANCZOS).convert('RGBA')
        mkp = Image.new('L', s.perfil.size, 0); ImageDraw.Draw(mkp).rounded_rectangle((0, 0, s.perfil.width - 1, s.perfil.height + 40), 30, fill=255); s.perfil.putalpha(mkp)
        cr = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cartao-resposta.png')).convert('RGBA')
        s.cartao = cr.resize((900, round(cr.height * 900 / cr.width)), Image.LANCZOS)  # cartão da marca enviado na 1.ª resposta (sem morada)
        m = miguel_navy()
        av = m.crop((560, 60, 1080, 580)).resize((104, 104), Image.LANCZOS).convert('RGBA')  # fotografia de perfil
        mk = Image.new('L', (416, 416), 0); ImageDraw.Draw(mk).ellipse((0, 0, 415, 415), fill=255)
        av.putalpha(mk.resize((104, 104), Image.LANCZOS)); s.avatar = av
        m = m.resize((W, round(m.height * W / m.width)), Image.LANCZOS)
        s.miguel = m.crop((0, 0, W, 1150))
        s.fade_m = vgrad(1150, NAVY, NAVY, 0, 1)
        s.fade_m.putalpha(Image.fromarray((np.clip((np.linspace(0, 1, 1150) - .55) / .45, 0, 1) ** 1.4 * 255).astype('uint8')[:, None].repeat(W, 1)))
        s.steps = [('Contacto', 'Telefone, WhatsApp ou e-mail'),
                   ('Resposta e marcação', 'Presencial ou por videochamada'),
                   ('O que trazer', cfg['documentos']),
                   ('Reunião', 'Análise do caso e das opções'),
                   ('Honorários por escrito', 'Claros, antes de avançar'),
                   ('Procuração', 'E o caso avança')]

    # ---------- cena 1: pesquisa ----------
    def scene_search(s, t):
        z = 1 + 0.05 * t / 5
        ph = s.photo.resize((round(W * z), round(H * z)), Image.BILINEAR)
        ox, oy = (ph.width - W) // 2, (ph.height - H) // 3
        im = ph.crop((ox, oy, ox + W, oy + H)).convert('RGBA')
        im.alpha_composite(s.shade)
        d = ImageDraw.Draw(im)
        # etiqueta
        lab = 'COMO TRABALHO · ' + s.c['area'].upper()
        f = F('b', 30); tw = d.textlength(lab, font=f)
        a = int(255 * seg(t, 0, .4))
        rr(d, ((W - tw) / 2 - 26, 150, (W + tw) / 2 + 26, 210), 30, fill=NAVY + (int(a * .9),), outline=GOLD + (a,), width=2)
        d.text(((W - tw) / 2, 162), lab, font=f, fill=GOLD + (a,))
        # barra de pesquisa (genérica, sem marcas)
        k = seg(t, .15, .6); y0 = s.by + (1 - k) * 80
        rr(d, (60, y0, W - 60, y0 + 130), 65, fill=(255, 255, 255, int(255 * k)))
        cx, cy = 130, y0 + 65  # lupa
        d.ellipse((cx - 22, cy - 26, cx + 14, cy + 10), outline=(95, 99, 104, int(255 * k)), width=6)
        d.line((cx + 10, cy + 6, cx + 30, cy + 26), fill=(95, 99, 104, int(255 * k)), width=8)
        q = s.c['pesquisa']; n = int(len(q) * max(0, min(1, (t - .4) / 2.0)))
        fq = F('r', 44 if len(q) < 30 else 39)
        d.text((185, y0 + 38), q[:n], font=fq, fill=(32, 33, 36, int(255 * k)))
        if t < 2.9 and int(t * 3) % 2 == 0:
            x = 185 + d.textlength(q[:n], font=fq) + 4
            d.line((x, y0 + 34, x, y0 + 96), fill=(26, 115, 232, 255), width=4)
        # resultado
        if t > 2.6:
            k2 = seg(t, 2.6, 3.05); ry = s.by + 170 + (1 - k2) * 120
            CH = 350  # cartão ao estilo do Perfil de Empresa no Google (ficha), sem estrelas nem marcas
            card = Image.new('RGBA', (W - 120, CH), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
            rr(cd, (0, 0, card.width - 1, card.height - 1), 34, fill=(255, 255, 255, 255), outline=GOLD, width=5)
            card.alpha_composite(s.avatar, (34, 30))
            cd.text((160, 36), 'MCG Advogados - Miguel Costa Gomes', font=F('s', 31), fill=(32, 33, 36))
            cd.text((160, 82), 'Advogado · seg. a sex., 8h–21h', font=F('r', 27), fill=(95, 99, 104))
            cd.text((36, 152), s.c['resultado'], font=F('b', 38), fill=(26, 13, 171))
            cd.text((36, 204), 'Em todo o país, presencialmente ou por videochamada', font=F('r', 26), fill=(77, 81, 86))
            bx, by2, fb, pos = 36, 262, F('s', 27), {}
            for lab in ('Ligar', 'WhatsApp', 'Instagram', 'Facebook'):
                bw = cd.textlength(lab, font=fb) + 52
                rr(cd, (bx, by2, bx + bw, by2 + 58), 29, fill=(232, 240, 254) if lab == 'Ligar' else (255, 255, 255), outline=(218, 220, 224), width=2)
                cd.text((bx + 26, by2 + 13), lab, font=fb, fill=(26, 115, 232)); pos[lab] = bx + bw / 2; bx += bw + 14
            press = 1 - 0.03 * math.sin(math.pi * max(0, min(1, (t - 3.65) / .35)))
            if press < 1: card = card.resize((round(card.width * press), round(card.height * press)), Image.BILINEAR)
            card.putalpha(card.getchannel('A').point(lambda v: int(v * k2)))
            im.alpha_composite(card, (round((W - card.width) / 2), round(ry + (CH - card.height) / 2)))
            if t > 3.6:  # toque no botão WhatsApp
                p = min(1, (t - 3.6) / .6); r = 24 + 50 * p; tx = 60 + pos['WhatsApp']; ty = ry + by2 + 29
                d.ellipse((tx - r, ty - r, tx + r, ty + r), outline=(26, 115, 232, int(230 * (1 - p))), width=7)
                d.ellipse((tx - 20, ty - 20, tx + 20, ty + 20), fill=(26, 115, 232, int(150 * (1 - p))))
        return im.convert('RGB')

    # ---------- cena 2: passo a passo ----------
    def scene_steps(s, t):  # t desde o início da cena
        im = s.navybg.copy().convert('RGBA'); d = ImageDraw.Draw(im)
        a = seg(t, 0, .35)
        d.text((80, 160), 'DEPOIS DO CONTACTO', font=F('b', 34), fill=GOLD + (int(255 * a),))
        d.text((80, 210), 'O que acontece', font=F('d', 80), fill=CREAM + (int(255 * a),))
        d.text((80, 298), 'a seguir', font=F('d', 80), fill=CREAM + (int(255 * a),))
        y0, gap, step = 440, 150, 1.1
        starts = [.3, .3] + [.3 + (i - 1) * step for i in range(2, 6)]
        cur = max(i for i in range(6) if t >= starts[i]) if t >= .3 else 0
        for i, (tit, sub) in enumerate(s.steps):
            ts = starts[i]
            if t < ts: break
            k = seg(t, ts, ts + .35); y = y0 + i * gap; x = 80 + (1 - k) * 120
            if i > 0:
                ly = y0 + (i - 1) * gap + 84
                d.line((128, ly, 128, ly + (gap - 84) * k), fill=GOLD + (200,), width=4)
            active = i == cur or i == 5
            cx, cy = 128, y + 42
            if active: d.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), fill=GOLD + (int(255 * k),))
            else: d.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), outline=GOLD, width=4, fill=NAVY)
            d.text((cx, cy), str(i + 1), font=F('b', 40), fill=(NAVY if active else GOLD) + (int(255 * k),), anchor='mm')
            al = int(255 * k * (1 if active else .72))
            d.text((x + 120, y), tit, font=F('b', 48), fill=(255, 255, 255, al))
            d.text((x + 120, y + 60), sub, font=F('r', 34), fill=CREAM[:3] + (int(al * .85),))
        if t > 5.0:  # lema e pílula
            a2 = seg(t, 5.0, 5.4)
            d.text((W / 2, 1350), 'O Advogado é o escudo e a espada do seu Cliente.', font=F('s', 36), fill=GOLD + (int(255 * a2),), anchor='mm')
            if t > 5.2: pill(d, W / 2, 1400, 'Saiba mais na legenda', F('s', 38))
        return im.convert('RGB')

    # ---------- cena 1b: a primeira resposta (WhatsApp e Direct), mensagem completa da marca ----------
    LINHAS = [(None, 'Dr. Miguel Costa Gomes', 'b', 40, (32, 33, 36)), (None, 'Advogado · C.P. 11209P', 'r', 36, (32, 33, 36)),
              (None, 'MCG Advogado', 'r', 36, (32, 33, 36)), ('📞', '+351 960 225 890', 's', 36, (26, 115, 232)),
              ('✉️', 'miguelcostagomes-11209P@adv.oa.pt', 'r', 31, (26, 115, 232)),
              ('📷', 'instagram.com/mcg.advogado', 'r', 31, (26, 115, 232)),
              ('👍', 'facebook.com/advogados.portugal.', 'r', 31, (26, 115, 232)), (None, 'mcg.miguelcostagomes', 'r', 31, (26, 115, 232))]

    def _linhas(s, layer, x, y, t, t0, step=.3, lh=52):
        d = ImageDraw.Draw(layer)
        for j, (em, txt, w, sz, col) in enumerate(s.LINHAS):
            kk = seg(t, t0 + j * step, t0 + j * step + .25); al = int(255 * kk)
            if al == 0: continue
            xx = x
            if em:
                e = emoji(em, 34).copy(); e.putalpha(e.getchannel('A').point(lambda v: int(v * kk)))
                layer.alpha_composite(e, (x, round(y + j * lh + 4))); xx = x + 48
            elif j == 7: xx = x
            d.text((xx, y + j * lh), txt, font=F(w, sz), fill=col + (al,))
        return len(s.LINHAS) * lh

    def scene_chat(s, t, modo):
        ig = modo == 'ig'
        im = Image.new('RGBA', (W, H), (255, 255, 255, 255) if ig else (239, 233, 223, 255)); d = ImageDraw.Draw(im)
        if ig:
            d.rectangle((0, 0, W, 230), fill=(255, 255, 255)); d.line((0, 230, W, 230), fill=(219, 219, 219), width=2)
            im.alpha_composite(s.avatar.resize((96, 96), Image.LANCZOS), (50, 108))
            d.text((170, 112), 'mcg.advogado', font=F('b', 40), fill=(0, 0, 0)); d.text((170, 162), 'MCG Advogado', font=F('r', 28), fill=(115, 115, 115))
        else:
            d.rectangle((0, 0, W, 230), fill=NAVY)
            im.alpha_composite(s.avatar.resize((96, 96), Image.LANCZOS), (50, 108))
            d.text((170, 112), 'MCG Advogado', font=F('b', 40), fill=(255, 255, 255)); d.text((170, 162), 'Advogado · C.P. 11209P', font=F('r', 28), fill=CREAM)
        f = F('b', 30); lab = 'A PRIMEIRA RESPOSTA · ' + ('NO DIRECT DO INSTAGRAM' if ig else 'NO WHATSAPP'); tw = d.textlength(lab, font=f)
        rr(d, ((W - tw) / 2 - 26, 252, (W + tw) / 2 + 26, 308), 28, fill=NAVY, outline=GOLD, width=2)
        d.text(((W - tw) / 2, 262), lab, font=f, fill=GOLD)
        # mensagem da cliente (à direita)
        k = seg(t, .1, .4); fm = F('r', 36)
        lines = wrap(d, s.c['mensagem'], fm, 640); bw = max(d.textlength(l, font=fm) for l in lines) + 64
        bh = len(lines) * 48 + 40; x1 = W - 50; y = 335 + (1 - k) * 40
        bub = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bub)
        if ig:
            g = Image.new('RGBA', (int(bw), int(bh)));
            gr = np.linspace(0, 1, int(bw))[None, :, None]; c1, c2 = np.array([131, 58, 240]), np.array([82, 88, 236])
            g = Image.fromarray(np.concatenate([np.repeat((c1 * (1 - gr) + c2 * gr), int(bh), 0), np.full((int(bh), int(bw), 1), 255)], 2).astype('uint8'), 'RGBA')
            mk = Image.new('L', g.size, 0); ImageDraw.Draw(mk).rounded_rectangle((0, 0, g.width - 1, g.height - 1), 34, fill=int(255 * k)); g.putalpha(mk)
            bub.alpha_composite(g, (int(x1 - bw), int(y))); tc = (255, 255, 255)
        else:
            rr(bd, (x1 - bw, y, x1, y + bh), 28, fill=(220, 236, 214, int(255 * k))); tc = (32, 33, 36)
        for j, l in enumerate(lines): bd.text((x1 - bw + 32, y + 20 + j * 48), l, font=fm, fill=tc + (int(255 * k),))
        im.alpha_composite(bub); d = ImageDraw.Draw(im)
        ry = 335 + bh + 30
        if .6 < t < 1.2:  # a escrever...
            rr(d, (50, ry, 210, ry + 80), 28, fill=(239, 239, 239) if ig else (255, 255, 255))
            for j in range(3):
                a = .5 + .5 * math.sin((t * 9) - j)
                d.ellipse((85 + j * 38 - 10, ry + 30, 85 + j * 38 + 10, ry + 50), fill=(140, 140, 140, int(120 + 135 * a)))
        if t >= 1.2:
            k2 = seg(t, 1.2, 1.5); L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); Ld = ImageDraw.Draw(L); yy = ry + (1 - k2) * 40
            if ig:  # cartão do perfil do Instagram (fotografia + mcg.advogado) e depois o texto
                ph = s.perfil; rr(Ld, (40, yy, 40 + ph.width, yy + ph.height + 110), 30, fill=(239, 239, 239))
                L.alpha_composite(ph, (40, round(yy)))
                Ld.text((70, yy + ph.height + 16), 'mcg.advogado', font=F('s', 36), fill=(0, 0, 0)); Ld.text((70, yy + ph.height + 62), 'Instagram', font=F('r', 28), fill=(115, 115, 115))
                y2 = yy + ph.height + 126
                rr(Ld, (40, y2, 40 + 760, y2 + len(s.LINHAS) * 50 + 36), 30, fill=(239, 239, 239))
                s._linhas(L, 70, y2 + 18, t, 1.6, lh=50)
            else:  # imagem da marca e o texto completo
                card = s.cartao; bh2 = 22 + card.height + 22 + len(s.LINHAS) * 52 + 14
                rr(Ld, (40, yy, 40 + card.width + 40, yy + bh2), 28, fill=(255, 255, 255))
                L.alpha_composite(card, (60, round(yy + 22)))
                s._linhas(L, 68, yy + 22 + card.height + 20, t, 1.5)
            L.putalpha(L.getchannel('A').point(lambda v: int(v * k2))); im.alpha_composite(L)
        return im.convert('RGB')

    def frame(s, t):
        A, B, C = 4.6, 10.1, 15.6
        if t < A - .25: return s.scene_search(t)
        if t < A: return Image.blend(s.scene_search(t), s.scene_chat(0, 'wa'), (t - (A - .25)) / .25)
        if t < B - .25: return s.scene_chat(t - A, 'wa')
        if t < B: return Image.blend(s.scene_chat(t - A, 'wa'), s.scene_chat(0, 'ig'), (t - (B - .25)) / .25)
        if t < C - .25: return s.scene_chat(t - B, 'ig')
        if t < C: return Image.blend(s.scene_chat(t - B, 'ig'), s.scene_steps(0), (t - (C - .25)) / .25)
        return s.scene_steps(t - C)

def render(cfg, out):
    r = Reel(cfg)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        p.stdin.write(r.frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    cfg = json.load(open(sys.argv[1]))
    if isinstance(cfg, list):  # series.json: gera todos (ou o slug indicado em argv[3])
        for c in cfg:
            if len(sys.argv) > 3 and c['slug'] != sys.argv[3]: continue
            render(c, os.path.join(sys.argv[2], f"reel-pesquisa-{c['slug']}.mp4"))
    else:
        render(cfg, sys.argv[2])
