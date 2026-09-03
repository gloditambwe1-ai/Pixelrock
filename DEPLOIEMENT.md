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

## Le site est en ligne

Hébergé sur Netlify, domaine `pixelrock.net` enregistré chez Cloudflare.

### Cloudflare : garder les enregistrements en « DNS only »

C'est le point à vérifier en premier. Netlify est déjà un réseau de diffusion :
activer le proxy Cloudflare (le nuage orange) met deux CDN en série, et ça cause
deux problèmes courants — le renouvellement automatique du certificat Netlify
échoue, et si le mode SSL de Cloudflare est réglé sur « Flexible », le site part
en boucle de redirection.

**Recommandé :** nuage **gris** (DNS only) sur les enregistrements qui pointent
vers Netlify. Le HTTPS reste assuré par Netlify.

Si tu tiens au proxy Cloudflare, alors le mode SSL/TLS doit impérativement être
**Full (strict)**, jamais Flexible.

### Une seule adresse par page

Netlify réécrit par défaut les liens en adresses sans `.html` **et** sert les
deux formes : `/services` et `/services.html` renvoyaient la même page, alors que
la balise canonique désigne `/services.html`. Deux adresses pour un même contenu,
c'est exactement ce que Google pénalise en diluant le signal.

Le `netlify.toml` livré désactive cette réécriture (`pretty_urls = false`) et
ajoute une redirection 301 de chaque forme courte vers la forme canonique. Après
le prochain déploiement, vérifier que `pixelrock.net/services` redirige bien vers
`pixelrock.net/services.html`.

## Se faire trouver sur Google

Dans l'ordre d'impact réel, du plus fort au plus faible.

### 1. La fiche Google Business — de loin le plus important

Pour une entreprise de service locale, la fiche pèse plus lourd que le site
lui-même : c'est elle qui fait apparaître Pixelrock dans le bloc de résultats
locaux et sur Maps, au-dessus des résultats classiques.

- Catégorie principale : **Concepteur de sites Web**. Catégories secondaires :
  Service de marketing Internet, Développeur de logiciels.
- Pas d'adresse publique : cocher « Je livre des biens et services à mes clients »
  et définir la zone desservie — Saguenay, Chicoutimi, Jonquière, La Baie, Alma.
- Le nom, le téléphone et l'adresse doivent être **écrits exactement pareil**
  partout sur le web. Google recoupe ces mentions ; une variante de numéro ou de
  nom affaiblit le signal.
- Ajouter le lien vers `pixelrock.net`, des photos, et les services avec leurs prix.
- **Demander un avis à chaque client livré.** C'est le facteur de classement local
  le plus sous-utilisé. Trois avis détaillés valent mieux que trente lignes de
  contenu supplémentaire sur le site.

### 2. Google Search Console

1. Ajouter la propriété de type **Domaine** (`pixelrock.net`), qui couvre le
   français et l'anglais d'un coup.
2. La validation se fait par enregistrement `TXT` — c'est immédiat puisque le DNS
   est chez Cloudflare.
3. Soumettre `https://pixelrock.net/sitemap.xml`.
4. Demander l'indexation de la page d'accueil et de la page Forfaits via
   l'inspection d'URL, pour ne pas attendre le passage naturel du robot.
5. Revenir après deux semaines regarder le rapport de couverture et les requêtes
   qui amènent déjà des impressions : c'est là que se trouvent les vrais mots-clés
   à renforcer, pas dans les suppositions.

### 3. Les citations locales

Chaque mention cohérente du nom, du téléphone et de la ville sur un autre site
renforce le référencement local. Les plus utiles dans la région :

- Chambre de commerce et d'industrie Saguenay-Le Fjord
- Promotion Saguenay, répertoire des entreprises
- Pages Jaunes
- Le profil LinkedIn, avec le lien vers le site

### 4. Bing

Bing Webmaster Tools permet d'importer directement depuis Search Console. Deux
minutes, et ça couvre aussi les recherches faites depuis Windows et ChatGPT.

### Ce qu'il ne faut pas faire

Acheter des liens, publier des pages de villes quasi identiques (« conception web
Chicoutimi », « conception web Jonquière »…), ou bourrer les textes de mots-clés.
Google traite les trois comme des signaux de spam, et pour un site neuf de cette
taille, le risque dépasse largement le gain.

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
- Plan de site enrichi : dates de dernière modification réelles, alternates de
  langue et images déclarées
- Une fiche de page typée par gabarit (`AboutPage`, `ContactPage`,
  `CollectionPage`, `ItemPage`) rattachée à la fiche d'entreprise
- Une seule adresse indexable par page, la forme courte redirigeant en 301
- Aucun débordement horizontal de 320 px à 1920 px, sur les dix-huit pages

## La navigation sur téléphone

Sous 940 px, la navigation passe dans une barre fixée au bas de l'écran
(`.tabbar`, générée par `tabbar()` dans `build.py`) : cinq onglets — Accueil,
Forfaits, Projets, À propos, Contact — avec une icône dessinée à angles droits,
comme le pilier de la marque. L'onglet de la page courante est souligné en
orange. La barre respecte l'encoche du bas (`env(safe-area-inset-bottom)`) et le
`body` reçoit la marge correspondante, pour que rien ne finisse caché dessous.

Le bouton sandwich de la barre du haut ne sert donc plus à naviguer : il ne
contient plus que la prise de rendez-vous et le choix du thème. Le sélecteur
FR/EN, lui, reste visible en permanence dans la barre du haut.

Pour changer les onglets : la liste `tabs` de chaque langue dans `LANGS`, et les
tracés SVG dans `TAB_ICONS`, indexés par la même clé.
