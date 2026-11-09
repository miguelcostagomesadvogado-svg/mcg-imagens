"""Publicação automática no Instagram e no Facebook (MCG Advogado).

Corre numa GitHub Action de 15 em 15 minutos. Lê os ficheiros agenda/*.json,
publica os que estão aprovados e cuja hora (Lisboa) já chegou, e regista o
resultado. Usa só a API oficial da Meta (Graph API).

Segredos necessários no GitHub (Settings > Secrets and variables > Actions):
  META_TOKEN   token de acesso da Página do Facebook (de longa duração)
  IG_USER_ID   id da conta profissional do Instagram ligada à Página
  FB_PAGE_ID   id da Página do Facebook
Opcional (variável): GRAPH_VERSION, por omissão v25.0
"""

import datetime as dt
import glob
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

LX = ZoneInfo("Europe/Lisbon")
AGENDA = "agenda"
MAX_ATRASO_H = 6  # peças com mais atraso não saem sozinhas (vão para agenda/atrasadas)
MAX_TENTATIVAS = 3

TOKEN = os.environ.get("META_TOKEN", "").strip()
IG = os.environ.get("IG_USER_ID", "").strip()
PAGE = os.environ.get("FB_PAGE_ID", "").strip()
VER = os.environ.get("GRAPH_VERSION", "").strip() or "v25.0"
REPO = os.environ.get("GITHUB_REPOSITORY", "miguelcostagomesadvogado-svg/mcg-imagens")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")
API = f"https://graph.facebook.com/{VER}"


class ErroMeta(Exception):
    pass


def agora():
    return dt.datetime.now(LX)


def url_imagem(caminho):
    return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{urllib.parse.quote(caminho)}"


