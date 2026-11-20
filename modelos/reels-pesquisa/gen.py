#!/usr/bin/env python3
"""Série de Reels "Como trabalho": pesquisa no telemóvel -> resultado MCG -> passo a passo
depois do contacto -> fecho. 1080x1920, 30 fps, 17 s, sem som (a música junta-se no Instagram).
Uso: python3 gen.py config.json saida.mp4   (config: ver series.json)"""
import sys, json, math, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR = 1080, 1920, 30, 17.8
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
        q = s.c['pesquisa']; n = int(len(q) * max(0, min(1, (t - .5) / 1.9)))
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
        d.text((80, 200), 'DEPOIS DO CONTACTO', font=F('b', 34), fill=GOLD + (int(255 * a),))
        d.text((80, 252), 'O que acontece', font=F('d', 84), fill=CREAM + (int(255 * a),))
        d.text((80, 345), 'a seguir', font=F('d', 84), fill=CREAM + (int(255 * a),))
        y0, gap, step = 505, 190, 1.2
        cur = int((t - .3) // step)
        for i, (tit, sub) in enumerate(s.steps):
            ts = .3 + i * step
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

    # ---------- cena 1b: a primeira resposta (o que o cliente recebe logo) ----------
    def scene_chat(s, t):
        im = Image.new('RGBA', (W, H), (239, 233, 223, 255)); d = ImageDraw.Draw(im)
        d.rectangle((0, 0, W, 230), fill=NAVY)
        av = s.avatar.resize((96, 96), Image.LANCZOS); im.alpha_composite(av, (50, 108))
        d.text((170, 112), 'MCG Advogado', font=F('b', 40), fill=(255, 255, 255))
        d.text((170, 162), 'Advogado · C.P. 11209P', font=F('r', 28), fill=CREAM)
        f = F('b', 30); lab = 'A PRIMEIRA RESPOSTA'; tw = d.textlength(lab, font=f)
        rr(d, ((W - tw) / 2 - 26, 262, (W + tw) / 2 + 26, 318), 28, fill=NAVY, outline=GOLD, width=2)
        d.text(((W - tw) / 2, 272), lab, font=f, fill=GOLD)
        # mensagem do cliente (à direita)
        k = seg(t, .15, .45); fm = F('r', 38)
        lines = wrap(d, s.c['mensagem'], fm, 640); bw = max(d.textlength(l, font=fm) for l in lines) + 64
        bh = len(lines) * 50 + 44; x1 = W - 50; y = 360 + (1 - k) * 40
        bub = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(bub)
        rr(bd, (x1 - bw, y, x1, y + bh), 28, fill=(220, 236, 214, int(255 * k)))
        for j, l in enumerate(lines): bd.text((x1 - bw + 32, y + 22 + j * 50), l, font=fm, fill=(32, 33, 36, int(255 * k)))
        im.alpha_composite(bub); d = ImageDraw.Draw(im)
        ry = 360 + bh + 40
        if .75 < t < 1.2:  # a escrever...
            rr(d, (50, ry, 210, ry + 80), 28, fill=(255, 255, 255))
            for j in range(3):
                a = .5 + .5 * math.sin((t * 9) - j)
                d.ellipse((85 + j * 38 - 10, ry + 30, 85 + j * 38 + 10, ry + 50), fill=(140, 140, 140, int(120 + 135 * a)))
        if t >= 1.2:  # resposta com a imagem da marca
            k2 = seg(t, 1.2, 1.5); card = s.cartao
            lines2 = [('Dr. Miguel Costa Gomes', F('b', 40), (32, 33, 36)), ('Advogado · C.P. 11209P', F('r', 36), (32, 33, 36)),
                      ('MCG Advogado', F('r', 36), (32, 33, 36)), ('+351 960 225 890', F('s', 36), (26, 115, 232)),
                      ('miguelcostagomes-11209P@adv.oa.pt', F('r', 32), (26, 115, 232)), ('instagram.com/mcg.advogado', F('r', 32), (26, 115, 232))]
            bh2 = 24 + card.height + 24 + len(lines2) * 54 + 16
            b2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); b2d = ImageDraw.Draw(b2); yy = ry + (1 - k2) * 40
            rr(b2d, (40, yy, 40 + card.width + 40, yy + bh2), 28, fill=(255, 255, 255, 255))
            b2.alpha_composite(card, (60, round(yy + 22)))
            for j, (txt, ft, col) in enumerate(lines2):
                kk = seg(t, 1.45 + j * .12, 1.7 + j * .12)
                b2d.text((68, yy + 24 + card.height + 22 + j * 54), txt, font=ft, fill=col + (int(255 * kk),))
            b2.putalpha(b2.getchannel('A').point(lambda v: int(v * k2))); im.alpha_composite(b2)
        return im.convert('RGB')

    def frame(s, t):
        A, B, C = 4.4, 7.6, 15.4
        if t < A - .25: return s.scene_search(t)
        if t < A: return Image.blend(s.scene_search(t), s.scene_chat(0), (t - (A - .25)) / .25)
        if t < B - .25: return s.scene_chat(t - A)
        if t < B: return Image.blend(s.scene_chat(t - A), s.scene_steps(0), (t - (B - .25)) / .25)
        if t < C - .25: return s.scene_steps(t - B)
        if t < C: return Image.blend(s.scene_steps(t - B), s.scene_end(0), (t - (C - .25)) / .25)
        return s.scene_end(t - C)

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
