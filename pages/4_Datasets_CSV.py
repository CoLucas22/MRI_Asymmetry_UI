"""Exploration des jeux de données CSV du pipeline."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

import ui

ui.header("Datasets CSV", "Jeux d'entraînement, de validation et CSV intermédiaires du pipeline.")
racine = ui.require_pipeline_root()

JEUX_PRINCIPAUX = [
    ("Entraînement", os.path.join(racine, "data_example", "train_dataset.csv")),
    ("Validation", os.path.join(racine, "data_example", "validation_dataset.csv")),
    ("Runs", os.path.join(racine, "data_example", "Runs_dataset.csv")),
]

dossier_csv = Path(racine, "data_example", "CSV_files")
jeux_secondaires = (
    [(p.name, str(p)) for p in sorted(dossier_csv.glob("*.csv"))] if dossier_csv.is_dir() else []
)


@st.cache_data(show_spinner=False)
def charger(chemin: str, horodatage: float) -> pd.DataFrame:
    """Lit un CSV. L'horodatage force la relecture quand le fichier change."""
    return pd.read_csv(chemin)


def lire(chemin: str) -> pd.DataFrame:
    return charger(chemin, os.path.getmtime(chemin))


resume = []
for libelle, chemin in JEUX_PRINCIPAUX:
    if os.path.isfile(chemin):
        donnees = lire(chemin)
        resume.append(
            {
                "Jeu de données": libelle,
                "Lignes": donnees.shape[0],
                "Colonnes": donnees.shape[1],
                "Fichier": os.path.basename(chemin),
            }
        )
    else:
        resume.append(
            {"Jeu de données": libelle, "Lignes": None, "Colonnes": None, "Fichier": "absent"}
        )

st.dataframe(pd.DataFrame(resume), hide_index=True, use_container_width=True)

disponibles = [
    (libelle, chemin)
    for libelle, chemin in JEUX_PRINCIPAUX + jeux_secondaires
    if os.path.isfile(chemin)
]

if not disponibles:
    st.info("Aucun CSV trouvé sous data_example/. Vérifiez le chemin du dépôt sur la page d'accueil.")
    st.stop()

st.subheader("Explorer un jeu de données")
libelle = st.selectbox("Jeu de données", [libelle for libelle, _ in disponibles])
chemin = dict(disponibles)[libelle]
df = lire(chemin)

col_lignes, col_colonnes, col_taille, col_nan = st.columns(4)
col_lignes.metric("Lignes", df.shape[0])
col_colonnes.metric("Colonnes", df.shape[1])
col_taille.metric("Taille", ui.taille_lisible(os.path.getsize(chemin)))
col_nan.metric("Valeurs manquantes", int(df.isna().sum().sum()))

onglet_donnees, onglet_stats, onglet_graphiques = st.tabs(
    ["Données", "Statistiques", "Graphiques"]
)

with onglet_donnees:
    col_filtre, col_max = st.columns([3, 1])
    filtre = col_filtre.text_input("Filtrer les colonnes par nom", "")
    max_lignes = col_max.number_input("Lignes affichées", min_value=5, max_value=500, value=50, step=10)

    affichage = df
    if filtre:
        colonnes_retenues = [c for c in df.columns if filtre.lower() in c.lower()]
        affichage = df[colonnes_retenues] if colonnes_retenues else df

    st.dataframe(affichage.head(int(max_lignes)), use_container_width=True, height=400)
    with open(chemin, "rb") as fichier:
        st.download_button(
            "Télécharger le CSV",
            fichier.read(),
            file_name=os.path.basename(chemin),
            mime="text/csv",
        )

with onglet_stats:
    numeriques = df.select_dtypes(include="number")
    if numeriques.empty:
        st.info("Aucune colonne numérique dans ce jeu de données.")
    else:
        st.dataframe(numeriques.describe().T, use_container_width=True)

    st.dataframe(
        pd.DataFrame(
            {
                "Colonne": df.columns,
                "Type": df.dtypes.astype(str),
                "Valeurs manquantes": df.isna().sum().values,
            }
        ),
        hide_index=True,
        use_container_width=True,
    )

with onglet_graphiques:
    colonnes_num = df.select_dtypes(include="number").columns.tolist()
    colonnes_cat = df.select_dtypes(include=["object", "category"]).columns.tolist()

    if not colonnes_num:
        st.info("Aucune colonne numérique à représenter.")
    else:
        graphique = st.radio(
            "Type de graphique",
            ["Histogramme", "Nuage de points", "Boîtes à moustaches"],
            horizontal=True,
        )

        if graphique == "Histogramme":
            colonne = st.selectbox("Colonne", colonnes_num)
            classes = st.slider("Nombre de classes", 5, 100, 30)
            valeurs = df[colonne].dropna()
            if valeurs.empty:
                st.info("Colonne entièrement vide.")
            else:
                effectifs, bornes = np.histogram(valeurs, bins=classes)
                centres = (bornes[:-1] + bornes[1:]) / 2
                st.bar_chart(pd.DataFrame({colonne: effectifs}, index=np.round(centres, 3)))

        elif graphique == "Nuage de points":
            col_x, col_y = st.columns(2)
            axe_x = col_x.selectbox("Axe des abscisses", colonnes_num, key="axe_x")
            axe_y = col_y.selectbox(
                "Axe des ordonnées", colonnes_num, index=min(1, len(colonnes_num) - 1), key="axe_y"
            )
            couleur = st.selectbox("Couleur", ["Aucune"] + colonnes_cat)
            st.scatter_chart(
                df,
                x=axe_x,
                y=axe_y,
                color=None if couleur == "Aucune" else couleur,
            )

        else:
            selection = st.multiselect(
                "Colonnes", colonnes_num, default=colonnes_num[: min(5, len(colonnes_num))]
            )
            if selection:
                import matplotlib

                matplotlib.use("Agg")
                import matplotlib.pyplot as plt

                figure, axes = plt.subplots(figsize=(max(6, len(selection) * 1.4), 4.5))
                axes.boxplot([df[c].dropna() for c in selection])
                axes.set_xticklabels(selection, rotation=20, ha="right")
                axes.spines[["top", "right"]].set_visible(False)
                figure.tight_layout()
                st.pyplot(figure)
