# Publicités Pixelrock

Tout est bâti avec l'identité du site : mêmes couleurs, mêmes polices
(Archivo, Newsreader, DM Mono), même pilier de marque, mêmes ombres carrées.
Les fichiers sources (`*.py`, `*.html`) sont là pour refaire une version modifiée
sans repartir de zéro.

## Affiches

| Fichier | Format | Où l'utiliser |
|---|---|---|
| `affiche-carre-1080x1080.png` | 1080 × 1080 | Publication Facebook et Instagram |
| `affiche-story-1080x1920.png` | 1080 × 1920 | Story Instagram / Facebook, statut WhatsApp |
| `affiche-forfaits-1080x1350.png` | 1080 × 1350 | Publication portrait — les trois forfaits et leurs prix |
| `depliant-lettre.pdf` | 8,5 × 11 po | Feuillet à imprimer, à laisser en main propre |

Les versions `@2x.png` sont les mêmes affiches en double résolution, pour
l'impression ou pour recadrer sans perte.

Chaque pièce porte un code QR qui mène à `pixelrock.net`.

## Vidéos

| Fichier | Format | Durée |
|---|---|---|
| `video-story-1080x1920.mp4` | 1080 × 1920, 25 im/s | 16 s |
| `video-carre-1080x1080.mp4` | 1080 × 1080, 25 im/s | 16 s |

Quatre temps : la marque qui se pose pièce par pièce, la promesse, les trois
arguments, puis où te joindre. H.264 + AAC : ça passe partout — Facebook,
Instagram, LinkedIn, TikTok, YouTube Shorts.

## La musique

`musique.wav` est **synthétisée ici**, note par note (accords doux en ré majeur,
quelques cloches, réverbération courte). Elle n'appartient à personne d'autre :
aucun droit à payer, aucune réclamation possible sur tes publications. Niveau
mesuré à −15,8 LUFS, c'est-à-dire à peu près la cible des réseaux sociaux, sans
écraser une voix si tu en ajoutes une.

Pour changer la musique : `musique.py`, la fonction `piste()`.
Pour changer les textes ou les couleurs : `affiches.py` et `video.py`, puis

```
python3 affiches.py
python3 musique.py
python3 video.py
```

## Un conseil sur l'usage

L'affiche carrée et la vidéo story sont les deux pièces à publier en premier.
Les forfaits avec les prix affichés fonctionnent mieux en deuxième temps,
auprès de gens qui te connaissent déjà : le prix convainc quand la confiance est
là, il fait fuir quand elle ne l'est pas encore.
