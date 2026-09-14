"""Figures produites par le pipeline."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

import ui

EXTENSIONS_IMAGE = {".png", ".jpg", ".jpeg"}
EXTENSIONS = EXTENSIONS_IMAGE | {".svg", ".pdf"}

ui.header("Résultats", "Figures exportées par le pipeline dans results/figures/.")
racine = ui.require_pipeline_root()

dossier = os.path.join(racine, "results", "figures")
if not os.path.isdir(dossier):
    st.info(f"Le dossier {dossier} n'existe pas encore. Lancez visualize.py depuis le module d'exécution.")
    st.stop()

fichiers = sorted(
    (p for p in Path(dossier).rglob("*") if p.suffix.lower() in EXTENSIONS),
    key=lambda p: p.stat().st_mtime,
    reverse=True,
)
if not fichiers:
    st.info("Aucune figure dans results/figures/. Lancez visualize.py depuis le module d'exécution.")
    st.stop()

st.caption(f"{len(fichiers)} fichiers dans {dossier}")

col_recherche, col_colonnes, col_rafraichir = st.columns([3, 1, 1])
recherche = col_recherche.text_input("Filtrer par nom de fichier", "")
nb_colonnes = col_colonnes.selectbox("Colonnes", [2, 3, 4], index=1)
if col_rafraichir.button("Rafraîchir"):
    st.rerun()

if recherche:
    fichiers = [p for p in fichiers if recherche.lower() in p.name.lower()]
    if not fichiers:
        st.info("Aucun fichier ne correspond au filtre.")
        st.stop()

images = [p for p in fichiers if p.suffix.lower() in EXTENSIONS_IMAGE]
autres = [p for p in fichiers if p.suffix.lower() not in EXTENSIONS_IMAGE]

if images:
    grille = st.columns(nb_colonnes)
    for index, chemin in enumerate(images):
        with grille[index % nb_colonnes]:
            st.image(str(chemin), use_container_width=True)
            st.caption(f"{chemin.name}, {ui.taille_lisible(chemin.stat().st_size)}")
            st.download_button(
                "Télécharger",
                chemin.read_bytes(),
                file_name=chemin.name,
                key=f"image_{index}",
            )

    st.subheader("Vue détaillée")
    selection = st.selectbox("Figure", images, format_func=lambda p: p.name)
    st.image(str(selection), use_container_width=True, caption=selection.name)

if autres:
    st.subheader("Autres formats")
    for index, chemin in enumerate(autres):
        col_nom, col_action = st.columns([4, 1])
        col_nom.write(f"{chemin.name}, {ui.taille_lisible(chemin.stat().st_size)}")
        col_action.download_button(
            "Télécharger",
            chemin.read_bytes(),
            file_name=chemin.name,
            key=f"autre_{index}",
        )
