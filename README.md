# SAÉ 1.5 – Traiter des données

Valorisation des **données ouvertes des voitures radars à conduite externalisée** (relevés de vitesses 2023, huit régions de France métropolitaine) : traitement automatique d'un fichier CSV avec Python puis restitution sur une page web avec graphiques. Travail en binôme.

| Élément | Contenu |
|---|---|
| `SAE15_Cahier-des-charges.pdf` | Cahier des charges |
| `SAE15_Soutenance.pptx` | Support de soutenance (motivations, méthodes d'extraction, structure du site, difficultés) |
| `site/import_csv.py` | Script de lecture du CSV et génération de `index.html` |
| `site/index.html` + `site/style.css` | Page web générée (graphiques Chart.js) |

## Régénérer la page
Le CSV source (~58 Mo) n'est pas inclus dans le dépôt. Le télécharger sur data.gouv.fr (« vitesses pratiquées par les voitures radars », 2023), le placer dans `site/` avec le nom attendu par le script, puis :
```bash
cd site
python import_csv.py
```

**Technos :** Python (`csv`), HTML/CSS, Chart.js.
