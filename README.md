# Projet FAO

Ce projet prépare un jeu de données FAO pour l'analyse de la disponibilité alimentaire et de la sous-nutrition en France.

## Objectif
- Diagnostiquer les fichiers FAO français
- Nettoyer les anomalies et convertir les valeurs numériques
- Construire un dataset global cohérent
- Calculer des indicateurs alimentaires et le taux de sous-nutrition

## Contenu du projet
- `data/` : sources CSV FAO
  - `fr_vegetaux.csv`
  - `fr_animaux.csv`
  - `fr_cereales.csv`
  - `fr_population.csv`
  - `fr_sousalimentation.csv`
  - `global_fao_dataset.csv` : sortie générée
- `dataset_global_propre.py` : script de construction du dataset global
- `profiler.py` : classes `DataProfiler` et `ProfileurFAO` pour profilage des données
- `test_profiler.py` : script d'exemple et de vérification du profiler
- `notebooks/` : notebooks de diagnostic, analyse exploratoire et modélisation
- `requirements.txt` : dépendances Python

## Installation
1. Activer l'environnement Python
2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation
### Générer le dataset global
Lancer le script de construction :

```bash
python dataset_global_propre.py
```

La sortie est enregistrée dans :
- `data/global_fao_dataset.csv`

### Profiler les données FAO
Exécuter un exemple de vérification :

```bash
python test_profiler.py
```

Ce script utilise `ProfileurFAO` pour afficher :
- valeurs manquantes
- couverture géographique

### Analyser avec les notebooks
- `notebooks/J1_diagnostic.ipynb` : diagnostic initial
- `notebooks/J2_analyse exploratoire et corrélations.ipynb` : analyse des relations
- `notebooks/J3_Modélisation_régression.ipynb` : modélisation et régression

## Nettoyage et construction des données
### Principales étapes
- chargement des fichiers CSV
- conversion de `Valeur` en type numérique
- traitement des valeurs négatives invalides
- sélection de la période de sous-alimentation `20162018`
- calcul des calories par personne à partir des données végétales et animales
- intégration de la population
- jointure finale sur `Code zone` et `Zone`

### Règles de traitement
- Les valeurs négatives sur certains indicateurs sont remplacées par `NaN`
- L'agrégation calorique est réalisée pour `Disponibilité alimentaire (kcal/personne/jour)`
- Le dataset final conserve uniquement les zones présentes dans toutes les sources jointes

## Résultat attendu
Le dataset global produit contient au moins les colonnes suivantes :
- `Code zone`
- `Zone`
- `Kcal_veg`
- `Kcal_anim`
- `Kcal_total_kcal_per_capita_per_day`
- `Population_milliers`
- `Population_millions`
- `Sous_alimentation_millions`
- `Taux_sous_nutrition_pct`

## Dépendances
- pandas
- numpy
- matplotlib
- scikit-learn
- scipy
- joblib
- pillow

## Prochaines étapes possibles
- enrichir le dataset avec des variables supplémentaires par zone
- ajouter des visualisations et un rapport consolidé
- explorer des modèles de régression ou de classification
- vérifier les données manquantes et la qualité par période

## Contribuer
Si tu veux améliorer ce projet :
- ajouter des tests unitaires pour `dataset_global_propre.py`
- documenter les anomalies détectées dans les jeux de données
- étendre le profiler pour analyser les séries temporelles
- ajouter un script de nettoyage plus complet pour les valeurs manquantes

## Exemples d'utilisation
1. Construire le dataset global :

```bash
python dataset_global_propre.py
```

2. Vérifier le profiler :

```bash
python test_profiler.py
```

3. Ouvrir le notebook de diagnostic :

```bash
jupyter notebook notebooks/J1_diagnostic.ipynb
```

4. Charger la sortie pour une visualisation rapide :

```python
import pandas as pd

df = pd.read_csv('data/global_fao_dataset.csv')
print(df.head())
```
