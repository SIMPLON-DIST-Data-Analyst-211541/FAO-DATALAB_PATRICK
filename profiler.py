# FICHIER CONTENANT LES CLASSES DATAPROFILER ET DATAPROFILEURFAO


import pandas as pd

## Classe mère DataProfiler

class DataProfiler:
    def __init__(self, df, name):
        self.df = df
        self.name = name

    def missing_values(self):
        return self.df["Valeur"].isna().sum()

    def duplicates_full(self):
        return self.df.duplicated().sum()

    def duplicates_business_key(self):
        key = ["Code zone", "Code Produit", "Code Élément", "Code année"]
        return self.df.duplicated(subset=key).sum()

    def units(self):
        return self.df["Unité"].value_counts()

    def symbols(self):
        if "Symbole" not in self.df.columns:
            return None
        return self.df["Symbole"].value_counts()

    def negative_values(self):
        vals = pd.to_numeric(self.df["Valeur"], errors="coerce")
        return vals[vals < 0]


### Classe fille ProfileurFAO

class ProfileurFAO(DataProfiler):
    def geographic_coverage(self):
        return {
            "nb_zones": self.df["Code zone"].nunique(),
            "zones": sorted(self.df["Zone"].unique())
        }

    def missing_by_period(self):
        if "Code année" not in self.df.columns:
            return None
        vals = pd.to_numeric(self.df["Valeur"], errors="coerce")
        return vals.groupby(self.df["Code année"]).apply(lambda x: x.isna().sum())
