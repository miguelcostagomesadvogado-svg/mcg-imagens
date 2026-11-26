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
import re
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

def _limpar_token(t):
    """Aceita o token mesmo que tenha sido colado com aspas, vírgula ou com o prefixo "access_token":."""
    t = (t or "").strip()
    if ":" in t:
        t = t.split(":")[-1]
    return t.strip().strip(",").strip().strip('"').strip("'").strip()


TOKEN = _limpar_token(os.environ.get("META_TOKEN", ""))
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


def limitar_hashtags(leg, maximo=5):
    """O Instagram só aceita 5 hashtags: mantém as 5 primeiras e retira as restantes."""
    vistos = [0]
    def troca(m):
        vistos[0] += 1
        return m.group(0) if vistos[0] <= maximo else ""
    leg = re.sub(r"(?<!\S)#\w+", troca, leg)
    return re.sub(r"[ \t]+(\n|$)", r"\1", re.sub(r"[ \t]{2,}", " ", leg))


def ig_publicar(peca):
    tipo, imgs, leg = peca["tipo"], peca.get("imagens", []), limitar_hashtags(peca.get("legenda", ""))
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
    tipo, imgs, leg = peca["tipo"], peca.get("imagens", []), limitar_hashtags(peca.get("legenda", ""))
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


# ---------- primeiro comentário ----------

def comentar(peca, rede, rid):
    """Escreve o primeiro comentário (campo 'comentario') logo a seguir à publicação.
    Não se aplica a stories. Uma falha aqui nunca anula a publicação: fica registada."""
    texto = (peca.get("comentario") or "").strip()
    if not texto or peca.get("tipo") == "story" or not rid or rid == "não aplicável":
        return None
    feitos = peca.setdefault("comentado", {})
    if rede in feitos:
        return None
    time.sleep(5)  # dá tempo à publicação para ficar disponível
    try:
        cid = pedido("POST", f"{rid}/comments", {"message": texto}).get("id")
        feitos[rede] = cid or "ok"
        print(f"Comentário OK {rede} {cid}")
        return None
    except ErroMeta as e:
        msg = f"{agora():%Y-%m-%d %H:%M} {rede}: {e}"
        peca.setdefault("erros_comentario", []).append(msg)
        print(f"Comentário ERRO {msg}")
        return msg


# ---------- Caixinha de perguntas: recolha semanal dos comentários ----------

PERGUNTAS = "perguntas"


