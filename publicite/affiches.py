"""Affiches publicitaires Pixelrock — HTML rendu par Chromium."""
import asyncio, base64, io, pathlib, sys
import qrcode
from playwright.async_api import async_playwright
from common import font_css, mark, BASE

OUT = pathlib.Path(__file__).parent / "out"
OUT.mkdir(exist_ok=True)

SITE = "pixelrock.net"
TEL = "581 574-8553"


def qr_data_uri(url="https://pixelrock.net", fg="#202328", bg="#E3E2DD"):
    q = qrcode.QRCode(border=1, box_size=12, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url)
    q.make(fit=True)
    img = q.make_image(fill_color=fg, back_color=bg).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def page(css, body, cls=""):
    return f"""<!doctype html><html lang="fr-CA"><head><meta charset="utf-8">
<style>{font_css()}{BASE}{css}</style></head><body class="{cls}">{body}</body></html>"""


# --------------------------------------------------------------- 1. carré 1080

CARRE = """
body{width:1080px;height:1080px;position:relative}
.cadre{position:absolute;inset:0;padding:88px 92px;display:flex;flex-direction:column;
  justify-content:space-between}
.tete{display:flex;align-items:center;gap:22px}
.tete .mark{width:38px;height:54px;color:var(--accent)}
.nom{font-family:var(--font-display);font-weight:800;font-size:34px;letter-spacing:.06em;
  text-transform:uppercase}
.eyebrow{font-size:22px;margin-bottom:30px}
h1{font-size:112px}
.lede{font-family:var(--font-body);font-size:34px;line-height:1.45;color:var(--ink-2);
  margin-top:34px;max-width:20ch}
.points{display:flex;gap:0;margin-top:46px;border-top:2px solid var(--ink)}
.point{flex:1;padding:26px 22px 0 0;font-family:var(--font-display);font-weight:700;
  font-size:25px;line-height:1.25}
.point span{display:block;font-family:var(--font-mono);font-weight:400;font-size:17px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:12px}
.pied{display:flex;align-items:flex-end;justify-content:space-between;gap:30px}
.coord{font-family:var(--font-mono);font-size:26px;line-height:1.7;letter-spacing:.02em}
.coord strong{font-family:var(--font-display);font-weight:800;font-size:34px;letter-spacing:0;
  display:block;margin-bottom:6px}
.qr{width:150px;height:150px;border:2px solid var(--ink)}
"""

CARRE_BODY = f"""<div class="grille"></div><div class="cadre">
  <div class="tete">{mark()}<p class="nom">Pixelrock</p></div>
  <div>
    <p class="eyebrow">Saguenay — Lac-Saint-Jean</p>
    <h1>Des sites web<br>bâtis sur <span class="acc">le roc</span>.</h1>
    <p class="lede">Vos clients vous cherchent sur Google. Il faut qu'ils vous trouvent.</p>
    <div class="points">
      <div class="point"><span>Prix fixe</span>Annoncé avant<br>de commencer</div>
      <div class="point"><span>1 à 2 semaines</span>Pour un site<br>de prestataire</div>
      <div class="point"><span>À vous</span>Le domaine,<br>le code, les accès</div>
    </div>
  </div>
  <div class="pied">
    <p class="coord"><strong>{SITE}</strong>{TEL} · Premier rendez-vous gratuit</p>
    <img class="qr" src="{qr_data_uri()}" alt="">
  </div>
</div>"""


# --------------------------------------------------------------- 2. story 1080×1920

