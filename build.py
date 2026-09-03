#!/usr/bin/env python3
"""
Pixelrock — générateur du site statique bilingue.

    python3 build.py

Le français est la langue principale : ses pages sont à la racine.
L'anglais est une traduction complète, servie depuis /en/.

  src/pages/*.html      fragments français   → /*.html
  src/pages-en/*.html   fragments anglais    → /en/*.html (noms de fichiers traduits)
  src/styles.css                             → assets/styles.css
  src/app.js                                 → assets/app.js
  src/assets/*                               → assets/*

Produit aussi sitemap.xml, robots.txt, site.webmanifest, netlify.toml et preview.html.

Pour modifier la navigation, le pied de page ou les données de référencement : ce fichier.
Pour modifier le contenu d'une page : src/pages/<page>.html (ou src/pages-en/)
Pour modifier le style : src/styles.css
Pour régénérer les icônes : python3 src/make_icons.py
"""

import base64
import hashlib
import json
from datetime import datetime, timezone
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
ASSETS = SRC / "assets"
OUT = ROOT

SITE = "Pixelrock"
DOMAIN = "https://pixelrock.net"
EMAIL = "gloditambwe1@gmail.com"
TEL_HREF = "+15815748553"
TEL_TEXT = "581 574-8553"
VILLE = "Saguenay"
REGION = "QC"
PAYS = "CA"
GEO = ("48.4280", "-71.0680")

VILLES_DESSERVIES = [
    "Saguenay", "Chicoutimi", "Jonquière", "La Baie", "Alma",
    "Saint-Félicien", "Roberval", "Dolbeau-Mistassini", "Métabetchouan",
    "Saint-Ambroise", "Shipshaw", "Laterrière", "Saguenay–Lac-Saint-Jean", "Québec",
]

# nom de fichier français → nom de fichier anglais
SLUG_EN = {
    "index.html": "index.html",
    "services.html": "packages.html",
    "realisations.html": "work.html",
    "a-propos.html": "about.html",
    "contact.html": "contact.html",
    "merci.html": "thank-you.html",
    "projet-kibi-label.html": "project-kibi-label.html",
    "projet-gnosis.html": "project-gnosis.html",
    "projet-zarya.html": "project-zarya.html",
}

MARK_RECTS = """<rect x="0" y="0" width="10" height="10"/><rect x="12" y="0" width="10" height="10"/><rect x="24" y="0" width="10" height="10"/><rect x="36" y="0" width="10" height="10"/><rect x="48" y="0" width="10" height="10"/>
<rect x="12" y="12" width="10" height="10"/><rect x="24" y="12" width="10" height="10"/><rect x="36" y="12" width="10" height="10"/>
<rect x="18" y="24" width="10" height="10"/><rect x="30" y="24" width="10" height="10"/>
<rect x="18" y="36" width="10" height="10"/><rect x="30" y="36" width="10" height="10"/>
<rect x="18" y="48" width="10" height="10"/><rect x="30" y="48" width="10" height="10"/>
<rect x="18" y="60" width="10" height="10"/><rect x="30" y="60" width="10" height="10"/>
<rect x="0" y="72" width="10" height="10"/><rect x="12" y="72" width="10" height="10"/><rect x="24" y="72" width="10" height="10"/><rect x="36" y="72" width="10" height="10"/><rect x="48" y="72" width="10" height="10"/>"""

