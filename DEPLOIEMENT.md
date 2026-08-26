# Mise en ligne de pixelrock.net

## Le site en local

```
python3 build.py     # régénère les pages depuis src/
npx serve .          # sert le site sur http://localhost:3000
```

`build.py` produit les 9 pages françaises à la racine, les 9 pages anglaises
dans `en/`, `assets/styles.css`, `assets/app.js`, `sitemap.xml`, `robots.txt`,
`site.webmanifest`, `netlify.toml` et `preview.html`.

Ne modifie jamais les fichiers HTML de la racine ni ceux de `en/` à la main :
ils sont écrasés à chaque construction. Le contenu vit dans `src/pages/`
(français) et `src/pages-en/` (anglais).

## Les deux langues

Le français est la langue principale : ses pages sont à la racine et portent le
`x-default`. L'anglais est servi depuis `/en/`, avec des noms de fichiers
traduits (`services.html` → `en/packages.html`, `realisations.html` →
`en/work.html`, etc. — la table est en haut de `build.py`, sous `SLUG_EN`).

Chaque page déclare ses `hreflang` réciproques, et le sélecteur FR/EN de la
barre de navigation renvoie vers la page équivalente, pas vers l'accueil.

Pour ajouter une page : créer le fragment dans `src/pages/`, sa traduction dans
`src/pages-en/` sous **le même nom de fichier**, et ajouter la correspondance de
nom anglais dans `SLUG_EN`.

## Avant la première mise en ligne

**1. Activer le formulaire de contact.** Il passe par FormSubmit, qui n'exige
aucun compte mais demande une activation unique : une fois le site en ligne,
envoyer un premier message depuis `contact.html`. FormSubmit envoie un courriel
de confirmation à `gloditambwe1@gmail.com` — cliquer le lien qu'il contient.
Tant que ce n'est pas fait, les envois ne sont pas transmis. Une seule
activation suffit pour les deux langues, l'adresse de destination étant la même.

Si tu déploies sur Netlify et préfères ses formulaires intégrés : ajouter
`data-netlify="true"` et `<input type="hidden" name="form-name" value="contact">`
sur le `<form>` de `src/pages/contact.html`, retirer l'attribut `action`, puis
configurer la notification par courriel dans le tableau de bord Netlify.

**2. Vérifier les tarifs et les délais** dans `src/pages/index.html` et
`src/pages/services.html`.

## Déploiement sur Netlify

1. Créer un dépôt Git et y pousser le dossier.
2. Sur Netlify : *Add new site → Import an existing project*, choisir le dépôt.
3. Réglages de build : commande vide, répertoire de publication `.`
   (`netlify.toml` s'en charge déjà, avec les en-têtes de sécurité et le cache
   des assets).
4. *Domain management → Add a domain* → `pixelrock.net`.

### DNS

Chez le registraire de `pixelrock.net`, deux options :

- **Netlify DNS** (le plus simple) : remplacer les serveurs de noms par ceux que
  Netlify indique. Le certificat HTTPS et la redirection `www` se configurent seuls.
- **DNS externe** : un enregistrement `A` sur `75.2.60.5` pour l'apex, et un
  `CNAME` de `www` vers `<ton-site>.netlify.app`. Vérifier la valeur exacte dans
  le tableau de bord Netlify — elle peut changer.

Puis activer HTTPS (*Domain management → HTTPS → Verify DNS configuration*).
La redirection de `www.pixelrock.net` vers `pixelrock.net` est déjà dans
`netlify.toml`.

## Après la mise en ligne

1. **Google Search Console** — ajouter la propriété `pixelrock.net`, la valider
   par enregistrement DNS `TXT`, puis soumettre `https://pixelrock.net/sitemap.xml`.
2. **Fiche Google Business** — c'est le levier le plus fort du référencement
   local, devant le site lui-même. Catégorie « Concepteur de sites Web »,
   zone de service : Saguenay, Chicoutimi, Jonquière, La Baie, Alma. Ajouter le
   lien vers `pixelrock.net`. Demander un avis à chaque client livré.
3. **Bing Webmaster Tools** — import direct depuis Search Console, deux minutes.
4. **Vérifier le rendu du partage** avec le validateur de liens de Facebook et
   de LinkedIn (l'image sociale est `assets/og-image.png`).

## Ce qui est déjà en place pour le référencement

- Titres et descriptions par page, orientés Saguenay et Québec
- Adresses canoniques sur `https://pixelrock.net`
- Données structurées `ProfessionalService` avec adresse, coordonnées
  géographiques, zone desservie (14 municipalités) et catalogue des forfaits
- Fil d'Ariane balisé sur les pages intérieures
- `FAQPage` généré automatiquement à partir des blocs de questions
- `sitemap.xml`, `robots.txt`, page de remerciement exclue de l'indexation
- Image de partage social 1200 × 630
- Icônes d'application pour Windows, Android et iOS, plus le manifeste
- Version anglaise complète sous `/en/`, avec `hreflang` réciproques et
  `x-default` sur le français
- Aucun débordement horizontal de 320 px à 1920 px, sur les dix-huit pages