def recolher_perguntas(forcar=False):
    """Ao domingo (a partir das 04h00), junta as dúvidas deixadas nos comentários das
    publicações dos últimos 7 dias em perguntas/AAAA-MM-DD.md, para a "Pergunta da semana".
    RGPD: guarda só o texto da pergunta — nunca nomes, @ ou identificadores de quem comentou."""
    hoje = agora()
    if not forcar and (hoje.weekday() != 6 or hoje.hour < 4):
        return None
    destino = os.path.join(PERGUNTAS, f"{hoje:%Y-%m-%d}.md")
    if os.path.exists(destino):
        return None
    limite = hoje - dt.timedelta(days=7)
    perguntas, vistos = [], set()
    for caminho in sorted(glob.glob(os.path.join(AGENDA, "publicado", "*.json"))):
        with open(caminho, encoding="utf-8") as f:
            peca = json.load(f)
        if peca.get("tipo") == "story" or not peca.get("publicado_em"):
            continue
        try:
            quando_pub = dt.datetime.strptime(peca["publicado_em"], "%Y-%m-%d %H:%M").replace(tzinfo=LX)
        except ValueError:
            continue
        if quando_pub < limite:
            continue
        proprios = {(peca.get("comentario") or "").strip()}
        for rede, rid in (peca.get("feito") or {}).items():
            if not rid or rid == "não aplicável":
                continue
            try:
                if rede == "instagram":
                    dados = pedido("GET", f"{rid}/comments", {"fields": "text,username", "limit": "100"}).get("data", [])
                    itens = [(c.get("text") or "") for c in dados if c.get("username") != "mcg.advogado"]
                else:
                    dados = pedido("GET", f"{rid}/comments", {"fields": "message,from", "limit": "100"}).get("data", [])
                    itens = [(c.get("message") or "") for c in dados if (c.get("from") or {}).get("id") != PAGE]
            except ErroMeta as e:
                print(f"Perguntas: não li {rede} {rid}: {e}")
                continue
            for t in itens:
                t = re.sub(r"@[\w.]+", "", t).strip()
                if len(t) < 15 or "?" not in t or t in proprios:
                    continue
                chave = t.lower()
                if chave in vistos:
                    continue
                vistos.add(chave)
                perguntas.append((os.path.basename(caminho)[:-5], t))
    os.makedirs(PERGUNTAS, exist_ok=True)
    linhas = [f"# Perguntas da semana até {hoje:%d/%m/%Y}", "",
              "Recolhidas automaticamente dos comentários. Só o texto (sem nomes nem @).",
              "Responder sempre em termos gerais, sem identificar quem perguntou.", ""]
    if perguntas:
        for origem, t in perguntas:
            linhas.append(f"- ({origem}) {t}")
    else:
        linhas.append("- (nenhuma pergunta nos comentários desta semana)")
    with open(destino, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    print(f"Perguntas guardadas em {destino}: {len(perguntas)}")
    return destino


# ---------- Comentários dos seguidores: recolha e respostas aprovadas ----------
# comentarios/pendentes/<rede>-<id>.json  -> comentários à espera de resposta
#   o Claude escreve "resposta"; o Dr. Miguel aprova -> "aprovado": true -> a Action responde
#   "ignorar": true -> arquiva sem responder
# comentarios/respondidos/ e comentarios/ignorados/ -> arquivo
# RGPD (repositório público): guarda só o texto do comentário, nunca nomes nem @.

COMENT = "comentarios"
DIAS_COMENT = 7
MIN_ENTRE_RECOLHAS = 10


def _ja_tratado(nome):
    return any(os.path.exists(os.path.join(COMENT, d, nome)) for d in ("pendentes", "respondidos", "ignorados"))


def _limpar_txt(t):
    return re.sub(r"@[\w.]+", "", t or "").strip()


def _pendentes_do_fio(itens, eu):
    """itens: lista (id, texto, autor_e_eu, quando) do fio (comentário + respostas).
    Devolve os comentários de terceiros feitos depois da última intervenção da MCG."""
    itens = sorted(itens, key=lambda x: x[3])
    ultimo_meu = max([i for i, it in enumerate(itens) if it[2]], default=-1)
    return [it for it in itens[ultimo_meu + 1:] if not it[2]]


def recolher_comentarios(forcar=False):
    os.makedirs(os.path.join(COMENT, "pendentes"), exist_ok=True)
    marca = os.path.join(COMENT, "ultima-recolha.txt")
    if not forcar and os.path.exists(marca):
        try:
            ult = dt.datetime.strptime(open(marca).read().strip(), "%Y-%m-%d %H:%M").replace(tzinfo=LX)
            if (agora() - ult).total_seconds() < MIN_ENTRE_RECOLHAS * 60:
                return 0
        except ValueError:
            pass
    limite = agora() - dt.timedelta(days=DIAS_COMENT)
    novos = 0
    ainda, lidas = set(), set()

    def guardar_pend(rede, alvo, item, pub_txt, link):
        nonlocal novos
        nome = f"{rede}-{item[0]}.json"
        ainda.add(nome)
        if _ja_tratado(nome):
            return
        texto = _limpar_txt(item[1])
        if not texto:
            return
        dados = {"rede": rede, "alvo": alvo, "comentario_id": item[0], "comentario": texto,
                 "quando": item[3].strftime("%Y-%m-%d %H:%M"), "publicacao": pub_txt, "link": link,
                 "resposta": "", "aprovado": False}
        with open(os.path.join(COMENT, "pendentes", nome), "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        novos += 1

    def hora(txt):
        return dt.datetime.fromisoformat(txt.replace("Z", "+00:00").replace("+0000", "+00:00")).astimezone(LX)

    # Instagram
    try:
        media = pedido("GET", f"{IG}/media", {"fields": "id,caption,permalink,timestamp,comments_count", "limit": "20"}).get("data", [])
    except ErroMeta as e:
        print(f"Comentários IG: {e}")
        media = None
    if media is not None:
        lidas.add("instagram")
    media = media or []
    for m in media:
        if not m.get("comments_count") or hora(m["timestamp"]) < limite:
            continue
        pub = (m.get("caption") or "").split("\n")[0][:120]
        try:
            lst = pedido("GET", f"{m['id']}/comments", {"fields": "id,text,username,timestamp,replies{id,text,username,timestamp}", "limit": "50"}).get("data", [])
        except ErroMeta as e:
            print(f"Comentários IG {m['id']}: {e}")
            lidas.discard("instagram")
            continue
        for c in lst:
            fio = [(c["id"], c.get("text"), c.get("username") == "mcg.advogado", hora(c["timestamp"]))]
            for r in (c.get("replies") or {}).get("data", []):
                fio.append((r["id"], r.get("text"), r.get("username") == "mcg.advogado", hora(r["timestamp"])))
            for it in _pendentes_do_fio(fio, "mcg.advogado"):
                if it[3] >= limite:
                    guardar_pend("instagram", c["id"], it, pub, m.get("permalink", ""))

    # Facebook (publicações e Reels da Página)
    posts = []
    lidas.add("facebook")
    for ponto, campos in ((f"{PAGE}/feed", "id,message,permalink_url,created_time"),
                          (f"{PAGE}/video_reels", "id,description,permalink_url,created_time")):
        try:
            posts += pedido("GET", ponto, {"fields": campos, "limit": "20"}).get("data", [])
        except ErroMeta as e:
            print(f"Comentários FB {ponto}: {e}")
            if ponto.endswith("/feed"):
                lidas.discard("facebook")
    vistos = set()
    for p in posts:
        if p["id"] in vistos or hora(p["created_time"]) < limite:
            continue
        vistos.add(p["id"])
        pub = (p.get("message") or p.get("description") or "").split("\n")[0][:120]
        try:
            lst = pedido("GET", f"{p['id']}/comments", {"fields": "id,message,from,created_time,comments.limit(25){id,message,from,created_time}", "limit": "50"}).get("data", [])
        except ErroMeta as e:
            print(f"Comentários FB {p['id']}: {e}")
            lidas.discard("facebook")
            continue
        for c in lst:
            eu = lambda x: (x.get("from") or {}).get("id") == PAGE
            fio = [(c["id"], c.get("message"), eu(c), hora(c["created_time"]))]
            for r in (c.get("comments") or {}).get("data", []):
                fio.append((r["id"], r.get("message"), eu(r), hora(r["created_time"])))
            for it in _pendentes_do_fio(fio, PAGE):
                if it[3] >= limite:
                    guardar_pend("facebook", c["id"], it, pub, p.get("permalink_url", ""))

    # Já respondidos à mão (ou apagados): saem dos pendentes, se ainda não foram aprovados.
    for caminho in glob.glob(os.path.join(COMENT, "pendentes", "*.json")):
        nome = os.path.basename(caminho)
        if nome.split("-")[0] not in lidas or nome in ainda:
            continue
        with open(caminho, encoding="utf-8") as f:
            c = json.load(f)
        if c.get("aprovado"):
            continue
        c["respondido_a_mao"] = f"{agora():%Y-%m-%d %H:%M}"
        os.makedirs(os.path.join(COMENT, "respondidos"), exist_ok=True)
        with open(os.path.join(COMENT, "respondidos", nome), "w", encoding="utf-8") as f:
            json.dump(c, f, ensure_ascii=False, indent=2)
        os.remove(caminho)
    with open(marca, "w") as f:
        f.write(f"{agora():%Y-%m-%d %H:%M}")
    if novos:
        print(f"Comentários novos por responder: {novos}")
    return novos


def responder_aprovadas():
    feitas = []
    for caminho in sorted(glob.glob(os.path.join(COMENT, "pendentes", "*.json"))):
        with open(caminho, encoding="utf-8") as f:
            c = json.load(f)
        destino = None
        if c.get("ignorar"):
            destino = "ignorados"
        elif c.get("aprovado") and (c.get("resposta") or "").strip():
            try:
                if c["rede"] == "instagram":
                    rid = pedido("POST", f"{c['alvo']}/replies", {"message": c["resposta"].strip()}).get("id")
                else:
                    rid = pedido("POST", f"{c['alvo']}/comments", {"message": c["resposta"].strip()}).get("id")
                c["respondido_em"] = f"{agora():%Y-%m-%d %H:%M}"
                c["resposta_id"] = rid
                destino = "respondidos"
            except ErroMeta as e:
                c["erro"] = f"{agora():%Y-%m-%d %H:%M} {e}"
                c["aprovado"] = False
                print(f"Resposta ERRO {caminho}: {e}")
        if destino or c.get("erro"):
            if destino:
                os.makedirs(os.path.join(COMENT, destino), exist_ok=True)
                novo = os.path.join(COMENT, destino, os.path.basename(caminho))
            else:
                novo = caminho
            with open(novo, "w", encoding="utf-8") as f:
                json.dump(c, f, ensure_ascii=False, indent=2)
            if destino:
                os.remove(caminho)
                feitas.append(os.path.basename(caminho))
    if feitas:
        print("Comentários tratados: " + ", ".join(feitas))
    return feitas


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
    if modo == "perguntas":
        recolher_perguntas(forcar=True)
        return
    if modo == "comentarios":
        responder_aprovadas()
        recolher_comentarios(forcar=True)
        return
    # Se a ligação à Meta falhar, não mexe na agenda (as peças não contam tentativas).
    try:
        pedido("GET", PAGE, {"fields": "id"})
    except ErroMeta as e:
        estado(["Ligação à Meta: COM ERRO", "", f"Última tentativa: {agora():%Y-%m-%d %H:%M} (Lisboa)", f"- {e}",
                "As peças aprovadas ficam guardadas e saem quando a ligação voltar."])
        print(f"Ligação à Meta com erro: {e}")
        return

    publicadas, erros, erros_coment = [], [], []
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
                erro_c = comentar(peca, rede, rid)
                if erro_c:
                    erros_coment.append(f"{os.path.basename(caminho)} — {erro_c}")
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

    # Peças já publicadas nas últimas 12 h que ficaram sem o primeiro comentário
    # (ex.: publicadas por uma versão antiga do script): comenta agora, uma única tentativa.
    for caminho in sorted(glob.glob(os.path.join(AGENDA, "publicado", "*.json"))):
        with open(caminho, encoding="utf-8") as f:
            peca = json.load(f)
        forcar = bool(peca.get("comentar_agora"))
        if not peca.get("comentario") or not peca.get("publicado_em"):
            continue
        if peca.get("erros_comentario") and not forcar:
            continue
        try:
            quando_pub = dt.datetime.strptime(peca["publicado_em"], "%Y-%m-%d %H:%M").replace(tzinfo=LX)
        except ValueError:
            continue
        if (agora() - quando_pub).total_seconds() > 12 * 3600 and not forcar:
            continue
        if forcar:
            # nova tentativa pedida à mão: limpa erros antigos e não repete se o texto já lá estiver
            peca.pop("comentar_agora", None)
            peca.pop("erros_comentario", None)
            for rede, rid in (peca.get("feito") or {}).items():
                if rede in (peca.get("comentado") or {}):
                    continue
                try:
                    campo = "text" if rede == "instagram" else "message"
                    lst = pedido("GET", f"{rid}/comments", {"fields": campo, "limit": "50"}).get("data", [])
                    if any((c.get(campo) or "").strip() == peca["comentario"].strip() for c in lst):
                        peca.setdefault("comentado", {})[rede] = "já existia"
                except ErroMeta:
                    pass
        mudou = False
        for rede, rid in (peca.get("feito") or {}).items():
            if rede in (peca.get("comentado") or {}):
                continue
            mudou = True
            erro_c = comentar(peca, rede, rid)
            if erro_c:
                erros_coment.append(f"{os.path.basename(caminho)} — {erro_c}")
        if mudou:
            guardar(caminho, peca)
            publicadas.append(os.path.basename(caminho) + " (só comentário)")

    try:
        recolher_perguntas()
    except Exception as e:  # a recolha nunca pode travar a publicação
        print(f"Perguntas: erro {e}")
    for func in (responder_aprovadas, recolher_comentarios):
        try:
            func()
        except Exception as e:  # os comentários nunca podem travar a publicação
            print(f"Comentários: erro {e}")
    if os.path.isdir(COMENT):
        git("add", "-A", COMENT)  # o ciclo em curso faz o commit e o push

    linhas = ["Ligação à Meta: ATIVA", "", f"Última execução: {agora():%Y-%m-%d %H:%M} (Lisboa)"]
    if publicadas:
        linhas.append("Publicadas nesta execução: " + ", ".join(publicadas))
    if erros:
        linhas.append("Com erro (ver agenda/erros/): " + ", ".join(erros))
    if erros_coment:
        linhas.append("Primeiro comentário NÃO publicado (a peça saiu): " + "; ".join(erros_coment))
    if glob.glob(os.path.join(AGENDA, "erros", "*.json")):
        linhas.append("Há peças em agenda/erros/ por resolver.")
    if publicadas or erros or erros_coment:
        estado(linhas)


def git(*args):
    import subprocess
    return subprocess.run(["git", *args], capture_output=True, text=True)


def ciclo(minutos=345, intervalo=120):
    """Vigia a agenda durante ~5h45: atualiza do GitHub, publica o que estiver na hora e guarda o resultado."""
    fim = time.time() + minutos * 60
    while True:
        git("stash", "-q")
        git("pull", "--rebase", "-q")
        git("stash", "pop", "-q")
        # Corre num processo novo para usar sempre a versão mais recente deste ficheiro
        # (alterações feitas durante a execução de ~6 h passam a valer logo).
        import subprocess
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "publicar"])
        if r.returncode != 0:
            print(f"Erro inesperado (código {r.returncode})")
        git("add", "-A", AGENDA)
        if os.path.isdir(PERGUNTAS):
            git("add", "-A", PERGUNTAS)
        if os.path.isdir(COMENT):
            git("add", "-A", COMENT)
        if git("diff", "--cached", "--quiet").returncode != 0:
            git("commit", "-q", "-m", "Agenda: resultado da publicação")
            for _ in range(3):
                git("pull", "--rebase", "-q")
                if git("push", "-q").returncode == 0:
                    break
                time.sleep(5)
        if time.time() + intervalo > fim:
            break
        time.sleep(intervalo)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "ciclo":
        ciclo()
    else:
        main()