STORY = """
body{width:1080px;height:1920px;position:relative}
.cadre{position:absolute;inset:0;padding:150px 96px 130px;display:flex;flex-direction:column;
  justify-content:space-between}
.tete{display:flex;align-items:center;gap:24px}
.tete .mark{width:44px;height:62px;color:var(--accent-clair)}
.nom{font-family:var(--font-display);font-weight:800;font-size:38px;letter-spacing:.06em;
  text-transform:uppercase}
.eyebrow{font-size:26px;margin-bottom:40px}
h1{font-size:130px}
.lede{font-family:var(--font-body);font-size:40px;line-height:1.45;color:#B9BCC2;
  margin-top:46px;max-width:19ch}
.liste{margin-top:70px;border-top:2px solid #3A3F47}
.liste div{padding:34px 0;border-bottom:2px solid #3A3F47;display:flex;align-items:baseline;gap:28px;
  font-family:var(--font-display);font-weight:700;font-size:38px}
.liste em{font-family:var(--font-mono);font-style:normal;font-weight:400;font-size:24px;
  color:var(--accent-clair);letter-spacing:.1em}
.pied{text-align:left}
.pied .url{font-family:var(--font-display);font-weight:800;font-size:66px;letter-spacing:-.02em}
.pied .tel{font-family:var(--font-mono);font-size:32px;color:#B9BCC2;margin-top:18px;
  letter-spacing:.04em}
.ruban{display:inline-block;margin-bottom:44px;background:var(--accent-clair);color:#16181B;
  font-family:var(--font-display);font-weight:800;font-size:32px;padding:20px 32px;
  letter-spacing:.01em}
"""

STORY_BODY = f"""<div class="grille"></div><div class="cadre">
  <div>
    <div class="tete">{mark()}<p class="nom">Pixelrock</p></div>
    <p class="eyebrow" style="margin-top:64px">Conception de sites web</p>
    <h1>Des sites<br>web bâtis<br>sur <span class="acc">le roc</span>.</h1>
    <p class="lede">Pour les prestataires et les PME du Saguenay–Lac-Saint-Jean.</p>
  </div>
  <div class="liste">
    <div><em>01</em>Prix fixe, écrit d'avance</div>
    <div><em>02</em>Livré en 1 à 2 semaines</div>
    <div><em>03</em>Le site vous appartient</div>
  </div>
  <div class="pied">
    <span class="ruban">Premier rendez-vous gratuit</span>
    <p class="url">{SITE}</p>
    <p class="tel">{TEL} · réponse sous 24 h</p>
  </div>
</div>"""


# --------------------------------------------------------------- 3. forfaits 1080×1350

FORFAITS = """
body{width:1080px;height:1350px;position:relative}
.cadre{position:absolute;inset:0;padding:80px 80px 74px;display:flex;flex-direction:column}
.tete{display:flex;align-items:center;justify-content:space-between}
.marque{display:flex;align-items:center;gap:20px}
.marque .mark{width:34px;height:48px;color:var(--accent)}
.nom{font-family:var(--font-display);font-weight:800;font-size:30px;letter-spacing:.06em;
  text-transform:uppercase}
.lieu{font-family:var(--font-mono);font-size:20px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-2)}
h1{font-size:76px;margin-top:56px}
.sous{font-family:var(--font-body);font-size:30px;color:var(--ink-2);margin-top:24px;max-width:34ch}
.cartes{margin-top:56px;display:flex;flex-direction:column;gap:26px}
.carte{background:var(--paper-raised);border:2px solid var(--ink);box-shadow:12px 12px 0 var(--ink);
  padding:34px 38px;display:flex;align-items:center;justify-content:space-between;gap:30px}
.carte h3{font-size:42px}
.carte p{font-family:var(--font-mono);font-size:21px;color:var(--ink-2);margin-top:12px;
  letter-spacing:.02em}
.carte .prix{font-family:var(--font-display);font-weight:800;font-size:52px;white-space:nowrap;
  color:var(--accent);text-align:right}
.carte .prix small{display:block;font-family:var(--font-mono);font-weight:400;font-size:18px;
  color:var(--ink-2);letter-spacing:.1em;text-transform:uppercase;margin-top:10px}
.pied{margin-top:auto;display:flex;align-items:flex-end;justify-content:space-between;gap:28px;
  border-top:2px solid var(--ink);padding-top:32px}
.pied .url{font-family:var(--font-display);font-weight:800;font-size:46px}
.pied .tel{font-family:var(--font-mono);font-size:23px;color:var(--ink-2);margin-top:12px}
.qr{width:130px;height:130px;border:2px solid var(--ink)}
"""