LANGS = {
    "fr": {
        "dir": "src/pages",
        "locale": "fr-CA",
        "og_locale": "fr_CA",
        "label": "FR",
        "nav": [
            ("accueil", "index.html", "Accueil"),
            ("services", "services.html", "Forfaits"),
            ("realisations", "realisations.html", "Réalisations"),
            ("apropos", "a-propos.html", "À propos"),
        ],
        "tabs": [
            ("accueil", "index.html", "Accueil"),
            ("services", "services.html", "Forfaits"),
            ("realisations", "realisations.html", "Projets"),
            ("apropos", "a-propos.html", "À propos"),
            ("contact", "contact.html", "Contact"),
        ],
        "tab_aria": "Navigation du site",
        "reglages_aria": "Langue et thème",
        "cta": "Prendre rendez-vous",
        "skip": "Aller au contenu",
        "brand_aria": "Pixelrock, accueil",
        "lang_aria": "Langue",
        "nav_aria": "Navigation principale",
        "menu_aria": "Menu",
        "theme": {
            "aria": "Thème",
            "titre": "Thème",
            "court": {"light": "Clair", "dark": "Sombre", "auto": "Système"},
            "long": {"light": "Clair", "dark": "Sombre", "auto": "Système"},
        },
        "band_title": "Un premier rendez-vous, ça ne coûte rien.",
        "band_text": "Trente minutes, sans engagement, chez vous ou en visioconférence. Réponse sous 24 heures, sept jours sur sept.",
        "foot_tagline": "Conception de sites web à Saguenay, pour le Saguenay–Lac-Saint-Jean et tout le Québec.",
        "foot_cols": ["Forfaits", "Réalisations", "Joindre"],
        "foot_links": [
            [("services.html#socle", "Le Socle"), ("services.html#assise", "L'Assise"),
             ("services.html#chantier", "Le Chantier"), ("services.html#processus", "Comment ça marche")],
            [("projet-kibi-label.html", "Kibi Label"), ("projet-gnosis.html", "GNOSIS"),
             ("projet-zarya.html", "Zarya"), ("a-propos.html", "À propos")],
        ],
        "foot_reply": "Réponse sous 24 h, 7 jours sur 7",
        "foot_legal": "© 2026 Pixelrock — Chicoutimi, Jonquière, La Baie, Alma et partout au Québec",
        "home_crumb": "Accueil",
        "crumbs": {
            "services.html": "Forfaits", "realisations.html": "Réalisations",
            "a-propos.html": "À propos", "contact.html": "Contact",
            "projet-kibi-label.html": "Kibi Label", "projet-gnosis.html": "GNOSIS",
            "projet-zarya.html": "Zarya",
        },
    },
    "en": {
        "dir": "src/pages-en",
        "locale": "en-CA",
        "og_locale": "en_CA",
        "label": "EN",
        "nav": [
            ("accueil", "index.html", "Home"),
            ("services", "services.html", "Packages"),
            ("realisations", "realisations.html", "Work"),
            ("apropos", "a-propos.html", "About"),
        ],
        "tabs": [
            ("accueil", "index.html", "Home"),
            ("services", "services.html", "Packages"),
            ("realisations", "realisations.html", "Work"),
            ("apropos", "a-propos.html", "About"),
            ("contact", "contact.html", "Contact"),
        ],
        "tab_aria": "Site navigation",
        "reglages_aria": "Language and theme",
        "cta": "Book a meeting",
        "skip": "Skip to content",
        "brand_aria": "Pixelrock, home",
        "lang_aria": "Language",
        "nav_aria": "Main navigation",
        "menu_aria": "Menu",
        "theme": {
            "aria": "Theme",
            "titre": "Theme",
            "court": {"light": "Light", "dark": "Dark", "auto": "System"},
            "long": {"light": "Light", "dark": "Dark", "auto": "System"},
        },
        "band_title": "A first meeting costs nothing.",
        "band_text": "Thirty minutes, no obligation, at your place or by video call. Reply within 24 hours, seven days a week.",
        "foot_tagline": "Web design in Saguenay, for Saguenay–Lac-Saint-Jean and all of Quebec.",
        "foot_cols": ["Packages", "Work", "Contact"],
        "foot_links": [
            [("services.html#socle", "The Base"), ("services.html#assise", "The Foundation"),
             ("services.html#chantier", "The Build"), ("services.html#processus", "How it works")],
            [("projet-kibi-label.html", "Kibi Label"), ("projet-gnosis.html", "GNOSIS"),
             ("projet-zarya.html", "Zarya"), ("a-propos.html", "About")],
        ],
        "foot_reply": "Reply within 24 h, 7 days a week",
        "foot_legal": "© 2026 Pixelrock — Chicoutimi, Jonquière, La Baie, Alma and anywhere in Quebec",
        "home_crumb": "Home",
        "crumbs": {
            "services.html": "Packages", "realisations.html": "Work",
            "a-propos.html": "About", "contact.html": "Contact",
            "projet-kibi-label.html": "Kibi Label", "projet-gnosis.html": "GNOSIS",
            "projet-zarya.html": "Zarya",
        },
    },
}

# Noms de fichiers portant l'empreinte du contenu.
# Sans ça, une feuille de style mise en cache pour un an continue d'être servie
# alors que le HTML, lui, a changé : la page s'affiche à moitié stylée.
ASSETS_VERSIONNES = {"css": "styles.css", "js": "app.js"}


def empreinte(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:10]


# posé avant le premier rendu : évite tout clignotement de thème
BOOT = (
    '<script>(function(){var d=document.documentElement;d.classList.add("js");'
    'try{var t=localStorage.getItem("pixelrock-theme");'
    'if(t==="light"||t==="dark")d.setAttribute("data-theme",t);}catch(e){}})();</script>'
)

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Archivo:wght@500;600;700;800&family=DM+Mono:wght@400;500&"
    'family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap">'
)


