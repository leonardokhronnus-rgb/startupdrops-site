"""Monta o site do StartupDrops em _site/ a partir dos drops em content/.

Cada drop é um arquivo .md com um cabeçalho (entre ---) e o texto.
Veja MODELO.md para o formato.
"""
import hashlib
import json
import re
import shutil
import sys
import unicodedata
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

import config
import og

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
BRT = timezone(timedelta(hours=-3))
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
MESES_LONGOS = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
                "setembro", "outubro", "novembro", "dezembro"]
OBRIGATORIOS = ("titulo", "editoria", "data")


def slugify(s, maxlen=80):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()[:maxlen].rstrip("-") or "drop"


def parse_date(v):
    if isinstance(v, datetime):
        d = v
    elif isinstance(v, date):
        d = datetime(v.year, v.month, v.day, 8, 0)
    else:
        s, d = str(v).strip(), None
        for fmt, n in (("%Y-%m-%d %H:%M", 16), ("%Y-%m-%dT%H:%M", 16), ("%Y-%m-%d", 10)):
            try:
                d = datetime.strptime(s[:n], fmt)
                if n == 10:
                    d = d.replace(hour=8)
                break
            except ValueError:
                continue
        if d is None:
            raise ValueError(f"data inválida: {v!r} (use AAAA-MM-DD ou AAAA-MM-DD HH:MM)")
    return d.replace(tzinfo=BRT) if d.tzinfo is None else d.astimezone(BRT)


CAMPOS = {"titulo", "linha_fina", "editoria", "formato", "data", "autor", "setor", "pais", "imagem",
          "credito_imagem", "fonte", "link_fonte", "valor", "valuation", "deal_da_semana", "deal_atual", "leitura_valuation",
          "empresas", "destaque", "na_pratica", "rascunho", "slug", "simbolo",
          "patrocinado", "patrocinador", "aviso", "link_cta", "texto_cta", "site", "logo", "posicao"}


def parse_header(text):
    """Lê o cabeçalho. Aceita YAML (como o painel grava) e, se não for YAML válido,
    o formato simples 'campo: valor' por linha (o valor pode ter dois-pontos)."""
    try:
        import yaml
        y = yaml.safe_load(text)
        if isinstance(y, dict) and all(isinstance(k, str) for k in y):
            meta = {}
            desc = [k for k in y if k.lower() not in CAMPOS]
            if desc:
                raise ValueError(f"campos desconhecidos {desc} (veja MODELO.md)")
            for k, v in y.items():
                k = k.lower()
                if v is None:
                    v = ""
                elif k == "data" and not isinstance(v, str):
                    v = v.strftime("%Y-%m-%d %H:%M") if hasattr(v, "hour") else v.strftime("%Y-%m-%d") + " 09:00"
                elif k == "empresas" and isinstance(v, str):
                    v = [x.strip() for x in v.strip("[]").split(",") if x.strip()]
                elif not isinstance(v, (bool, list)):
                    v = str(v)
                meta[k] = v
            return meta
    except ValueError:
        raise
    except Exception:
        pass
    meta, desconhecidos = {}, []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"linha {n} sem 'campo:': {line.strip()[:60]}")
        k, v = line.split(":", 1)
        k, v = k.strip().lower(), v.strip()
        v = re.sub(r"\s{2,}#\s.*$", "", v)  # comentário no fim da linha (dois espaços + #)
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        if k not in CAMPOS:
            desconhecidos.append(k)
            continue
        if v.lower() in ("true", "sim"):
            v = True
        elif v.lower() in ("false", "não", "nao", ""):
            v = False if v else ""
        elif k == "empresas":
            v = [x.strip() for x in v.strip("[]").split(",") if x.strip()]
        meta[k] = v
    if desconhecidos:
        raise ValueError(f"campos desconhecidos {desconhecidos} (veja MODELO.md)")
    return meta


