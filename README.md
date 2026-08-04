# Projet FAO

Ce projet vise à diagnostiquer et nettoyer des données FAO françaises pour construire une base cohérente et exploitable.

## Structure du dossier
- `data/` : fichiers CSV FAO
- `notebooks/` : notebook de diagnostic `J1_diagnostic.ipynb`
- `profiler.py` : classe `ProfileurFAO` pour analyser les fichiers
- `test_profiler.py` : script de validation et d'exemple d'utilisation
- `requirements.txt` : dépendances Python

## Données
Les fichiers importés sont :
- `data/fr_vegetaux.csv`
- `data/fr_animaux.csv`
- `data/fr_cereales.csv`
- `data/fr_population.csv`
- `data/fr_sousalimentation.csv`

La colonne clé utilisée pour les jointures est `Code zone`.

## Nettoyage
- Les valeurs négatives sur les éléments de type `Production` ont été remplacées par `NaN`.
- Justification : une production négative n'est pas interprétable économiquement et signale une anomalie.
- Ce choix permet de conserver une période récente et cohérente avec le reste des données, notamment autour de 2013.

## Jointure
- Méthode : `inner` sur `Code zone`.
- Conséquence : seuls les pays présents dans les trois fichiers sont conservés dans la table finale.
- Analyse des exclusions : les codes `Code zone` présents dans un fichier mais absents d'un autre sont listés avec des ensembles (`set`).

## Exécution
1. Installer les dépendances : `pip install -r requirements.txt`
2. Lancer le notebook : ouvrir `notebooks/J1_diagnostic.ipynb`
3. Vérifier les scripts : `python test_profiler.py`

## Prochaines étapes
- Consolider le jeu de données nettoyé
- Ajouter des analyses descriptives et des visualisations
- Vérifier la qualité des données par zone et par période
- Préparer un jeu final pour modélisation ou reporting