# ----------------------------------------------------------------- adresses

def out_name(lang, fr_name):
    return fr_name if lang == "fr" else SLUG_EN[fr_name]


def url_of(lang, fr_name):
    name = out_name(lang, fr_name)
    base = "/" if lang == "fr" else "/en/"
    return base if name == "index.html" else base + name


def prefix(lang):
    """chemin relatif vers la racine du site"""
    return "" if lang == "fr" else "../"


def mark_svg(cls):
    return (
        f'<svg class="mark {cls}" viewBox="0 0 58 82" aria-hidden="true" focusable="false">'
        f"{MARK_RECTS}</svg>"
    )


def lang_switch(lang, fr_name):
    out = ['<div class="lang" role="group" aria-label="' + LANGS[lang]["lang_aria"] + '">']
    for code in ("fr", "en"):
        label = LANGS[code]["label"]
        if code == lang:
            out.append(f'<span aria-current="true">{label}</span>')
        else:
            # depuis le français on descend dans en/, depuis l'anglais on remonte
            href = ("en/" + out_name("en", fr_name)) if code == "en" else ("../" + fr_name)
            out.append(f'<a href="{href}" hreflang="{LANGS[code]["locale"]}" lang="{code}">{label}</a>')
    out.append("</div>")
    return "".join(out)


def theme_options(lang, inline=False):
    """Les trois choix, en toutes lettres. Sans JavaScript ils ne servent à rien :
    la CSS ne les affiche que si le script a posé la classe js.

    En ligne, les séparateurs sont des éléments à part : cliquer un point
    ne doit pas changer le thème."""
    T = LANGS[lang]["theme"]
    morceaux = []
    for i, cle in enumerate(("light", "dark", "auto")):
        if inline and i:
            morceaux.append('<span class="theme-sep" aria-hidden="true">·</span>')
        morceaux.append(
            f'<button type="button" data-theme-choice="{cle}" data-court="{T["court"][cle]}"'
            f' aria-pressed="false">{T["long"][cle]}</button>'
        )
    return "".join(morceaux)


def theme_switch(lang):
    """Barre de navigation : un menu déroulant qui montre le thème courant."""
    T = LANGS[lang]["theme"]
    return f"""<details class="theme">
        <summary class="theme__btn" aria-label="{T['aria']}">
          <span class="theme__icon" aria-hidden="true"></span>
          <span class="theme__now">{T['court']['auto']}</span>
        </summary>
        <div class="theme__menu" role="group" aria-label="{T['aria']}">{theme_options(lang)}</div>
      </details>"""


def theme_block(lang):
    """Menu mobile : les trois choix sur une seule ligne, juste sous le bouton
    de rendez-vous. Du texte, rien d'autre."""
    T = LANGS[lang]["theme"]
    return (f'<div class="theme-choix" role="group" aria-label="{T["aria"]}">'
            f'{theme_options(lang, inline=True)}</div>')


# Icônes de la barre du bas : tracées à angles droits, sans arrondi,
# pour rester dans la même famille que le pilier de la marque.
TAB_ICONS = {
    "accueil": '<path d="M3 11 12 3l9 8"/><path d="M5.5 10.5V20h13v-9.5"/><path d="M10 20v-5h4v5"/>',
    "services": '<path d="M3 4h18v5H3z"/><path d="M3 12h18v3H3z"/><path d="M3 18h18v3H3z"/>',
    "realisations": '<path d="M3 3h7v7H3z"/><path d="M14 3h7v7h-7z"/><path d="M3 14h7v7H3z"/><path d="M14 14h7v7h-7z"/>',
    "apropos": '<path d="M8 3h8v8H8z"/><path d="M3 21v-3h18v3"/>',
    "contact": '<path d="M3 5h18v14H3z"/><path d="m3 6 9 7 9-7"/>',
}


def tab_icon(key):
    return (
        '<svg class="tabbar__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false" '
        'fill="none" stroke="currentColor" stroke-width="1.8">'
        f'{TAB_ICONS[key]}</svg>'
    )


def tabbar(lang, current, fr_name):
    """Sur téléphone, la navigation vit en bas de l'écran, sous le pouce.
    Elle double la barre du haut sur grand écran, où elle est masquée."""
    L = LANGS[lang]
    items = []
    for key, href, label in L["tabs"]:
        cur = ' aria-current="page"' if key == current else ""
        mod = ' class="tabbar__link tabbar__link--cta"' if key == "contact" else ' class="tabbar__link"'
        items.append(
            f'<a href="{out_name(lang, href)}"{mod}{cur}>{tab_icon(key)}'
            f'<span class="tabbar__mot">{label}</span></a>'
        )
    return (f'<nav class="tabbar" aria-label="{L["tab_aria"]}">'
            f'<div class="tabbar__inner">{"".join(items)}</div></nav>')


