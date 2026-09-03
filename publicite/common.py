"""Éléments partagés par les affiches et les vidéos Pixelrock."""
import base64, pathlib

FONTS_DIR = pathlib.Path("/tmp/f/package/files")

FACES = [
    ("Archivo", 600, "archivo-latin-600-normal.woff2"),
    ("Archivo", 700, "archivo-latin-700-normal.woff2"),
    ("Archivo", 800, "archivo-latin-800-normal.woff2"),
    ("Newsreader", 400, "newsreader-latin-400-normal.woff2"),
    ("DM Mono", 400, "dm-mono-latin-400-normal.woff2"),
    ("DM Mono", 500, "dm-mono-latin-500-normal.woff2"),
]


def font_css():
    out = []
    for fam, w, f in FACES:
        b64 = base64.b64encode((FONTS_DIR / f).read_bytes()).decode()
        out.append(
            f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};"
            f"font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
        )
    return "\n".join(out)


MARK_RECTS = """<rect x="0" y="0" width="10" height="10"/><rect x="12" y="0" width="10" height="10"/><rect x="24" y="0" width="10" height="10"/><rect x="36" y="0" width="10" height="10"/><rect x="48" y="0" width="10" height="10"/>
<rect x="12" y="12" width="10" height="10"/><rect x="24" y="12" width="10" height="10"/><rect x="36" y="12" width="10" height="10"/>
<rect x="18" y="24" width="10" height="10"/><rect x="30" y="24" width="10" height="10"/>
<rect x="18" y="36" width="10" height="10"/><rect x="30" y="36" width="10" height="10"/>
<rect x="18" y="48" width="10" height="10"/><rect x="30" y="48" width="10" height="10"/>
<rect x="18" y="60" width="10" height="10"/><rect x="30" y="60" width="10" height="10"/>
<rect x="0" y="72" width="10" height="10"/><rect x="12" y="72" width="10" height="10"/><rect x="24" y="72" width="10" height="10"/><rect x="36" y="72" width="10" height="10"/><rect x="48" y="72" width="10" height="10"/>"""


def mark(cls="mark", ids=False):
    rects = MARK_RECTS
    if ids:
        parts = rects.replace("\n", "").split("<rect")[1:]
        rects = "".join(f'<rect data-i="{i}"{p}' for i, p in enumerate(parts))
    return (f'<svg class="{cls}" viewBox="0 0 58 82" aria-hidden="true">{rects}</svg>')


BASE = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --paper:#E3E2DD; --paper-raised:#EDECE8; --ink:#202328; --ink-2:#4A4F57;
  --accent:#A63315; --accent-clair:#EC6E38; --line:#C9C7C0;
  --font-display:'Archivo',system-ui,sans-serif;
  --font-body:'Newsreader',Georgia,serif;
  --font-mono:'DM Mono',ui-monospace,monospace;
}
body{background:var(--paper);color:var(--ink);font-family:var(--font-body);
  -webkit-font-smoothing:antialiased;overflow:hidden}
.sombre{background:#16181B;color:#EDECE8}
.mark rect{fill:currentColor}
.grille{position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(to right,var(--line) 1px,transparent 1px),
                   linear-gradient(to bottom,var(--line) 1px,transparent 1px);
  background-size:96px 96px;opacity:.55}
.sombre .grille{background-image:linear-gradient(to right,#2C3037 1px,transparent 1px),
                   linear-gradient(to bottom,#2C3037 1px,transparent 1px);opacity:.75}
.eyebrow{font-family:var(--font-mono);text-transform:uppercase;letter-spacing:.22em;
  color:var(--accent)}
.sombre .eyebrow{color:var(--accent-clair)}
h1,h2,h3,.mot{font-family:var(--font-display);font-weight:800;letter-spacing:-.02em;line-height:1.02}
.acc{color:var(--accent)}
.sombre .acc{color:var(--accent-clair)}
"""