def pedido(metodo, caminho, dados=None):
    dados = dict(dados or {})
    dados["access_token"] = TOKEN
    corpo = urllib.parse.urlencode(dados).encode()
    url = f"{API}/{caminho}"
    if metodo == "GET":
        req = urllib.request.Request(url + "?" + corpo.decode())
    else:
        req = urllib.request.Request(url, data=corpo, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        txt = e.read().decode(errors="replace")
        try:
            msg = json.loads(txt).get("error", {}).get("message", txt)
        except Exception:
            msg = txt
        raise ErroMeta(f"{caminho}: {msg}") from None


# ---------- Instagram ----------

def ig_esperar(cid):
    for _ in range(40):
        st = pedido("GET", cid, {"fields": "status_code"}).get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise ErroMeta(f"contentor {cid} com estado {st}")
        time.sleep(5)
    raise ErroMeta(f"contentor {cid} não ficou pronto a tempo")


def ig_publicar(peca):
    tipo, imgs, leg = peca["tipo"], peca.get("imagens", []), peca.get("legenda", "")
    if tipo == "texto":
        return None  # o Instagram não aceita publicações só com texto
    if tipo == "story":
        ids = []
        for i in imgs:
            c = pedido("POST", f"{IG}/media", {"image_url": url_imagem(i), "media_type": "STORIES"})["id"]
            ig_esperar(c)
            ids.append(pedido("POST", f"{IG}/media_publish", {"creation_id": c})["id"])
        return ",".join(ids)
    if tipo == "imagem" or len(imgs) == 1:
        c = pedido("POST", f"{IG}/media", {"image_url": url_imagem(imgs[0]), "caption": leg})["id"]
        ig_esperar(c)
        return pedido("POST", f"{IG}/media_publish", {"creation_id": c})["id"]
    if tipo == "carrossel":
        filhos = []
        for i in imgs[:20]:
            c = pedido("POST", f"{IG}/media", {"image_url": url_imagem(i), "is_carousel_item": "true"})["id"]
            filhos.append(c)
        for c in filhos:
            ig_esperar(c)
        c = pedido("POST", f"{IG}/media", {"media_type": "CAROUSEL", "children": ",".join(filhos), "caption": leg})["id"]
        ig_esperar(c)
        return pedido("POST", f"{IG}/media_publish", {"creation_id": c})["id"]
    raise ErroMeta(f"tipo desconhecido: {tipo}")


# ---------- Facebook ----------

def fb_publicar(peca):
    tipo, imgs, leg = peca["tipo"], peca.get("imagens", []), peca.get("legenda", "")
    if tipo == "texto":
        return pedido("POST", f"{PAGE}/feed", {"message": leg})["id"]
    if tipo == "story":
        ids = []
        for i in imgs:
            foto = pedido("POST", f"{PAGE}/photos", {"url": url_imagem(i), "published": "false"})["id"]
            r = pedido("POST", f"{PAGE}/photo_stories", {"photo_id": foto})
            ids.append(str(r.get("post_id") or r.get("id") or foto))
        return ",".join(ids)
    if tipo == "imagem" or len(imgs) == 1:
        r = pedido("POST", f"{PAGE}/photos", {"url": url_imagem(imgs[0]), "message": leg})
        return r.get("post_id") or r["id"]
    if tipo == "carrossel":
        dados = {"message": leg}
        for n, i in enumerate(imgs):
            foto = pedido("POST", f"{PAGE}/photos", {"url": url_imagem(i), "published": "false"})["id"]
            dados[f"attached_media[{n}]"] = json.dumps({"media_fbid": foto})
        return pedido("POST", f"{PAGE}/feed", dados)["id"]
    raise ErroMeta(f"tipo desconhecido: {tipo}")


# ---------- ciclo principal ----------

def ler_hora(txt):
    t = dt.datetime.fromisoformat(txt)
    return t if t.tzinfo else t.replace(tzinfo=LX)


def guardar(caminho, peca):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(peca, f, ensure_ascii=False, indent=2)
        f.write("\n")


def mover(caminho, pasta):
    os.makedirs(os.path.join(AGENDA, pasta), exist_ok=True)
    shutil.move(caminho, os.path.join(AGENDA, pasta, os.path.basename(caminho)))


def estado(linhas):
    with open(os.path.join(AGENDA, "ESTADO.md"), "w", encoding="utf-8") as f:
        f.write("# Estado da publicação automática\n\n" + "\n".join(linhas) + "\n")


def verificar():
    """Confirma que o token e os ids funcionam (corrida manual 'verificar')."""
    linhas = [f"Última verificação: {agora():%Y-%m-%d %H:%M} (Lisboa)", ""]
    ok = True
    try:
        p = pedido("GET", PAGE, {"fields": "name"})
        linhas.append(f"- Página do Facebook: OK ({p.get('name')})")
    except ErroMeta as e:
        ok = False
        linhas.append(f"- Página do Facebook: ERRO — {e}")
    try:
        u = pedido("GET", IG, {"fields": "username"})
        linhas.append(f"- Instagram: OK (@{u.get('username')})")
        lim = pedido("GET", f"{IG}/content_publishing_limit", {"fields": "quota_usage,config"})
        linhas.append(f"- Limite de publicações do Instagram nas últimas 24 h: {json.dumps(lim.get('data', lim), ensure_ascii=False)}")
    except ErroMeta as e:
        ok = False
        linhas.append(f"- Instagram: ERRO — {e}")
    linhas.insert(1, "Ligação à Meta: ATIVA" if ok else "Ligação à Meta: COM ERRO")
    estado(linhas)
    print("\n".join(linhas))
    return ok


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "publicar"
    if not (TOKEN and IG and PAGE):
        estado([
            "Ligação à Meta: NÃO CONFIGURADA",
            "",
            "Faltam os segredos META_TOKEN, IG_USER_ID e FB_PAGE_ID no GitHub.",
            "As peças aprovadas ficam guardadas na agenda e saem quando a ligação estiver ativa.",
        ])
        print("Segredos em falta: nada publicado.")
        return
    if modo == "verificar":
        verificar()
        return

    publicadas, erros = [], []
    for caminho in sorted(glob.glob(os.path.join(AGENDA, "*.json"))):
        with open(caminho, encoding="utf-8") as f:
            peca = json.load(f)
        if not peca.get("aprovado"):
            continue
        quando = ler_hora(peca["quando"])
        if quando > agora():
            continue
        atraso = (agora() - quando).total_seconds() / 3600
        if atraso > MAX_ATRASO_H and not peca.get("publicar_atrasado"):
            peca["nota"] = f"Não publicada: {atraso:.0f} h de atraso. Mude 'quando' para publicar."
            guardar(caminho, peca)
            mover(caminho, "atrasadas")
            continue
        feito = peca.setdefault("feito", {})
        for rede in peca.get("redes", ["instagram", "facebook"]):
            if rede in feito:
                continue
            try:
                rid = ig_publicar(peca) if rede == "instagram" else fb_publicar(peca)
                feito[rede] = rid or "não aplicável"
                print(f"OK {os.path.basename(caminho)} {rede} {rid}")
            except ErroMeta as e:
                peca.setdefault("erros", []).append(f"{agora():%Y-%m-%d %H:%M} {rede}: {e}")
                print(f"ERRO {os.path.basename(caminho)} {rede}: {e}")
        if all(r in feito for r in peca.get("redes", [])):
            peca["publicado_em"] = f"{agora():%Y-%m-%d %H:%M}"
            guardar(caminho, peca)
            mover(caminho, "publicado")
            publicadas.append(os.path.basename(caminho))
        else:
            peca["tentativas"] = peca.get("tentativas", 0) + 1
            guardar(caminho, peca)
            if peca["tentativas"] >= MAX_TENTATIVAS:
                mover(caminho, "erros")
                erros.append(os.path.basename(caminho))

    linhas = ["Ligação à Meta: ATIVA", "", f"Última execução: {agora():%Y-%m-%d %H:%M} (Lisboa)"]
    if publicadas:
        linhas.append("Publicadas nesta execução: " + ", ".join(publicadas))
    if erros:
        linhas.append("Com erro (ver agenda/erros/): " + ", ".join(erros))
    if glob.glob(os.path.join(AGENDA, "erros", "*.json")):
        linhas.append("Há peças em agenda/erros/ por resolver.")
    if publicadas or erros:
        estado(linhas)


if __name__ == "__main__":
    main()
