"""Gera a prévia (_previa/) a partir de _site/, com links relativos, para publicar como artifact no Claude.
Uso: python3 build.py && python3 previa.py
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC, OUT = ROOT / "_site", ROOT / "_previa"
ATTR = re.compile(r'''((?:href|src|action|content)=["'])(/[^"'#?]*)([^"']*["'])''')
JS = re.compile(r'''(["'`])(/(?:busca\.json|static/[^"'`]*|[a-z0-9-]+/[^"'`]*))(["'`])''')


def rel(target, depth):
    if target.startswith("//"):
        return target
    path = target.lstrip("/")
    if path == "" or path.endswith("/"):
        path += "index.html"
    return "../" * depth + path


def convert(html, depth):
    html = ATTR.sub(lambda m: m.group(1) + rel(m.group(2), depth) + m.group(3)
                    if not m.group(1).startswith("content") else m.group(0), html)
    html = re.sub(r'srcset="([^"]*)"', lambda m: 'srcset="' + re.sub(
        r'(^|,\s*)(/[^\s,]+)', lambda n: n.group(1) + rel(n.group(2), depth), m.group(1)) + '"', html)
    html = JS.sub(lambda m: m.group(1) + rel(m.group(2), depth) + m.group(3), html)
    return html


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT, ignore=lambda d, n: [x for x in n if (d.endswith("static/img") and x == "drops") or (d.endswith("static") and x == "og")])
    for f in OUT.rglob("*.html"):
        depth = len(f.relative_to(OUT).parts) - 1
        f.write_text(convert(f.read_text(encoding="utf-8"), depth), encoding="utf-8")
    print("Prévia gerada em _previa/")


if __name__ == "__main__":
    main()