def nav_html(lang, current, fr_name):
    L = LANGS[lang]
    links = []
    for key, href, label in L["nav"]:
        cur = ' aria-current="page"' if key == current else ""
        links.append(f'<a href="{out_name(lang, href)}"{cur}>{label}</a>')
    return f"""<header class="nav">
  <div class="wrap nav__inner">
    <a class="brand" href="{out_name(lang, 'index.html')}" aria-label="{L['brand_aria']}">
      {mark_svg("brand__mark")}
      <span class="brand__name">{SITE}</span>
    </a>
    <nav class="nav__links" aria-label="{L['nav_aria']}">
      {chr(10).join("      " + l for l in links).strip()}
    </nav>
    <div class="nav__end">
      {theme_switch(lang)}
      {lang_switch(lang, fr_name)}
      <a class="nav__cta" href="{out_name(lang, 'contact.html')}">{L['cta']}</a>
      <details class="menu">
        <summary class="menu__btn" aria-label="{L['reglages_aria']}"><span class="menu__bars" aria-hidden="true"></span></summary>
        <div class="menu__panel">
          <div class="wrap">
            <a class="btn btn--primary menu__cta" href="{out_name(lang, 'contact.html')}">{L['cta']}</a>
            {theme_block(lang)}
          </div>
        </div>
      </details>
    </div>
  </div>
</header>"""


def cta_band(lang):
    L = LANGS[lang]
    return f"""<section class="cta-band">
  <div class="wrap cta-band__inner">
    <div>
      <h2>{L['band_title']}</h2>
      <p>{L['band_text']}</p>
    </div>
    <a class="btn btn--primary" href="{out_name(lang, 'contact.html')}">{L['cta']}</a>
  </div>
</section>"""


def footer_html(lang):
    L = LANGS[lang]
    cols = ""
    for title, links in zip(L["foot_cols"][:2], L["foot_links"]):
        items = "\n        ".join(
            f'<a href="{out_name(lang, h.split("#")[0])}{"#" + h.split("#")[1] if "#" in h else ""}">{t}</a>'
            for h, t in links
        )
        cols += f"""      <div class="foot__col">
        <h4>{title}</h4>
        {items}
      </div>
"""
    return f"""<footer class="foot">
  <div class="wrap">
    <div class="foot__inner">
      <div class="foot__col">
        <a class="brand" href="{out_name(lang, 'index.html')}" aria-label="{L['brand_aria']}">
          {mark_svg("brand__mark")}
          <span class="brand__name">{SITE}</span>
        </a>
        <p>{L['foot_tagline']}</p>
      </div>
{cols}      <div class="foot__col">
        <h4>{L['foot_cols'][2]}</h4>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="tel:{TEL_HREF}">{TEL_TEXT}</a>
        <p>{L['foot_reply']}</p>
      </div>
    </div>
    <p class="foot__legal">{L['foot_legal']}</p>
  </div>
</footer>"""


# ----------------------------------------------------------------- données structurées

