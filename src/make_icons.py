#!/usr/bin/env python3
"""
Génère les icônes de Pixelrock à partir de la grille du logo.

Le pilier garde le gris foncé de la marque (#202328) sur fond grès (#E3E2DD).
L'orange est réservé aux pages du site, où il doit rester visible sur les deux thèmes.

    python3 src/make_icons.py
"""

from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent.parent
OUT = ROOT / "src" / "assets"

INK = (32, 35, 40, 255)      # #202328 — le pilier
PAPER = (227, 226, 221, 255)  # #E3E2DD — le grès

# grille du logo : module 12, bloc 10, 5 colonnes sur 7 rangées
BLOCKS = (
    [(x, 0) for x in (0, 12, 24, 36, 48)]
    + [(x, 12) for x in (12, 24, 36)]
    + [(x, y) for y in (24, 36, 48, 60) for x in (18, 30)]
    + [(x, 72) for x in (0, 12, 24, 36, 48)]
)
MARK_W, MARK_H = 58, 82


def render(size, scale, bg=PAPER, fg=INK, supersample=8):
    """Dessine le pilier centré, occupant `scale` de la hauteur du canevas.

    bg=None laisse le fond transparent (favicons de navigateur).
    """
    s = size * supersample
    img = Image.new("RGBA", (s, s), bg if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    unit = (s * scale) / MARK_H          # taille d'une unité de la grille
    mw, mh = MARK_W * unit, MARK_H * unit
    ox, oy = (s - mw) / 2, (s - mh) / 2

    for bx, by in BLOCKS:
        x0, y0 = ox + bx * unit, oy + by * unit
        d.rectangle([x0, y0, x0 + 10 * unit, y0 + 10 * unit], fill=fg)

    return img.resize((size, size), Image.LANCZOS)


def svg_favicon():
    """Favicon sans fond, pilier gris foncé de la marque (#202328)."""
    rects = "".join(
        f'<rect x="{x}" y="{y}" width="10" height="10"/>' for x, y in BLOCKS
    )
    # 58x82 centré dans un carré de 100x100 : décalage x=21, y=9
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        f'<g fill="#202328" transform="translate(21 9)">{rects}</g>'
        "</svg>"
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # aplatir le logo GNOSIS sur son marron principal : plus de coins blancs
    g = OUT / "gnosis.png"
    if g.exists():
        src = Image.open(g).convert("RGBA")
        flat = Image.new("RGBA", src.size, (138, 90, 30, 255))
        flat.alpha_composite(src)
        flat.convert("RGB").save(g)
        print("  gnosis.png aplati sur #8A5A1E")

    # favicons de navigateur : aucun fond
    jobs_transparent = [
        ("favicon-16.png", 16, 0.86),
        ("favicon-32.png", 32, 0.86),
        ("favicon-48.png", 48, 0.86),
    ]
    for name, size, scale in jobs_transparent:
        render(size, scale, bg=None).save(OUT / name)
        print(f"  {name} ({size}px, sans fond)")

    # icônes d'application : fond plein, iOS et Android ne gèrent pas la transparence
    jobs_solid = [
        ("apple-touch-icon.png", 180, 0.62),   # iOS rogne les coins
        ("icon-192.png", 192, 0.68),
        ("icon-512.png", 512, 0.68),
        ("icon-maskable-512.png", 512, 0.46),  # zone sûre Android : 80 % du canevas
    ]
    for name, size, scale in jobs_solid:
        render(size, scale).convert("RGB").save(OUT / name)
        print(f"  {name} ({size}px)")

    ico = render(48, 0.86, bg=None)
    ico.save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("  favicon.ico (sans fond)")

    (OUT / "favicon.svg").write_text(svg_favicon(), encoding="utf-8")
    print("  favicon.svg")


if __name__ == "__main__":
    main()
