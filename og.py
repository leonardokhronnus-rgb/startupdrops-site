"""Imagens de compartilhamento (LinkedIn, WhatsApp, X) no estilo Azul & Lima. 1200x630."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONTS = ROOT / "static" / "fonts"
BLUE, LIME, NAVY, DEEP = (1, 49, 205), (185, 252, 1), (6, 17, 47), (7, 15, 43)
W, H = 1200, 630


def font(name, size, weight="Bold"):
    f = ImageFont.truetype(str(FONTS / name), size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def wrap(draw, text, fnt, maxw, maxlines):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        while draw.textlength(lines[-1] + "…", font=fnt) > maxw and " " in lines[-1]:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += "…"
    return lines


def base(bg=BLUE):
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 22))
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 22))
    # marca (logo oficial)
    logo = Image.open(ROOT / "assets" / "logo-full.png").convert("RGBA")
    lh = 74
    logo = logo.resize((int(logo.width * lh / logo.height), lh), Image.LANCZOS)
    img = img.convert("RGBA")
    img.alpha_composite(logo, (52, 34))
    img = img.convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    return img, d


def drop_image(d, out: Path):
    img, dr = base(BLUE)
    # símbolo grande ao fundo
    fs = font("SpaceGrotesk.ttf", 260)
    sym = d["simbolo"][:8]
    while dr.textlength(sym, font=fs) > 560 and fs.size > 120:
        fs = font("SpaceGrotesk.ttf", fs.size - 20)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((W - 50, H - 30), sym, font=fs, fill=(185, 252, 1, 46), anchor="rd")
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    dr = ImageDraw.Draw(img, "RGBA")
    # pill da editoria
    fp = font("DMSans.ttf", 22, "ExtraBold")
    label = d["kicker"].upper() + (f" · {d['valor']}" if d.get("valor") else "")
    tw = dr.textlength(label, font=fp)
    dr.rounded_rectangle([60, 150, 60 + tw + 32, 194], radius=6, fill=LIME)
    dr.text((76, 172), label, font=fp, fill=NAVY, anchor="lm")
    # título
    size = 64
    while True:
        ft = font("SpaceGrotesk.ttf", size)
        lines = wrap(dr, d["titulo"], ft, 1060, 4)
        if len(lines) <= 3 or size <= 50:
            break
        size -= 4
    y = 232
    for ln in lines:
        dr.text((60, y), ln, font=ft, fill="white")
        y += int(size * 1.12)
    # rodapé
    fm = font("DMSans.ttf", 22, "Bold")
    meta = f"Por {d['autor']} · " + d["data_curta"]
    dr.text((60, H - 56), meta.upper(), font=fm, fill=(201, 214, 255), anchor="lm")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)


def home_image(_tagline: str, out: Path):
    tagline = "Deals, tendências, economia e as melhores ideias do mundo, com contexto para quem toma decisões."
    img, dr = base(BLUE)
    ft = font("SpaceGrotesk.ttf", 92)
    dr.text((60, 210), "O que um fundador", font=ft, fill="white")
    dr.text((60, 312), "precisa", font=ft, fill=LIME)
    dr.text((60 + dr.textlength("precisa ", font=ft), 312), "ler hoje.", font=ft, fill="white")
    fm = font("DMSans.ttf", 26, "Medium")
    for i, ln in enumerate(wrap(dr, tagline, fm, 1000, 2)):
        dr.text((60, 470 + i * 36), ln, font=fm, fill=(201, 214, 255))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