def ld_business(lang):
    fr = lang == "fr"
    return {
        "@type": "ProfessionalService",
        "@id": f"{DOMAIN}/#pixelrock",
        "name": SITE,
        "description": (
            "Conception et développement de sites web pour les entreprises du "
            "Saguenay–Lac-Saint-Jean et du Québec. Prix fixe, délais écrits, "
            "et le client est propriétaire de son site."
        ) if fr else (
            "Web design and development for businesses in Saguenay–Lac-Saint-Jean "
            "and across Quebec. Fixed price, written timelines, and the client owns "
            "the site."
        ),
        "url": DOMAIN + url_of(lang, "index.html"),
        "logo": f"{DOMAIN}/assets/icon-512.png",
        "image": f"{DOMAIN}/assets/og-image.png",
        "email": EMAIL,
        "telephone": TEL_HREF,
        "priceRange": "$$",
        "inLanguage": LANGS[lang]["locale"],
        "availableLanguage": ["fr-CA", "en-CA"],
        "founder": {"@type": "Person", "name": "Glodi Tambwe"},
        "address": {
            "@type": "PostalAddress",
            "addressLocality": VILLE,
            "addressRegion": REGION,
            "addressCountry": PAYS,
        },
        "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]},
        "areaServed": [{"@type": "City", "name": v} for v in VILLES_DESSERVIES],
        "sameAs": ["https://kibilabel.ca", "https://gnosislearn.com", "https://zaryaonline.ca"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Forfaits de conception web" if fr else "Web design packages",
            "itemListElement": [
                {"@type": "Offer", "name": "Le Socle" if fr else "The Base",
                 "description": ("Site de 1 à 5 pages pour travailleurs autonomes et prestataires de services, livré en 1 à 2 semaines."
                                 if fr else "One-to-five-page site for self-employed people and service providers, delivered in 1 to 2 weeks."),
                 "priceCurrency": "CAD", "price": "700"},
                {"@type": "Offer", "name": "L'Assise" if fr else "The Foundation",
                 "description": ("Site sur mesure jusqu'à une quinzaine de pages pour PME établies, livré en 3 à 4 semaines."
                                 if fr else "Custom site of up to fifteen pages for established small businesses, delivered in 3 to 4 weeks."),
                 "priceCurrency": "CAD", "price": "2500"},
                {"@type": "Offer", "name": "Le Chantier" if fr else "The Build",
                 "description": ("Application, outil interne ou plateforme sur mesure. Prix et délai établis après un premier rendez-vous, selon la complexité et l'ampleur du projet."
                                 if fr else "Application, internal tool or custom platform. Price and timeline set after a first meeting, based on the project's complexity and scope.")},
                {"@type": "Offer", "name": "Entretien" if fr else "Maintenance",
                 "description": ("Service optionnel : hébergement, domaine, mises à jour, sauvegardes et 30 minutes de modifications par mois."
                                 if fr else "Optional service: hosting, domain, updates, backups and 30 minutes of changes a month."),
                 "priceCurrency": "CAD", "price": "50"},
            ],
        },
    }


def strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    for a, b in [("&mdash;", "—"), ("&nbsp;", " "), ("&rarr;", "→"), ("&amp;", "&"),
                 ("&laquo;", "«"), ("&raquo;", "»"), ("&quot;", '"')]:
        s = s.replace(a, b)
    return " ".join(s.split())


def ld_faq(body):
    items = []
    for block in re.findall(r"<details[^>]*>(.*?)</details>", body, re.S):
        m = re.search(r"<summary[^>]*>(.*?)</summary>", block, re.S)
        if not m:
            continue
        answers = [strip_tags(a) for a in re.findall(r"<p[^>]*>(.*?)</p>", block, re.S)]
        if not answers:
            continue
        items.append({"@type": "Question", "name": strip_tags(m.group(1)),
                      "acceptedAnswer": {"@type": "Answer", "text": " ".join(answers)}})
    return {"@type": "FAQPage", "mainEntity": items} if items else None


def ld_breadcrumb(lang, fr_name):
    L = LANGS[lang]
    label = L["crumbs"].get(fr_name)
    if not label:
        return None
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": L["home_crumb"],
             "item": DOMAIN + url_of(lang, "index.html")},
            {"@type": "ListItem", "position": 2, "name": label,
             "item": DOMAIN + url_of(lang, fr_name)},
        ],
    }


PAGE_TYPE = {
    "index.html": "WebPage",
    "services.html": "WebPage",
    "realisations.html": "CollectionPage",
    "a-propos.html": "AboutPage",
    "contact.html": "ContactPage",
    "projet-kibi-label.html": "ItemPage",
    "projet-gnosis.html": "ItemPage",
    "projet-zarya.html": "ItemPage",
}

PROJETS = {
    "projet-kibi-label.html": ("Kibi Label", "https://kibilabel.ca", "WebSite"),
    "projet-gnosis.html": ("GNOSIS", "https://gnosislearn.com", "WebApplication"),
    "projet-zarya.html": ("Zarya", "https://zaryaonline.ca", "WebApplication"),
}