FORFAITS_BODY = f"""<div class="grille"></div><div class="cadre">
  <div class="tete">
    <div class="marque">{mark()}<p class="nom">Pixelrock</p></div>
    <p class="lieu">Saguenay · Québec</p>
  </div>
  <h1>Trois façons de <span class="acc">bâtir</span>.</h1>
  <p class="sous">Prix fixe et date de livraison écrits après un premier rendez-vous de trente minutes. Sans engagement.</p>
  <div class="cartes">
    <div class="carte">
      <div><h3>Le Socle</h3><p>Travailleurs autonomes et prestataires · 1 à 2 semaines</p></div>
      <p class="prix">700 $<small>à partir de</small></p>
    </div>
    <div class="carte">
      <div><h3>L'Assise</h3><p>PME établies · 3 à 4 semaines</p></div>
      <p class="prix">2 500 $<small>à partir de</small></p>
    </div>
    <div class="carte">
      <div><h3>Le Chantier</h3><p>Application, outil interne, plateforme sur mesure</p></div>
      <p class="prix">Sur devis<small>après rendez-vous</small></p>
    </div>
  </div>
  <div class="pied">
    <div><p class="url">{SITE}</p><p class="tel">{TEL} · gloditambwe1@gmail.com</p></div>
    <img class="qr" src="{qr_data_uri()}" alt="">
  </div>
</div>"""


# --------------------------------------------------------------- 4. dépliant lettre

DEPLIANT = """
@page{size:8.5in 11in;margin:0}
body{width:816px;height:1056px;position:relative}
.grille{background-size:68px 68px;opacity:.22}
.cadre{position:absolute;inset:0;padding:56px 64px 48px;display:flex;flex-direction:column}
.tete{display:flex;align-items:center;justify-content:space-between}
.marque{display:flex;align-items:center;gap:16px}
.marque .mark{width:26px;height:37px;color:var(--accent)}
.nom{font-family:var(--font-display);font-weight:800;font-size:23px;letter-spacing:.06em;
  text-transform:uppercase}
.lieu{font-family:var(--font-mono);font-size:14px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-2)}
h1{font-size:46px;margin-top:34px}
.sous{font-family:var(--font-body);font-size:18px;line-height:1.5;color:var(--ink-2);
  margin-top:16px;max-width:56ch}
h2{font-family:var(--font-mono);font-weight:400;font-size:13px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--accent);margin-top:32px;padding-bottom:9px;
  border-bottom:2px solid var(--ink)}
.rangee{display:flex;gap:22px;margin-top:22px}
.f{flex:1;border:2px solid var(--ink);background:var(--paper-raised);padding:20px 20px 22px;
  box-shadow:7px 7px 0 var(--ink)}
.f h3{font-size:25px}
.f .tag{font-family:var(--font-mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-2);margin-top:8px;min-height:2.6em;line-height:1.3}
.f .prix{font-family:var(--font-display);font-weight:800;font-size:30px;color:var(--accent);
  margin-top:14px}
.f .prix small{display:block;font-family:var(--font-mono);font-weight:400;font-size:12px;
  color:var(--ink-2);letter-spacing:.06em;margin-top:6px}
.etapes{display:flex;gap:20px;margin-top:22px}
.e{flex:1}
.e span{font-family:var(--font-mono);font-size:13px;letter-spacing:.12em;color:var(--accent)}
.e h4{font-family:var(--font-display);font-weight:700;font-size:18px;margin-top:8px}
.e p{font-family:var(--font-body);font-size:14px;line-height:1.45;color:var(--ink-2);margin-top:6px}
.deja{margin-top:26px;border:2px solid var(--ink);padding:18px 22px;display:flex;
  align-items:center;gap:18px;flex-wrap:wrap}
.deja b{font-family:var(--font-display);font-weight:700;font-size:16px}
.deja span{font-family:var(--font-mono);font-size:15px;color:var(--ink-2);letter-spacing:.02em}
.pied{margin-top:auto;border-top:2px solid var(--ink);padding-top:20px;display:flex;
  align-items:flex-end;justify-content:space-between;gap:24px}
.pied .url{font-family:var(--font-display);font-weight:800;font-size:34px}
.pied .tel{font-family:var(--font-mono);font-size:16px;color:var(--ink-2);margin-top:10px;
  line-height:1.6}
.qr{width:108px;height:108px;border:2px solid var(--ink)}
"""