def load_drops():
    drops, erros = [], []
    for f in sorted((ROOT / "content").rglob("*.md")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, re.S)
        if not m:
            erros.append(f"{f.name}: falta o cabeçalho entre ---")
            continue
        try:
            meta = parse_header(m.group(1))
        except ValueError as e:
            erros.append(f"{f.name}: {e}")
            continue
        if meta.get("patrocinado"):
            meta.setdefault("editoria", "patrocinado")
        falta = [k for k in OBRIGATORIOS if not meta.get(k)]
        if falta:
            erros.append(f"{f.name}: faltam os campos {falta}")
            continue
        if meta.get("patrocinado"):
            meta["editoria"] = "patrocinado"
        elif meta["editoria"] not in config.EDITORIAS:
            erros.append(f"{f.name}: editoria '{meta['editoria']}' não existe (use {list(config.EDITORIAS)})")
            continue
        if meta.get("rascunho"):
            continue
        if meta["editoria"] in ("rodadas", "modelos", "economia"):
            # padrão de matéria: notícia, por que importa, na prática, fonte
            falta = []
            if "## Por que importa" not in m.group(2): falta.append("a seção '## Por que importa'")
            if not meta.get("na_pratica"): falta.append("o campo na_pratica")
            if not meta.get("fonte"): falta.append("o campo fonte")
            if falta:
                erros.append(f"{f.name}: falta {', '.join(falta)}")
                continue
        try:
            dt = parse_date(meta["data"])
        except ValueError as e:
            erros.append(f"{f.name}: {e}")
            continue
        ed = config.EDITORIAS.get(meta["editoria"]) or {"nome": "Branded Content", "cor": "#b9fc01", "descricao": ""}
        slug = meta.get("slug") or slugify(meta["titulo"])
        formato = meta.get("formato")
        d = {
            "file": f.name,
            "slug": slug,
            "href": f"/{meta['editoria']}/{slug}/",
            "titulo": str(meta["titulo"]).strip(),
            "linha_fina": str(meta.get("linha_fina") or "").strip(),
            "editoria": meta["editoria"],
            "ed_nome": ed["nome"],
            "cor": ed["cor"],
            "formato": formato,
            "kicker": config.FORMATOS.get(formato, ed["nome"]) if meta["editoria"] == "artigos" else ed["nome"],
            "dt": dt,
            "data_curta": f"{dt.day} {MESES[dt.month - 1]} {dt.year}",
            "data_longa": f"{dt.day} de {MESES_LONGOS[dt.month - 1]} de {dt.year}",
            "hora": dt.strftime("%H:%M"),
            "autor": meta.get("autor") or config.AUTOR_PADRAO,
            "imagem": meta.get("imagem"),
            "credito_imagem": meta.get("credito_imagem") or ("Ilustração StartupDrops" if meta.get("imagem") else ""),
            "fonte": meta.get("fonte"),
            "link_fonte": meta.get("link_fonte"),
            "valor": meta.get("valor"),
            "empresas": meta.get("empresas") or [],
            "na_pratica": str(meta.get("na_pratica") or "").strip(),
            "destaque": bool(meta.get("destaque")),
            "setor": meta.get("setor"),
            "pais": meta.get("pais"),
            "deal_da_semana": bool(meta.get("deal_da_semana")),
            "deal_atual": bool(meta.get("deal_atual")),
            "valuation": meta.get("valuation"),
            "leitura_valuation": str(meta.get("leitura_valuation") or "").strip(),
            "patrocinado": bool(meta.get("patrocinado")),
            "patrocinador": meta.get("patrocinador") or "",
            "aviso": meta.get("aviso") or "",
            "link_cta": meta.get("link_cta") or "",
            "texto_cta": meta.get("texto_cta") or "Saiba mais",
            "site": meta.get("site") or "",
            "logo": meta.get("logo") or "",
            "posicao": str(meta.get("posicao") or "").strip().lower(),
            "corpo": markdown.markdown(m.group(2).strip(), extensions=["extra", "sane_lists"]),
        }
        # A linha "Com informações de" aparece uma vez só, no rodapé da matéria.
        _m = re.search(r'<p>\s*Com informações de (.+?)\.?\s*</p>\s*', d["corpo"], re.S)
        d["fonte_html"] = ""
        if _m:
            d["fonte_html"] = _m.group(1).strip().rstrip(".").replace("<a href=", '<a target="_blank" rel="noopener nofollow" data-umami-event="fonte-original" href=')
            d["corpo"] = (d["corpo"][:_m.start()] + d["corpo"][_m.end():]).strip()
        d["simbolo"] = str(meta.get("simbolo") or "").strip() or simbolo_padrao(d)
        drops.append(d)
    slugs = [d["href"] for d in drops]
    for s in {x for x in slugs if slugs.count(x) > 1}:
        erros.append(f"dois drops com o mesmo endereço {s}: mude o título ou use o campo slug")
    return sorted(drops, key=lambda d: d["dt"], reverse=True), erros