def ld_webpage(lang, fr_name, meta):
    node = {
        "@type": PAGE_TYPE.get(fr_name, "WebPage"),
        "@id": f"{DOMAIN}{url_of(lang, fr_name)}#page",
        "url": DOMAIN + url_of(lang, fr_name),
        "name": meta.get("title", SITE),
        "description": meta.get("description", ""),
        "inLanguage": LANGS[lang]["locale"],
        "isPartOf": {"@id": f"{DOMAIN}/#site"},
        "about": {"@id": f"{DOMAIN}/#pixelrock"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/og-image.png"},
    }
    if fr_name in PROJETS:
        nom, site, kind = PROJETS[fr_name]
        node["mainEntity"] = {
            "@type": kind, "name": nom, "url": site,
            "author": {"@type": "Person", "name": "Glodi Tambwe"},
        }
    if fr_name == "a-propos.html":
        node["mainEntity"] = {
            "@type": "Person",
            "name": "Glodi Tambwe",
            "jobTitle": "Développeur web" if lang == "fr" else "Web developer",
            "worksFor": {"@id": f"{DOMAIN}/#pixelrock"},
            "email": EMAIL,
            "telephone": TEL_HREF,
            "address": {"@type": "PostalAddress", "addressLocality": VILLE,
                        "addressRegion": REGION, "addressCountry": PAYS},
        }
    return node


def json_ld(lang, fr_name, body, meta):
    graph = [ld_business(lang), ld_webpage(lang, fr_name, meta)]
    graph.append({"@type": "WebSite", "@id": f"{DOMAIN}/#site",
                  "url": DOMAIN + "/", "name": SITE, "inLanguage": ["fr-CA", "en-CA"],
                  "publisher": {"@id": f"{DOMAIN}/#pixelrock"}})
    bc = ld_breadcrumb(lang, fr_name)
    if bc:
        graph.append(bc)
    faq = ld_faq(body)
    if faq:
        graph.append(faq)
    return ('<script type="application/ld+json">'
            + json.dumps({"@context": "https://schema.org", "@graph": graph},
                         ensure_ascii=False, separators=(",", ":"))
            + "</script>")


# ----------------------------------------------------------------- assemblage

def parse(fragment):
    m = re.match(r"\s*<!--(.*?)-->", fragment, re.S)
    meta = {}
    if m:
        for line in m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        fragment = fragment[m.end():]
    return meta, fragment.strip()


def localise_body(lang, body):
    """Adapte les chemins d'un fragment : noms de fichiers anglais et assets à la racine."""
    if lang == "fr":
        return body
    for fr_name, en_name in SLUG_EN.items():
        if fr_name != en_name:
            body = body.replace(f'href="{fr_name}', f'href="{en_name}')
    return body.replace('src="assets/', 'src="../assets/')


def render(lang, fr_name, meta, body):
    L = LANGS[lang]
    p = prefix(lang)
    title = meta.get("title", SITE)
    desc = meta.get("description", "")
    canonical = DOMAIN + url_of(lang, fr_name)
    robots = "noindex,nofollow" if meta.get("noindex") else "index,follow,max-image-preview:large"

    alternates = ""
    if not meta.get("noindex"):
        alternates = (
            f'<link rel="alternate" hreflang="fr-CA" href="{DOMAIN}{url_of("fr", fr_name)}">\n'
            f'<link rel="alternate" hreflang="en-CA" href="{DOMAIN}{url_of("en", fr_name)}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}{url_of("fr", fr_name)}">\n'
        )

    icons = (
        f'<link rel="icon" href="{p}assets/favicon.ico" sizes="48x48">\n'
        f'<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">\n'
        f'<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">\n'
        f'<link rel="manifest" href="{p}site.webmanifest">'
    )

    return f"""<!doctype html>
<html lang="{L['locale']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{BOOT}
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
{alternates}<meta name="theme-color" content="#E3E2DD" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#16181B" media="(prefers-color-scheme: dark)">
<meta name="author" content="Glodi Tambwe">
<meta name="geo.region" content="CA-QC">
<meta name="geo.placename" content="Saguenay, Québec">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{L['og_locale']}">
<meta property="og:image" content="{DOMAIN}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Pixelrock — des sites web bâtis sur le roc">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{DOMAIN}/assets/og-image.png">
{icons}
{FONTS}
<link rel="stylesheet" href="{p}assets/{ASSETS_VERSIONNES["css"]}">
<script src="{p}assets/{ASSETS_VERSIONNES["js"]}" defer></script>
{json_ld(lang, fr_name, body, meta)}
</head>
<body>
<a class="skip" href="#contenu">{L['skip']}</a>
{nav_html(lang, meta.get('nav', ''), fr_name)}
<main id="contenu">
{body}
</main>
{'' if meta.get('nav') == 'contact' else cta_band(lang)}
{footer_html(lang)}
{tabbar(lang, meta.get('nav', ''), fr_name)}
</body>
</html>
"""


def webmanifest():
    return json.dumps({
        "name": "Pixelrock — conception de sites web",
        "short_name": "Pixelrock",
        "description": "Conception de sites web au Saguenay–Lac-Saint-Jean et partout au Québec.",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "lang": "fr-CA",
        "dir": "ltr",
        "background_color": "#E3E2DD",
        "theme_color": "#202328",
        "icons": [
            {"src": "/assets/favicon-32.png", "sizes": "32x32", "type": "image/png"},
            {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "/assets/icon-maskable-512.png", "sizes": "512x512",
             "type": "image/png", "purpose": "maskable"},
        ],
    }, ensure_ascii=False, indent=2)


def page_lastmod(fr_name):
    """Date de dernière modification réelle du contenu, pas la date de construction."""
    stamps = []
    for lang, L in LANGS.items():
        f = ROOT / L["dir"] / fr_name
        if f.exists():
            stamps.append(f.stat().st_mtime)
    stamps.append((SRC / "styles.css").stat().st_mtime)
    return datetime.fromtimestamp(max(stamps), tz=timezone.utc).strftime("%Y-%m-%d")


# images à déclarer pour chaque page, avec leur légende
PAGE_IMAGES = {
    "index.html": [("og-image.png", "Pixelrock — des sites web bâtis sur le roc")],
    "realisations.html": [("kibi.png", "Kibi Label"), ("gnosis.png", "GNOSIS"), ("zarya.png", "Zarya")],
    "projet-kibi-label.html": [("kibi.png", "Kibi Label, institut de beauté à Chicoutimi")],
    "projet-gnosis.html": [("gnosis.png", "GNOSIS, application d'apprentissage")],
    "projet-zarya.html": [("zarya.png", "Zarya, plateforme de faisabilité de voyage")],
}


def sitemap(indexed):
    weight = {"index.html": "1.0", "services.html": "0.9", "contact.html": "0.9",
              "realisations.html": "0.8"}
    freq = {"index.html": "weekly", "services.html": "monthly", "realisations.html": "monthly"}
    rows = []
    for lang in ("fr", "en"):
        for fr_name in indexed:
            loc = DOMAIN + url_of(lang, fr_name)
            alts = "".join(
                f'\n    <xhtml:link rel="alternate" hreflang="{LANGS[c]["locale"]}" '
                f'href="{DOMAIN}{url_of(c, fr_name)}"/>' for c in ("fr", "en")
            )
            alts += (f'\n    <xhtml:link rel="alternate" hreflang="x-default" '
                     f'href="{DOMAIN}{url_of("fr", fr_name)}"/>')
            images = "".join(
                f'\n    <image:image>\n      <image:loc>{DOMAIN}/assets/{src}</image:loc>'
                f'\n      <image:title>{title}</image:title>\n    </image:image>'
                for src, title in PAGE_IMAGES.get(fr_name, [])
            )
            rows.append(
                f"  <url>\n    <loc>{loc}</loc>{alts}\n"
                f"    <lastmod>{page_lastmod(fr_name)}</lastmod>\n"
                f"    <changefreq>{freq.get(fr_name, 'yearly')}</changefreq>\n"
                f"    <priority>{weight.get(fr_name, '0.7')}</priority>{images}\n  </url>"
            )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml"\n'
            '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
            + "\n".join(rows) + "\n</urlset>\n")


