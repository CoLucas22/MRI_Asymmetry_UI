"""MRI Asymmetry Analysis - interface Streamlit.

Page d'accueil : configuration du dépôt pipeline et vue d'ensemble.
"""

from __future__ import annotations

import glob
import os

import streamlit as st

import ui

ETAPES = [
    ("preprocess.py", "Prétraitement des IRM DICOM : normalisation, recadrage, export des tableaux."),
    ("extract_features.py", "Extraction des descripteurs d'asymétrie gauche/droite sur les coupes axiales."),
    ("visualize.py", "Génération des figures et des cartes d'asymétrie dans results/figures/."),
    ("classification_task.R", "Régression logistique sur le jeu d'entraînement, prédiction sur le jeu de validation."),
]

MODULES = [
    ("pages/1_Upload_DICOM.py", "Upload DICOM"),
    ("pages/2_Pipeline.py", "Exécution du pipeline"),
    ("pages/3_Resultats.py", "Résultats"),
    ("pages/4_Datasets_CSV.py", "Datasets CSV"),
]

ui.header(
    "MRI Asymmetry Analysis",
    "Analyse d'asymétrie sur IRM axiales dans le cadre de la maladie de Crohn.",
)

racine = ui.pipeline_root()
configure = bool(racine) and os.path.isdir(racine)

with st.expander("Dépôt pipeline", expanded=not configure):
    saisie = st.text_input(
        "Chemin vers le clone de MRI_Asymmetry_Analysis_Pipeline",
        value=racine,
        placeholder="/home/user/MRI_Asymmetry_Analysis_Pipeline",
    )
    if st.button("Enregistrer le chemin"):
        racine = ui.set_pipeline_root(saisie)
        configure = bool(racine) and os.path.isdir(racine)
        if configure:
            st.success("Chemin enregistré. Il sera réutilisé au prochain lancement.")
        else:
            st.error("Répertoire introuvable. Vérifiez le chemin absolu du clone.")


def compte_dicom(base: str) -> int:
    total = 0
    for _, _, fichiers in os.walk(base):
        total += sum(1 for f in fichiers if f.lower().endswith(".dcm"))
    return total


if configure:
    col_dicom, col_csv, col_figures = st.columns(3)
    col_dicom.metric("Fichiers DICOM", compte_dicom(os.path.join(racine, "data_example")))
    col_csv.metric(
        "Fichiers CSV",
        len(glob.glob(os.path.join(racine, "data_example", "**", "*.csv"), recursive=True)),
    )
    col_figures.metric(
        "Figures produites",
        len(glob.glob(os.path.join(racine, "results", "figures", "**", "*.png"), recursive=True)),
    )
else:
    st.info("Renseignez le chemin du dépôt pour activer les autres modules.")

st.subheader("Étapes du pipeline")
for numero, (script, description) in enumerate(ETAPES, start=1):
    st.markdown(f"{numero}. `{script}` : {description}")

st.subheader("Modules")
for chemin_page, libelle in MODULES:
    st.page_link(chemin_page, label=libelle)
