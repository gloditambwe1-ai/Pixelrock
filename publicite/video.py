"""Vidéos publicitaires Pixelrock.

Le mouvement est piloté image par image : la page expose une fonction
render(t) et Chromium en capture 25 par seconde. Rien n'est laissé au hasard,
la vidéo est donc exactement reproductible."""
import asyncio, pathlib, shutil, subprocess, sys
from playwright.async_api import async_playwright
from common import font_css, mark, BASE

ICI = pathlib.Path(__file__).parent
OUT = ICI / "out"
OUT.mkdir(exist_ok=True)

FPS = 25
DUREE = 16.4

CSS = """
html,body{width:100%;height:100%}
body{background:#16181B;color:#EDECE8;position:relative}
.acc{color:var(--accent-clair)}
.eyebrow{color:var(--accent-clair)}
.grille{background-image:linear-gradient(to right,#2C3037 1px,transparent 1px),
   linear-gradient(to bottom,#2C3037 1px,transparent 1px);opacity:.75}
.scene{position:absolute;inset:0;overflow:hidden}
.grille{background-size:var(--maille) var(--maille)}
.bloc{position:absolute;left:var(--pad);right:var(--pad);top:0;bottom:0;
  display:flex;flex-direction:column;justify-content:center;align-items:flex-start;
  opacity:0;will-change:transform,opacity}
.bloc > *{width:100%}
.ruban{align-self:flex-start;width:auto !important}

/* 1 — la marque se pose, pièce par pièce */
.marque{display:flex;align-items:center;gap:calc(var(--gap)*1.6);opacity:1}
.marque .mark{width:var(--markw);height:auto;color:var(--accent-clair)}
.marque .mark rect{opacity:0}
.marque .nom{font-family:var(--font-display);font-weight:800;letter-spacing:.07em;
  text-transform:uppercase;font-size:var(--nom);opacity:0;white-space:nowrap}

h1{font-size:var(--h1);line-height:1.03}
.lede{font-family:var(--font-body);font-size:var(--lede);line-height:1.4;color:#B9BCC2;
  margin-top:var(--sp)}
.liste div{display:flex;align-items:baseline;gap:calc(var(--sp)*.8);
  font-family:var(--font-display);font-weight:700;font-size:var(--pt);
  padding:calc(var(--sp)*.55) 0;border-bottom:2px solid #3A3F47;opacity:0}
.liste em{font-family:var(--font-mono);font-style:normal;font-weight:400;font-size:var(--num);
  color:var(--accent-clair);letter-spacing:.1em}
.url{font-family:var(--font-display);font-weight:800;font-size:var(--url);letter-spacing:-.02em}
.tel{font-family:var(--font-mono);font-size:var(--tel);color:#B9BCC2;margin-top:calc(var(--sp)*.5)}
.ruban{display:inline-block;background:var(--accent-clair);color:#16181B;
  font-family:var(--font-display);font-weight:800;font-size:var(--ruban);
  padding:calc(var(--sp)*.42) calc(var(--sp)*.7);margin-bottom:var(--sp)}
.trait{height:3px;background:var(--accent-clair);width:0;margin-top:var(--sp)}

.story{--pad:96px;--maille:108px;--gap:26px;--markw:112px;--nom:70px;--h1:112px;--lede:40px;
  --sp:44px;--pt:40px;--num:26px;--url:72px;--tel:31px;--ruban:34px}
.carre{--pad:88px;--maille:96px;--gap:24px;--markw:96px;--nom:60px;--h1:96px;--lede:36px;
  --sp:36px;--pt:36px;--num:24px;--url:64px;--tel:28px;--ruban:31px}
"""