ROBOTS = f"""User-agent: *
Allow: /
Disallow: /merci.html
Disallow: /en/thank-you.html

Sitemap: {DOMAIN}/sitemap.xml
"""

NETLIFY = """[build]
  publish = "."

# Netlify réécrit par défaut les liens en adresses sans .html et sert les deux
# formes : deux adresses pour une même page. On désactive la réécriture pour que
# l'adresse canonique soit la seule servie, et on redirige l'autre forme vers elle.
[build.processing]
  skip_processing = false

[build.processing.html]
  pretty_urls = false

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    X-Frame-Options = "SAMEORIGIN"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "geolocation=(), microphone=(), camera=()"

# Les feuilles de style et scripts portent une empreinte dans leur nom :
# leur adresse change à chaque modification, le cache long est donc sans risque.
[[headers]]
  for = "/assets/*.css"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/assets/*.js"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

# Les images gardent un nom fixe : une semaine, pour pouvoir les remplacer.
[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=604800"

[[headers]]
  for = "/*.html"
  [headers.values]
    Cache-Control = "public, max-age=0, must-revalidate"

[[redirects]]
  from = "https://www.pixelrock.net/*"
  to = "https://pixelrock.net/:splat"
  status = 301
  force = true
REDIRECTS"""




def netlify_redirects():
    """Les adresses sans .html redirigent vers la page canonique, dans les deux langues."""
    out = []
    for lang in LANGS:
        for fr_name in SLUG_EN:
            name = out_name(lang, fr_name)
            if name == "index.html":
                continue
            base = "" if lang == "fr" else "/en"
            out.append(
                f'\n[[redirects]]\n  from = "{base}/{name[:-5]}"\n'
                f'  to = "{base}/{name}"\n  status = 301\n'
            )
    return "".join(out)


