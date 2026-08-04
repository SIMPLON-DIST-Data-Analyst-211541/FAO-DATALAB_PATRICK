# NETTOYAGE ET CONSTRUCTION DU DATASET GLOBAL

## Chargement des données

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

def load_fao_data():
    df_veg = pd.read_csv(DATA_DIR / "fr_vegetaux.csv")
    df_anim = pd.read_csv(DATA_DIR / "fr_animaux.csv")
    df_cer = pd.read_csv(DATA_DIR / "fr_cereales.csv")
    df_pop = pd.read_csv(DATA_DIR / "fr_population.csv")
    df_sous = pd.read_csv(DATA_DIR / "fr_sousalimentation.csv")
    return df_veg, df_anim, df_cer, df_pop, df_sous


# Nettoyage des anomalies

## a) Conversion de la colonne 'Valeur' en numérique

def clean_value_column(df):
    df = df.copy()
    df["Valeur"] = pd.to_numeric(df["Valeur"], errors="coerce")
    return df

# b) Gestion des valeurs négatives

def treat_negative_values(df, elements_to_nans=None):
    df = df.copy()
    if elements_to_nans is None:
        elements_to_nans = []

    mask_neg = df["Valeur"] < 0
    mask_element = df["Élément"].isin(elements_to_nans)
    df.loc[mask_neg & mask_element, "Valeur"] = pd.NA
    return df

# Sélection de la période de référence (sous-alimentation)

def select_undernourishment_period(df_sous, period_code="20162018"):
    df = df_sous.copy()
    df = clean_value_column(df)
    df_period = df[df["Code année"] == period_code]
    # On garde uniquement Zone + Valeur
    df_period = df_period[["Code zone", "Zone", "Valeur"]].rename(
        columns={"Valeur": "Sous_alimentation_millions"}
    )
    return df_period


# Construction des indicateurs de disponibilité calorique

def compute_kcal_per_capita(df_veg, df_anim):
    df_veg = clean_value_column(df_veg)
    df_anim = clean_value_column(df_anim)

    elem_kcal = "Disponibilité alimentaire (kcal/personne/jour)"

    kcal_veg = (
        df_veg[df_veg["Élément"] == elem_kcal]
        .groupby(["Code zone", "Zone"], as_index=False)["Valeur"]
        .sum()
        .rename(columns={"Valeur": "Kcal_veg"})
    )

    kcal_anim = (
        df_anim[df_anim["Élément"] == elem_kcal]
        .groupby(["Code zone", "Zone"], as_index=False)["Valeur"]
        .sum()
        .rename(columns={"Valeur": "Kcal_anim"})
    )

    kcal_total = pd.merge(
        kcal_veg,
        kcal_anim,
        on=["Code zone", "Zone"],
        how="outer"
    )

    kcal_total["Kcal_veg"] = kcal_total["Kcal_veg"].fillna(0)
    kcal_total["Kcal_anim"] = kcal_total["Kcal_anim"].fillna(0)
    kcal_total["Kcal_total_kcal_per_capita_per_day"] = (
        kcal_total["Kcal_veg"] + kcal_total["Kcal_anim"]
    )

    return kcal_total


# Intégration de la population

def prepare_population(df_pop):
    df = df_pop.copy()
    df = clean_value_column(df)
    df = df[["Code zone", "Zone", "Valeur"]].rename(
        columns={"Valeur": "Population_milliers"}
    )
    return df


# Jointure globale (Zone comme clé)

## On joint :kcal_total, population, sous-alimentation

def build_global_dataset(df_veg, df_anim, df_pop, df_sous):
    kcal_total = compute_kcal_per_capita(df_veg, df_anim)
    pop = prepare_population(df_pop)
    sous = select_undernourishment_period(df_sous, period_code="20162018")

    # Jointure principale sur Code zone
    df_global = (
        kcal_total
        .merge(pop, on=["Code zone", "Zone"], how="inner")
        .merge(sous, on=["Code zone", "Zone"], how="inner")
    )

    # Calcul du taux de sous-nutrition (%)
    # Sous_alimentation_millions / Population_totale * 100
    df_global["Population_millions"] = df_global["Population_milliers"] / 1000
    df_global["Taux_sous_nutrition_pct"] = (
        df_global["Sous_alimentation_millions"] / df_global["Population_millions"] * 100
    )

    return df_global


### Dcumentation des pays exclus

def list_excluded_countries(df_veg, df_pop, df_sous):
    zones_veg = set(df_veg["Code zone"].unique())
    zones_pop = set(df_pop["Code zone"].unique())
    zones_sous = set(df_sous["Code zone"].unique())

    common = zones_veg & zones_pop & zones_sous

    excl_veg = zones_veg - common
    excl_pop = zones_pop - common
    excl_sous = zones_sous - common

    return excl_veg, excl_pop, excl_sous


# Export du Dataset propre

def export_global_dataset(df_global, output_path="data/global_fao_dataset.csv"):
    df_global.to_csv(output_path, index=False)
    print(f"Dataset global exporté vers {output_path}")


if __name__ == "__main__":
    df_veg, df_anim, df_cer, df_pop, df_sous = load_fao_data()
    df_global = build_global_dataset(df_veg, df_anim, df_pop, df_sous)
    export_global_dataset(df_global)
