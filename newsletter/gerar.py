"""Gera a edição semanal da newsletter StartupDrops.

Uso (na raiz do repositório):
    python newsletter/gerar.py 2 "7 DE DEZEMBRO DE 2026"

Lê newsletter/edicao-NN.md (escrito no mesmo formato da edição 01) e gera:
  - static/img/newsletter/banner-edicao-NN.png  (banner azul do topo, publicado com o site)
  - newsletter/edicao-NN-CODIGO.txt             (HTML colorido para colar no Buttondown, modo Markdown)

Regras de design aprovadas pelo Leonardo:
  - Etiquetas de seção e botões em azul #0131cd com texto branco (nada de verde nos botões/etiquetas).
  - Nas notícias: título clicável + "Ler mais →" em texto. Botão só em "Leitura da semana" e "Deal da semana".
  - Verde-limão só no banner.
"""
import html
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
NAVY, BLUE, LIME, GRAY = "#06112f", "#0131cd", "#b9fc01", "#4a5578"
F = "font-family:Arial,Helvetica,sans-serif;"
BOTAO = {"Leitura da semana", "Deal da semana"}
FONTS = "/usr/share/fonts/opentype/inter/"


def banner(n: int, data: str) -> Path:
    W, H, S = 1200, 400, 2
    im = Image.new("RGB", (W * S, H * S), BLUE)
    d = ImageDraw.Draw(im)
    for x in range(0, W * S, 75 * S):
        d.line([(x, 0), (x, H * S)], fill="#1a45d4", width=S)
    for y in range(0, H * S, 75 * S):
        d.line([(0, y), (W * S, y)], fill="#1a45d4", width=S)
    try:
        f_brand = ImageFont.truetype(FONTS + "InterDisplay-Bold.otf", 64 * S)
        f_big = ImageFont.truetype(FONTS + "InterDisplay-ExtraBold.otf", 58 * S)
        f_small = ImageFont.truetype(FONTS + "Inter-Bold.otf", 22 * S)
    except OSError:
        f_brand = f_big = f_small = ImageFont.load_default()
    ic = Image.open(ROOT / "static/img/icon-180.png").convert("RGBA").resize((96 * S, 96 * S), Image.LANCZOS)
    im.paste(ic, (70 * S, 62 * S), ic)
    d.text((186 * S, 72 * S), "Startup", font=f_brand, fill="white")
    w = d.textlength("Startup", font=f_brand)
    d.text((186 * S + w, 72 * S), "Drops", font=f_brand, fill=LIME)
    titulo = "A semana em 5 minutos"
    d.text((72 * S, 200 * S), titulo, font=f_big, fill="white")
    tw = d.textlength(titulo, font=f_big)
    d.rounded_rectangle([72 * S, 276 * S, 72 * S + tw, 284 * S], radius=4 * S, fill=LIME)
    d.text((72 * S, 318 * S), f"EDIÇÃO #{n}  ·  {data.upper()}", font=f_small, fill="#dce6ff")
    out = ROOT / f"static/img/newsletter/banner-edicao-{n:02d}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    im.resize((W, H), Image.LANCZOS).save(out)
    return out


def inline(t: str) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"\[(.+?)\]\((.+?)\)",
                  lambda m: f'<a href="{m.group(2)}" style="color:{BLUE};font-weight:bold;text-decoration:none;">{m.group(1)}</a>', t)


def btn(text: str, url: str) -> str:
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:4px 0 22px;"><tr>'
            f'<td bgcolor="{BLUE}" style="background:{BLUE};border-radius:8px;"><a href="{url}" style="display:inline-block;'
            f'padding:11px 18px;{F}font-size:14px;font-weight:bold;color:#ffffff !important;text-decoration:none;">'
            f'<span style="color:#ffffff !important;"><font color="#ffffff">{html.escape(text)}</font></span></a></td></tr></table>')


def label(t: str) -> str:
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:34px 0 16px;"><tr>'
            f'<td bgcolor="{BLUE}" style="background:{BLUE};border-radius:6px;padding:6px 12px;{F}font-size:12px;'
            f'font-weight:bold;letter-spacing:1.5px;color:#ffffff;text-transform:uppercase;">{html.escape(t)}</td></tr></table>')


def gerar_html(md: str, n: int) -> str:
    body = md[md.index("Bom dia!"):] if "Bom dia!" in md else md.split("\n---\n", 1)[-1]
    out = [f'<a href="https://startupdrops.com.br/"><img src="https://startupdrops.com.br/static/img/newsletter/banner-edicao-{n:02d}.png" '
           f'alt="StartupDrops: a semana em 5 minutos. Edição #{n}" width="620" style="display:block;width:100%;max-width:620px;'
           f'height:auto;border:0;border-radius:10px;margin:0 0 24px;"></a>']
    secao = ""
    for b in [b.strip() for b in body.split("\n\n") if b.strip()]:
        if b == "---":
            out.append('<hr style="border:0;border-top:1px solid #dfe5f3;margin:34px 0;">')
            continue
        if b.startswith("## "):
            secao = b[3:]
            out.append(label(secao))
            continue
        lines = b.split("\n")
        if b.startswith("- "):
            items = "".join(f'<li style="margin:0 0 10px;">{inline(l[2:])}</li>' for l in lines)
            out.append(f'<ul style="{F}font-size:16px;line-height:1.5;color:{NAVY};padding-left:20px;margin:0 0 16px;">{items}</ul>')
            continue
        m = re.fullmatch(r"\[(.+?)\]\((.+?)\)", lines[-1].strip())
        url = None
        if m:
            url = m.group(2)
            lines = lines[:-1]
            if not lines:
                out.append(btn(m.group(1), url) if secao in BOTAO else
                           f'<p style="margin:0 0 22px;"><a href="{url}" style="{F}font-size:15px;font-weight:bold;color:{BLUE};text-decoration:none;">{html.escape(m.group(1))}</a></p>')
                continue
        first = lines[0]
        is_title = bool(re.fullmatch(r"\*\*.+\*\*", first))
        if is_title:
            t = html.escape(first.strip("*"))
            if url and secao not in BOTAO:
                t = f'<a href="{url}" style="color:{NAVY};text-decoration:none;">{t}</a>'
            out.append(f'<p style="{F}font-size:19px;line-height:1.3;font-weight:bold;color:{NAVY};margin:0 0 8px;">{t}</p>')
            lines = lines[1:]
        texto = "<br>".join(inline(l) for l in lines)
        if url and secao not in BOTAO:
            texto += f' <a href="{url}" style="color:{BLUE};font-weight:bold;text-decoration:none;white-space:nowrap;">Ler mais →</a>'
        if texto:
            mb = "26px" if (url and secao not in BOTAO) else "12px"
            out.append(f'<p style="{F}font-size:16px;line-height:1.6;color:{GRAY if is_title else NAVY};margin:0 0 {mb};">{texto}</p>')
        if url and secao in BOTAO:
            out.append(btn(m.group(1), url))
    return '<div style="max-width:620px;margin:0 auto;">\n' + "\n".join(out) + "\n</div>"


if __name__ == "__main__":
    n, data = int(sys.argv[1]), sys.argv[2]
    md = (ROOT / f"newsletter/edicao-{n:02d}.md").read_text()
    print(banner(n, data))
    codigo = ROOT / f"newsletter/edicao-{n:02d}-CODIGO.txt"
    codigo.write_text(gerar_html(md, n))
    print(codigo)