def build():
    out_assets = OUT / "assets"
    out_assets.mkdir(parents=True, exist_ok=True)
    (OUT / "en").mkdir(exist_ok=True)

    # une empreinte dans le nom : chaque modification produit une nouvelle adresse,
    # donc aucun navigateur ni aucun CDN ne peut servir l'ancienne version
    for motif in ("styles*.css", "app*.js"):
        for vieux in out_assets.glob(motif):
            vieux.unlink()
    ASSETS_VERSIONNES["css"] = f"styles.{empreinte(SRC / 'styles.css')}.css"
    ASSETS_VERSIONNES["js"] = f"app.{empreinte(SRC / 'app.js')}.js"
    shutil.copy(SRC / "styles.css", out_assets / ASSETS_VERSIONNES["css"])
    shutil.copy(SRC / "app.js", out_assets / ASSETS_VERSIONNES["js"])
    for f in ASSETS.iterdir():
        if f.suffix.lower() in {".png", ".ico", ".svg", ".webp", ".jpg"}:
            shutil.copy(f, out_assets / f.name)

    indexed = []
    for lang, L in LANGS.items():
        pages_dir = ROOT / L["dir"]
        target = OUT if lang == "fr" else OUT / "en"
        for page in sorted(pages_dir.glob("*.html")):
            fr_name = page.name
            meta, body = parse(page.read_text(encoding="utf-8"))
            body = localise_body(lang, body)
            html = render(lang, fr_name, meta, body)
            (target / out_name(lang, fr_name)).write_text(html, encoding="utf-8")
            print(f"  {'' if lang == 'fr' else 'en/'}{out_name(lang, fr_name)}")
            if lang == "fr" and not meta.get("noindex"):
                indexed.append(fr_name)

    (OUT / "site.webmanifest").write_text(webmanifest(), encoding="utf-8")
    (OUT / "sitemap.xml").write_text(sitemap(indexed), encoding="utf-8")
    (OUT / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (OUT / "netlify.toml").write_text(NETLIFY.replace("REDIRECTS", netlify_redirects()), encoding="utf-8")
    print("  site.webmanifest, sitemap.xml, robots.txt, netlify.toml")

    build_preview()


def data_uri(path):
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def build_preview():
    """Version autonome de l'accueil français, en un seul fichier, pour partage."""
    pages = ROOT / "src" / "pages"
    _, body = parse((pages / "index.html").read_text(encoding="utf-8"))
    css = (SRC / "styles.css").read_text(encoding="utf-8")
    js = (SRC / "app.js").read_text(encoding="utf-8")

    contact = parse((pages / "contact.html").read_text(encoding="utf-8"))[1]
    contact = contact.replace('class="phead"', 'class="phead" id="contact"', 1)
    body = body + "\n" + contact

    for name in ("kibi", "gnosis", "zarya"):
        body = body.replace(f"assets/{name}.png", data_uri(ASSETS / f"{name}.png"))

    body = (
        body.replace('href="projet-kibi-label.html"', 'href="https://kibilabel.ca" target="_blank" rel="noopener"')
        .replace('href="projet-gnosis.html"', 'href="https://gnosislearn.com" target="_blank" rel="noopener"')
        .replace('href="projet-zarya.html"', 'href="https://zaryaonline.ca" target="_blank" rel="noopener"')
        .replace("Lire l'étude de cas &rarr;", "Voir le site en ligne &rarr;")
    )
    body = re.sub(r'href="services\.html[^"]*"', 'href="#forfaits"', body)
    body = body.replace('href="contact.html"', 'href="#contact"')

    nav = f"""<header class="nav">
  <div class="wrap nav__inner">
    <a class="brand" href="#haut">{mark_svg("brand__mark")}<span class="brand__name">{SITE}</span></a>
    <nav class="nav__links" aria-label="Navigation principale">
      <a href="#forfaits">Forfaits</a>
      <a href="#realisations">Réalisations</a>
      <a href="#contact">Contact</a>
    </nav>
    <div class="nav__end">
      {theme_switch("fr")}
      <a class="nav__cta" href="#contact">Prendre rendez-vous</a></div>
  </div>
</header>"""

    foot = footer_html("fr")
    foot = re.sub(r'href="(services|realisations|a-propos|merci|projet-[a-z-]+)\.html[^"]*"',
                  'href="#forfaits"', foot)
    foot = foot.replace('href="index.html"', 'href="#haut"')

    html = (f"<title>{SITE}</title>\n{FONTS}\n<style>\n{css}\n</style>\n"
            f'{nav}\n<main id="haut">\n{body}\n</main>\n{foot}\n<script>\n{js}\n</script>')
    (ROOT / "preview.html").write_text(html, encoding="utf-8")
    print("  preview.html (aperçu autonome)")


if __name__ == "__main__":
    build()
    print("\nSite généré — servir avec :  npx serve .")
