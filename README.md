# Pub Helly-Co Services

Pub en boucle pour l'écran TV de la boutique Helly-Co Services (réparation de téléphone,
transfert d'argent, démarches, bureautique). Chaque version est une page HTML animée,
exportée en vidéo MP4 1920x1080.

Galerie et vote : https://benyachou.github.io/helly-co-pub/

## Versions de 5 minutes (celles qui sont sur la clé USB)

| Fichier | Nom | Idée |
| --- | --- | --- |
| `v9-helly-co-5min` | Avant / après | La version choisie au départ par le client, en boucle de 5 min |
| `v10-helly-co-cinema` | Cinéma | Sombre, grands mots découpés sur les photos |
| `v11-helly-co-bilingue` | Bilingue | Chaque message traduit en arabe en dessous |
| `v12-helly-co-lumiere` | Lumière | Fond clair, rythme calme |
| `v15-helly-co-gens-d-ici` | Les gens d'ici | Six personnages du quartier, chacun son petit problème |

Les v1 à v8 sont les premiers essais d'une minute, gardés seulement sur le PC.

## Fabriquer une vidéo

```
python exporter.py v15-helly-co-gens-d-ici            -> v15-helly-co-gens-d-ici.mp4 (~35 min)
python exporter.py v15-helly-co-gens-d-ici --apercu 20 56   -> captures aux secondes données
```

- `fabriquer.py` : génère les v10, v11 et v12 à partir de la v9.
- `preparer_persos.py` : met les portraits des personnages de la v15 en page
  (portraits fabriqués avec `~/ia-locale/portraits.py`).

## Dossiers

- `assets/` : logo, logos Western Union / MoneyGram / Ria, photos, portraits de la v15.
- `fonts/` : polices utilisées par les pages.
- `docs/` : la galerie en ligne (GitHub Pages) avec les vidéos allégées.
- `vote/` : le service de vote (Cloudflare Worker).