DEPLIANT_BODY = f"""<div class="grille"></div><div class="cadre">
  <div class="tete">
    <div class="marque">{mark()}<p class="nom">Pixelrock</p></div>
    <p class="lieu">Conception de sites web · Saguenay</p>
  </div>
  <h1>Des sites web bâtis sur <span class="acc">le roc</span>.</h1>
  <p class="sous">Vos clients vous cherchent sur Google avant de vous appeler. Je bâtis le site qui les convainc — prix fixe, date de livraison écrite, et vous parlez directement à la personne qui code.</p>

  <h2>Les forfaits</h2>
  <div class="rangee">
    <div class="f"><h3>Le Socle</h3><p class="tag">Travailleurs autonomes et prestataires de services</p>
      <p class="prix">700 $<small>À PARTIR DE · 1 À 2 SEMAINES</small></p></div>
    <div class="f"><h3>L'Assise</h3><p class="tag">PME établies, structure sur mesure</p>
      <p class="prix">2 500 $<small>À PARTIR DE · 3 À 4 SEMAINES</small></p></div>
    <div class="f"><h3>Le Chantier</h3><p class="tag">Application, outil interne, plateforme</p>
      <p class="prix">Sur devis<small>APRÈS UN PREMIER RENDEZ-VOUS</small></p></div>
  </div>

  <h2>Comment ça se passe</h2>
  <div class="etapes">
    <div class="e"><span>01</span><h4>Le rendez-vous</h4><p>Trente minutes, gratuit, chez vous ou en visioconférence.</p></div>
    <div class="e"><span>02</span><h4>Le devis</h4><p>Un prix fixe et une date, par écrit. Ce qui est inclus, et ce qui ne l'est pas.</p></div>
    <div class="e"><span>03</span><h4>La construction</h4><p>Un lien d'aperçu dès le premier jour. Vous commentez au fur et à mesure.</p></div>
    <div class="e"><span>04</span><h4>La mise en ligne</h4><p>Une heure de formation. Vous repartez avec le domaine, le code et les accès.</p></div>
  </div>

  <div class="deja">
    <b>Déjà en ligne&nbsp;:</b>
    <span>gnosislearn.com · zaryaonline.ca · kibilabel.ca</span>
  </div>

  <div class="pied">
    <div>
      <p class="url">pixelrock.net</p>
      <p class="tel">581 574-8553 · gloditambwe1@gmail.com<br>Réponse sous 24 h, 7 jours sur 7</p>
    </div>
    <img class="qr" src="{qr_data_uri()}" alt="">
  </div>
</div>"""


AFFICHES = [
    ("affiche-carre-1080x1080", CARRE, CARRE_BODY, "", 1080, 1080, False),
    ("affiche-story-1080x1920", STORY, STORY_BODY, "sombre", 1080, 1920, False),
    ("affiche-forfaits-1080x1350", FORFAITS, FORFAITS_BODY, "", 1080, 1350, False),
    ("depliant-lettre", DEPLIANT, DEPLIANT_BODY, "", 816, 1056, True),
]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        for name, css, body, cls, w, h, pdf in AFFICHES:
            html = page(css, body, cls)
            f = OUT / (name + ".html")
            f.write_text(html, encoding="utf-8")
            ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2)
            pg = await ctx.new_page()
            await pg.goto(f.as_uri())
            await pg.wait_for_timeout(600)
            await pg.screenshot(path=str(OUT / (name + ".png")))
            if pdf:
                ctx2 = await b.new_context(viewport={"width": w, "height": h})
                pg2 = await ctx2.new_page()
                await pg2.goto(f.as_uri())
                await pg2.wait_for_timeout(500)
                await pg2.pdf(path=str(OUT / (name + ".pdf")), width="8.5in", height="11in",
                              print_background=True, margin={"top": "0", "bottom": "0",
                                                             "left": "0", "right": "0"})
                await ctx2.close()
            await ctx.close()
            print("ok", name)
        await b.close()

asyncio.run(main())