BODY = f"""<div class="grille"></div>
<div class="scene">
  <div class="bloc" id="b1" style="opacity:1">
    <div class="marque">{mark("mark", ids=True)}<p class="nom" id="nom">Pixelrock</p></div>
  </div>

  <div class="bloc" id="b2">
    <h1><span class="l" id="h1a">Des sites web</span><br><span class="l" id="h1b">bâtis sur <span class="acc">le roc</span>.</span></h1>
    <p class="lede" id="h1c">Conception de sites web au Saguenay–Lac-Saint-Jean.</p>
  </div>

  <div class="bloc" id="b3">
    <p class="eyebrow" id="e3" style="font-size:var(--num);letter-spacing:.2em">Ce que vous obtenez</p>
    <div class="liste" style="margin-top:var(--sp)">
      <div id="p1"><em>01</em>Prix fixe, écrit d'avance</div>
      <div id="p2"><em>02</em>Livré en 1 à 2 semaines</div>
      <div id="p3"><em>03</em>Le site vous appartient</div>
    </div>
  </div>

  <div class="bloc" id="b4">
    <span class="ruban" id="r4">Premier rendez-vous gratuit</span>
    <p class="url">pixelrock.net</p>
    <p class="tel">581 574-8553 · réponse sous 24 h, 7 jours sur 7</p>
    <div class="trait" id="t4"></div>
  </div>
</div>

<script>
var E = function (id) {{ return document.getElementById(id); }};
function clamp(x) {{ return x < 0 ? 0 : x > 1 ? 1 : x; }}
function ease(x) {{ x = clamp(x); return 1 - Math.pow(1 - x, 3); }}
/* apparition : de bas en haut, sans rebond */
function monte(el, t, t0, d, dist) {{
  var k = ease((t - t0) / d);
  el.style.opacity = k;
  el.style.transform = 'translateY(' + ((1 - k) * (dist === undefined ? 26 : dist)) + 'px)';
}}
/* disparition douce d'un bloc entier */
function sort(el, t, t0, d) {{
  var k = ease((t - t0) / d);
  el.style.opacity = 1 - k;
  el.style.transform = 'translateY(' + (-k * 22) + 'px)';
}}

var RECTS = document.querySelectorAll('.marque .mark rect');

window.render = function (t) {{
  /* ---- scène 1 : la marque (0 → 4.4 s) ---- */
  var b1 = E('b1');
  RECTS.forEach(function (r, i) {{
    var k = ease((t - (0.25 + i * 0.055)) / 0.5);
    r.style.opacity = k;
    r.style.transform = 'translateY(' + ((1 - k) * -9) + 'px)';
    r.style.transformBox = 'fill-box';
  }});
  monte(E('nom'), t, 1.5, 0.9, 16);
  if (t > 3.7) sort(b1, t, 3.7, 0.7); else {{ b1.style.opacity = 1; b1.style.transform = 'none'; }}

  /* ---- scène 2 : la promesse (4.3 → 8.6 s) ---- */
  var b2 = E('b2');
  b2.style.opacity = t > 4.3 ? 1 : 0;
  monte(E('h1a'), t, 4.4, 0.85, 34);
  monte(E('h1b'), t, 4.7, 0.85, 34);
  monte(E('h1c'), t, 5.3, 0.9, 26);
  if (t > 8.0) sort(b2, t, 8.0, 0.7);

  /* ---- scène 3 : les trois arguments (8.6 → 12.9 s) ---- */
  var b3 = E('b3');
  b3.style.opacity = t > 8.6 ? 1 : 0;
  monte(E('e3'), t, 8.7, 0.7, 18);
  monte(E('p1'), t, 9.2, 0.75, 24);
  monte(E('p2'), t, 9.8, 0.75, 24);
  monte(E('p3'), t, 10.4, 0.75, 24);
  if (t > 12.3) sort(b3, t, 12.3, 0.7);

  /* ---- scène 4 : où me joindre (12.9 s → fin) ---- */
  var b4 = E('b4');
  b4.style.opacity = t > 12.9 ? 1 : 0;
  monte(E('r4'), t, 13.0, 0.7, 20);
  monte(b4.querySelector('.url'), t, 13.3, 0.8, 28);
  monte(b4.querySelector('.tel'), t, 13.7, 0.8, 22);
  E('t4').style.width = (ease((t - 14.0) / 1.4) * 100) + '%';

  /* fondu au noir tout à la fin */
  document.body.style.filter = t > 15.9 ? 'brightness(' + (1 - clamp((t - 15.9) / 0.5)) + ')' : 'none';
}};
window.render(0);
</script>"""


def html(cls):
    return (f"""<!doctype html><html lang="fr-CA"><head><meta charset="utf-8">
<style>{font_css()}{BASE}{CSS}</style></head><body class="{cls}">{BODY}</body></html>""")


FORMATS = [
    ("video-story-1080x1920", "story", 1080, 1920),
    ("video-carre-1080x1080", "carre", 1080, 1080),
]


async def frames(nom, cls, w, h):
    dossier = pathlib.Path("/tmp/frames") / nom
    if dossier.exists():
        shutil.rmtree(dossier)
    dossier.mkdir(parents=True)
    f = OUT / (nom + ".html")
    f.write_text(html(cls), encoding="utf-8")
    n = int(DUREE * FPS)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                                    args=["--force-device-scale-factor=1"])
        ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
        pg = await ctx.new_page()
        await pg.goto(f.as_uri())
        await pg.wait_for_timeout(700)
        for i in range(n):
            await pg.evaluate("t => window.render(t)", i / FPS)
            await pg.screenshot(path=str(dossier / f"{i:04d}.jpg"), type="jpeg", quality=94)
        await b.close()
    return dossier, n


def encode(nom, dossier):
    mp4 = OUT / (nom + ".mp4")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-framerate", str(FPS), "-i", str(dossier / "%04d.jpg"),
        "-i", str(OUT / "musique.wav"),
        "-c:v", "libx264", "-preset", "slow", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-shortest", str(mp4),
    ], check=True)
    return mp4


async def main():
    choix = sys.argv[1:] or [f[0] for f in FORMATS]
    for nom, cls, w, h in FORMATS:
        if nom not in choix:
            continue
        d, n = await frames(nom, cls, w, h)
        print(nom, n, "images")
        print("→", encode(nom, d))

asyncio.run(main())
