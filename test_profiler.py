# TESTER MON FICHIER PROFILER.PY

import pandas as pd
from profiler import ProfileurFAO

# Chargement des fichiers
df_veg = pd.read_csv("data/fr_vegetaux.csv")
df_anim = pd.read_csv("data/fr_animaux.csv")
df_cer = pd.read_csv("data/fr_cereales.csv")
df_pop = pd.read_csv("data/fr_population.csv")
df_sous = pd.read_csv("data/fr_sousalimentation.csv")

# Instanciation
prof_veg = ProfileurFAO(df_veg, "Végétaux")
prof_anim = ProfileurFAO(df_anim, "Animaux")
prof_cer = ProfileurFAO(df_cer, "Céréales")
prof_pop = ProfileurFAO(df_pop, "Population")
prof_sous = ProfileurFAO(df_sous, "Sous-alimentation")

# Exemple : afficher les valeurs manquantes
print("Valeurs manquantes :")
print({
    "veg": prof_veg.missing_values(),
    "anim": prof_anim.missing_values(),
    "cer": prof_cer.missing_values(),
    "pop": prof_pop.missing_values(),
    "sous": prof_sous.missing_values()
})

# Exemple : couverture géographique
print("\nCouverture géographique :")
print({
    "veg": prof_veg.geographic_coverage(),
    "pop": prof_pop.geographic_coverage(),
    "sous": prof_sous.geographic_coverage()
})
