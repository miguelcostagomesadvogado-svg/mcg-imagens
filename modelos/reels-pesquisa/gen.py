#!/usr/bin/env python3
"""Série de Reels "Como trabalho": pesquisa no telemóvel -> resultado MCG -> passo a passo
depois do contacto -> fecho. 1080x1920, 30 fps, 17 s, sem som (a música junta-se no Instagram).
Uso: python3 gen.py config.json saida.mp4   (config: ver series.json)"""
import sys, json, math, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR = 1080, 1920, 30, 17.0
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
        m = miguel_navy(); m = m.resize((W, round(m.height * W / m.width)), Image.LANCZOS)
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
        q = s.c['pesquisa']; n = int(len(q) * max(0, min(1, (t - .6) / 2.3)))
        fq = F('r', 44 if len(q) < 30 else 39)
        d.text((185, y0 + 38), q[:n], font=fq, fill=(32, 33, 36, int(255 * k)))
        if t < 3.3 and int(t * 3) % 2 == 0:
            x = 185 + d.textlength(q[:n], font=fq) + 4
            d.line((x, y0 + 34, x, y0 + 96), fill=(26, 115, 232, 255), width=4)
        # resultado
        if t > 3.1:
            k2 = seg(t, 3.1, 3.55); ry = s.by + 170 + (1 - k2) * 120
            press = 1 - 0.03 * math.sin(math.pi * max(0, min(1, (t - 4.15) / .35)))
            card = Image.new('RGBA', (W - 120, 330), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
            rr(cd, (0, 0, card.width - 1, card.height - 1), 34, fill=(255, 255, 255, 255), outline=GOLD, width=5)
            cd.ellipse((40, 40, 120, 120), fill=NAVY); cd.text((80, 80), 'MCG', font=F('b', 26), fill=GOLD, anchor='mm')
            cd.text((145, 42), 'MCG Advogado', font=F('s', 30), fill=(32, 33, 36))
            cd.text((145, 82), 'Miguel Costa Gomes · Advogado', font=F('r', 26), fill=(95, 99, 104))
            cd.text((40, 150), s.c['resultado'], font=F('b', 40), fill=(26, 13, 171))
            cd.text((40, 210), 'Em todo o país, presencialmente ou', font=F('r', 30), fill=(77, 81, 86))
            cd.text((40, 252), 'por videochamada · +351 960 225 890', font=F('r', 30), fill=(77, 81, 86))
            if press < 1: card = card.resize((round(card.width * press), round(card.height * press)), Image.BILINEAR)
            card.putalpha(card.getchannel('A').point(lambda v: int(v * k2)))
            im.alpha_composite(card, (round((W - card.width) / 2), round(ry + (330 - card.height) / 2)))
            if t > 4.1:  # toque
                p = min(1, (t - 4.1) / .6); r = 24 + 60 * p; tx = W - 230
                d.ellipse((tx - r, ry + 175 - r, tx + r, ry + 175 + r), outline=(26, 115, 232, int(230 * (1 - p))), width=7)
                d.ellipse((tx - 22, ry + 153, tx + 22, ry + 197), fill=(26, 115, 232, int(150 * (1 - p))))
        return im.convert('RGB')

    # ---------- cena 2: passo a passo ----------
    def scene_steps(s, t):  # t desde o início da cena
        im = s.navybg.copy().convert('RGBA'); d = ImageDraw.Draw(im)
        a = seg(t, 0, .35)
        d.text((80, 200), 'DEPOIS DO CONTACTO', font=F('b', 34), fill=GOLD + (int(255 * a),))
        d.text((80, 252), 'O que acontece', font=F('d', 84), fill=CREAM + (int(255 * a),))
        d.text((80, 345), 'a seguir', font=F('d', 84), fill=CREAM + (int(255 * a),))
        y0, gap, step = 505, 190, 1.45
        cur = int((t - .35) // step)
        for i, (tit, sub) in enumerate(s.steps):
            ts = .35 + i * step
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
            d.text((x + 120, y), tit, font=F('b', 50), fill=(255, 255, 255, al))
            d.text((x + 120, y + 64), sub, font=F('r', 36), fill=CREAM[:3] + (int(al * .85),))
        return im.convert('RGB')

    # ---------- cena 3: fecho ----------
    def scene_end(s, t):
        im = Image.new('RGBA', (W, H), NAVY + (255,))
        z = 1 + .03 * t / 2.4
        m = s.miguel.resize((round(W * z), round(1150 * z)), Image.BILINEAR).crop((0, 0, W, 1150)).convert('RGBA')
        m.alpha_composite(s.fade_m); im.alpha_composite(m, (0, -60))
        d = ImageDraw.Draw(im); a = seg(t, .15, .55)
        d.text((W / 2, 1040), 'MCG Advogado', font=F('d', 92), fill=CREAM + (int(255 * a),), anchor='mm')
        d.line((W / 2 - 70, 1112, W / 2 + 70, 1112), fill=GOLD + (int(255 * a),), width=4)
        fq = F('s', 44)
        for j, ln in enumerate(['O Advogado é o escudo', 'e a espada do seu Cliente.']):
            d.text((W / 2, 1185 + j * 60), ln, font=fq, fill=GOLD + (int(255 * a),), anchor='mm')
        d.text((W / 2, 1340), 'Família · Sucessões · Laboral · Acidentes de trabalho · Penal, entre outras', font=F('r', 28), fill=CREAM + (int(220 * a),), anchor='mm')
        if t > .5: pill(d, W / 2, 1410, 'Saiba mais na legenda', F('s', 38))
        return im.convert('RGB')

    def frame(s, t):
        A, B = 5.0, 14.6
        if t < A - .25: return s.scene_search(t)
        if t < A: return Image.blend(s.scene_search(t), s.scene_steps(0), (t - (A - .25)) / .25)
        if t < B - .25: return s.scene_steps(t - A)
        if t < B: return Image.blend(s.scene_steps(t - A), s.scene_end(0), (t - (B - .25)) / .25)
        return s.scene_end(t - B)

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