def simbolo_padrao(d):
    """Texto do bloco visual quando o drop não tem imagem (ex.: R$180M, YC, M&A)."""
    v = d.get("valor") or ""
    m = re.search(r"(R\$|US\$|€)\s*([\d.,]+)\s*(mil(?:hões|hão)?|bilh(?:ões|ão)|mi|bi)?", v, re.I)
    if m:
        unid = (m.group(3) or "").lower()
        suf = "B" if unid.startswith("bi") else "M" if unid.startswith("mi") and unid != "mil" else "mil" if unid == "mil" else ""
        return f"{m.group(1)}{m.group(2)}{suf}"
    if d["editoria"] == "rodadas":
        return "M&A"
    fonte = re.split(r"\s+e\s+|,|\(|\s+via\s+", d.get("fonte") or "")[0].strip()
    return (fonte[:7] or {"economia": "%", "artigos": "✳", "modelos": "↗"}.get(d["editoria"], "SD"))


def write(path, content):
    f = OUT / path.lstrip("/")
    if path.endswith("/"):
        f = f / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")


def main():
    drops, erros = load_drops()
    for e in erros:
        print("ERRO:", e, file=sys.stderr)
    if erros:
        sys.exit("Corrija os erros acima antes de publicar.")
    todos = drops
    patrocinados = [d for d in drops if d["patrocinado"]]
    drops = [d for d in drops if not d["patrocinado"]]

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT / "static")
    if (ROOT / "CNAME").exists():
        shutil.copy(ROOT / "CNAME", OUT / "CNAME")

    # Versões leves das imagens (WebP): 720px para cards e 1400px para capa e matéria.
    from PIL import Image as _Img
    webdir = OUT / "static" / "img" / "web"; webdir.mkdir(parents=True, exist_ok=True)
    for d in todos:
        d["thumb"] = d["img_full"] = d["imagem"]
        src = ROOT / d["imagem"].lstrip("/") if d["imagem"] and d["imagem"].startswith("/static/") else None
        if src and src.exists():
            stem = src.stem
            for largura, campo in ((720, "thumb"), (1400, "img_full")):
                alvo = webdir / f"{stem}-{largura}.webp"
                im = _Img.open(src).convert("RGB")
                if im.width > largura:
                    im = im.resize((largura, round(im.height * largura / im.width)), _Img.LANCZOS)
                im.save(alvo, "WEBP", quality=78, method=5)
                d[campo] = f"/static/img/web/{alvo.name}"
    for d in todos:
        d["og"] = d["imagem"] or f"/static/og/{d['slug']}.png"
        if not d["imagem"]:
            og.drop_image(d, OUT / "static" / "og" / f"{d['slug']}.png")
    og.home_image(config.SITE["tagline"], OUT / "static" / "og" / "home.png")

    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]))
    import hashlib as _h
    env.globals["css_v"] = _h.md5((ROOT / "static" / "style.css").read_bytes()).hexdigest()[:8]
    now = datetime.now(BRT)
    por_ed = {k: [d for d in drops if d["editoria"] == k] for k in config.EDITORIAS}
    common = dict(
        site=config.SITE, editorias=config.EDITORIAS, year=now.year,
        hoje=f"{now.day} de {MESES_LONGOS[now.month - 1]} de {now.year}",
        ticker=drops[:14],
        destaques=drops[:3],
        deals=[d for d in por_ed["rodadas"] if d["valor"]][:5] or por_ed["rodadas"][:5],
        artigos_side=por_ed["artigos"][:3],
        patrocinadores=config.PATROCINADORES,
        analytics=config.ANALYTICS,
    )
    deals_semana = [d for d in drops if d["deal_da_semana"]]
    render = lambda tpl, **kw: env.get_template(tpl).render(**common, **kw)

    # Home
    edu_all = json.loads((ROOT / "content" / "educacao.json").read_text(encoding="utf-8")) if (ROOT / "content" / "educacao.json").exists() else {"modulos": [], "drops": []}
    mods = {m["id"]: m["nome"] for m in edu_all["modulos"]}
    dia = datetime.now(BRT).timetuple().tm_yday
    edu_teaser = []
    for i in range(3):  # 3 drops que mudam todo dia
        if edu_all["drops"]:
            x = dict(edu_all["drops"][(dia * 3 + i * 7) % len(edu_all["drops"])]); x["modulo_nome"] = mods.get(x["modulo"], ""); edu_teaser.append(x)
    # Posições na home: o campo "posicao" (manchete, lateral-1, lateral-2, card-1 ... card-9) fixa o lugar
    # de qualquer conteúdo, inclusive patrocinado. O resto entra por data, do mais novo para o mais antigo.
    todos_home = drops + patrocinados
    fixo = {d["posicao"]: d for d in sorted(todos_home, key=lambda d: d["dt"]) if d["posicao"]}
    deal = next((d for d in deals_semana if d["deal_atual"]), deals_semana[0] if deals_semana else None)
    # Regra da capa (muda todo dia):
    #   destaque = notícia do dia mais recente marcada com "destaque: true"; sem marcação, a notícia
    #   mais nova desse dia que tenha imagem. Card branco (lateral-1) = a notícia seguinte do mesmo dia.
    #   Card verde (lateral-2) = "Leitura da semana", fixada com "posicao: lateral-2" (troca semanal).
    #   Deal da semana = "deal_atual: true" (troca semanal). Patrocinado com "posicao" sempre vence.
    noticias = [d for d in drops if d["editoria"] != "artigos"]
    ultimo_dia = noticias[0]["dt"].date() if noticias else None
    do_dia = [d for d in noticias if d["dt"].date() == ultimo_dia and d is not deal]
    if fixo.get("manchete"):
        destaque = fixo["manchete"]
    else:
        destaque = next((d for d in do_dia if d["destaque"]), None) or \
                   next((d for d in do_dia if d.get("imagem")), None) or (do_dia[0] if do_dia else None)
    usados = {id(destaque), id(deal)} | {id(d) for d in fixo.values()}
    livres = [d for d in drops if id(d) not in usados]
    def preencher(prefixo, n, pool):
        out = []
        for i in range(1, n + 1):
            d = fixo.get(f"{prefixo}-{i}")
            if not d and pool:
                d = pool.pop(0)
            if d:
                out.append(d)
        return out
    pool_lat1 = [d for d in livres if d["editoria"] != "artigos"]
    lat1 = preencher("lateral", 1, pool_lat1)
    lat2 = fixo.get("lateral-2") or next((d for d in livres if d["editoria"] == "artigos" and d not in lat1), None)
    laterais = lat1 + ([lat2] if lat2 else [])
    usados |= {id(d) for d in laterais}
    livres = [d for d in drops if id(d) not in usados]
    cards = preencher("card", 9, livres)
    radar = [d for d in por_ed["rodadas"] if d is not deal][:6]
    write("/", render("index.html", active="home", title=None, destaque=destaque, laterais=laterais,
                      deal=deal, cards=cards, radar=radar, patrocinados=patrocinados, arq_pages=(len(drops) + 11) // 12,
                      edu_teaser=edu_teaser))

    # Todas as notícias (arquivo paginado, linkado da home)
    per_arq = 12
    arq = [drops[i:i + per_arq] for i in range(0, max(len(drops), 1), per_arq)]
    for n, chunk in enumerate(arq, 1):
        write("/noticias/" if n == 1 else f"/noticias/pagina/{n}/", render(
            "editoria.html", active=None, title="Todas as notícias",
            ed={"nome": "Todas as notícias", "descricao": "Tudo o que já saiu no StartupDrops, do mais novo para o mais antigo."},
            ed_slug="noticias", itens=chunk, page=n, pages=len(arq), base="/noticias/"))

    # Editorias (com paginação)
    per = config.SITE["per_page"]
    for k, ed in config.EDITORIAS.items():
        itens = por_ed[k]
        paginas = [itens[i:i + per] for i in range(0, max(len(itens), 1), per)] or [[]]
        for n, chunk in enumerate(paginas, 1):
            write(f"/{k}/" if n == 1 else f"/{k}/pagina/{n}/", render(
                "editoria.html", active=k, title=ed["nome"], ed=ed, ed_slug=k, itens=chunk,
                page=n, pages=len(paginas), base=f"/{k}/"))

    # Drops
    for d in drops:
        rel = [x for x in por_ed[d["editoria"]] if x is not d][:4]
        write(d["href"], render("drop.html", active=d["editoria"], title=d["titulo"], d=d, rel=rel))

    for d in patrocinados:
        write(d["href"], render("drop.html", active=None, title=d["titulo"], d=d, rel=[]))
    edu = json.loads((ROOT / "content" / "educacao.json").read_text(encoding="utf-8")) if (ROOT / "content" / "educacao.json").exists() else {"modulos": [], "drops": []}
    write("/educacao/", render("educacao.html", active="educacao", title="Educação", edu=edu))
    write("/deal-da-semana/", render("deals.html", active="rodadas", title="Deal da Semana", itens=deals_semana))
    write("/busca/", render("busca.html", active=None, title="Busca"))
    write("/busca.json", json.dumps([{"t": d["titulo"], "f": d["linha_fina"], "k": d["kicker"], "u": d["href"],
                                      "d": d["data_curta"]} for d in drops], ensure_ascii=False))
    write("/privacidade/", render("privacidade.html", active=None, title="Política de privacidade"))
    write("/sobre/", render("sobre.html", active="sobre", title="Sobre"))
    write("/anuncie/", render("anuncie.html", active="anuncie", title="Anuncie"))
    write("/contato/", render("contato.html", active=None, title="Fale conosco"))
    write("/termos/", render("termos.html", active=None, title="Termos de uso"))
    write("/cookies/", render("cookies.html", active=None, title="Política de cookies"))
    write("/404.html", render("404.html", active=None, title="Página não encontrada"))

    # RSS (alimenta a newsletter) e sitemap
    base = config.SITE["url"].rstrip("/")
    items = "".join(
        f"<item><title>{escape(d['titulo'])}</title><link>{base}{d['href']}</link><guid>{base}{d['href']}</guid>"
        f"<category>{escape(d['ed_nome'])}</category><pubDate>{d['dt'].strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate>"
        f"<description>{escape(d['linha_fina'])}</description></item>" for d in drops[:40])
    write("/feed.xml", f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{config.SITE["name"]}</title>'
          f"<link>{base}/</link><description>{escape(config.SITE['tagline'])}</description><language>pt-br</language>{items}</channel></rss>")
    urls = ["/", "/noticias/", "/deal-da-semana/", "/educacao/", "/sobre/", "/anuncie/", "/privacidade/", "/contato/", "/termos/", "/cookies/"] + [f"/{k}/" for k in config.EDITORIAS] + [d["href"] for d in todos]
    write("/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          + "".join(f"<url><loc>{base}{u}</loc></url>" for u in urls) + "</urlset>")
    write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")
    print(f"Site gerado com {len(drops)} drops.")


if __name__ == "__main__":
    main()
