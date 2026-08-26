# Pixelrock — système visuel

## Concept

Le logo n'est pas une lettre, c'est une **construction** : sept rangées de blocs
empilés sur une base large, avec un chapiteau. Un pilier. Une colonne montée
bloc par bloc.

Ça donne la promesse de la marque : **bâti sur le roc**. Chaque site est monté
morceau par morceau, sur une base solide, et il tient. Au Saguenay — région
posée sur le Bouclier canadien — l'image parle d'elle-même.

Tout le langage visuel découle de là : rien n'est arrondi, rien ne flotte.
Les blocs sont posés, avec une ombre pleine décalée qui les ancre au sol.

## La grille du logo

Module de 12 unités, bloc de 10, gouttière de 2. Sept rangées sur cinq colonnes.
Le fût est décalé d'un demi-module (6 unités) et centré sur la base.

```
viewBox="0 0 58 82"
rangée 1 (y=0)      x = 0, 12, 24, 36, 48     chapiteau
rangée 2 (y=12)     x = 12, 24, 36            épaulement
rangées 3-6         x = 18, 30                fût (demi-module)
rangée 7 (y=72)     x = 0, 12, 24, 36, 48     base
```

Cette grille de 12 est le module du site entier : gouttières, trames de fond,
ombres décalées.

## Couleurs

Les deux premières viennent directement du logo. L'accent est ajouté : un
vermillon d'oxyde, couleur de peinture industrielle — un clin d'œil au pays de
l'aluminium, et surtout la seule dépense d'audace de la palette.

| Rôle | Clair | Sombre |
|---|---|---|
| Papier (fond) | `#E3E2DD` | `#16181B` |
| Papier surélevé (blocs) | `#EFEEEA` | `#202328` |
| Papier creusé (bandeau) | `#D7D6D0` | `#0E1012` |
| Encre (texte) | `#202328` | `#E3E2DD` |
| Encre secondaire | `#55585E` | `#ACABA5` |
| Filet | `#C4C3BC` | `#33363B` |
| **Accent** | `#A63315` | `#EC6E38` |
| Accent sur encre | `#F2814F` | `#A63315` |
| Ombre de bloc | `#202328` | `#3B3F45` |

Tous les couples texte/fond passent le seuil WCAG AA (4,5:1 minimum pour le
petit texte). L'accent existe en deux versions parce qu'un vermillon foncé sur
fond pâle et un orange vif sur fond foncé ne sont pas la même couleur — c'est le
même rôle, pas la même valeur.

**Règle d'usage de l'accent :** filets d'énumération, chiffres, surtitres,
bouton principal, un mot dans le titre. Jamais de grands aplats.

## Typographie

| Rôle | Police | Usage |
|---|---|---|
| Titres et interface | **Archivo** 700/800 | Grotesque industrielle, verticales franches — elle répond aux blocs du logo. Interlettrage serré (-0,025 em) sur les grands titres. |
| Texte courant | **Newsreader** 400/500 | Empattements chauds. C'est le contrepoids : il empêche la marque de sonner « startup » et parle à un propriétaire de PME. |
| Étiquettes et chiffres | **DM Mono** 400/500 | Surtitres, prix, coordonnées, numéros d'étape. Chiffres tabulaires. |

Le pari du système est ce contraste : une charpente brutaliste, un texte chaud
et lisible. Ni un site d'agence générique, ni un portfolio de développeur.

## Formes et mouvement

- **Aucun arrondi**, nulle part. Rayon zéro sur tous les éléments.
- **Blocs posés** : bordure 1 px encre + ombre pleine décalée de 6 px. Au survol,
  le bloc glisse de 2 px et l'ombre rétrécit — il s'enfonce, il ne s'envole pas.
- **Filets pleine largeur** entre les sections, jamais de cartes qui flottent.
- **Un seul moment de mouvement** : au chargement, le logo s'assemble de la base
  vers le haut, bloc par bloc, 42 ms d'écart. Une seule fois, et c'est tout.
  Désactivé si `prefers-reduced-motion`.

## Ton de voix

Direct, concret, sans jargon. On parle de téléphone qui sonne, pas
d'« expérience utilisateur ». On dit les prix. On dit ce qui n'est pas inclus.
On dit « je », jamais « nous ».

Les mots de la marque : bâtir, poser, socle, assise, chantier, roc.

## À décider

Le logo se lit comme un **I**, alors que la marque s'appelle Pixelrock. Deux
sorties possibles : assumer le pilier comme mark abstrait (c'est le parti pris
retenu ici, et il tient), ou décliner un **P** dans exactement la même grille de
12 si l'initiale compte. Le système fonctionne dans les deux cas.
