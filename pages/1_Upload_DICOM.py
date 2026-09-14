"""Chargement et aperçu de fichiers DICOM."""

from __future__ import annotations

import io
import os
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

import ui

ui.header("Upload DICOM", "Chargement de fichiers .DCM et aperçu des coupes.")


def apercu(donnees: bytes, legende: str) -> None:
    """Affiche les métadonnées et l'image d'une coupe DICOM."""
    try:
        import pydicom
    except ImportError:
        st.warning("pydicom n'est pas installé. Lancez `pip install pydicom`.")
        return

    try:
        ds = pydicom.dcmread(io.BytesIO(donnees))
        pixels = ds.pixel_array.astype(float)
    except Exception as erreur:  # fichier corrompu, syntaxe de transfert non gérée
        st.error(f"Lecture impossible : {erreur}")
        return

    col_meta, col_image = st.columns([1, 2])
    with col_meta:
        champs = {
            "Patient": getattr(ds, "PatientID", "inconnu"),
            "Modalité": getattr(ds, "Modality", "inconnue"),
            "Dimensions": f"{getattr(ds, 'Rows', '?')} x {getattr(ds, 'Columns', '?')}",
            "Espacement des pixels": str(getattr(ds, "PixelSpacing", "inconnu")),
            "Épaisseur de coupe": str(getattr(ds, "SliceThickness", "inconnue")),
            "Date d'examen": str(getattr(ds, "StudyDate", "inconnue")),
        }
        st.dataframe(
            pd.DataFrame({"Champ": list(champs), "Valeur": list(champs.values())}),
            hide_index=True,
            use_container_width=True,
        )
    with col_image:
        etendue = float(pixels.max() - pixels.min())
        if etendue == 0:
            st.warning("Coupe uniforme : aucun contraste à afficher.")
            return
        normalise = (pixels - pixels.min()) / etendue * 255
        st.image(normalise.astype(np.uint8), caption=legende, use_container_width=True)


onglet_fichiers, onglet_depot = st.tabs(["Fichiers chargés", "Répertoire du pipeline"])

with onglet_fichiers:
    charges = st.file_uploader(
        "Fichiers DICOM",
        type=["dcm", "DCM"],
        accept_multiple_files=True,
    )

    if not charges:
        st.info("Glissez des fichiers .DCM dans la zone ci-dessus pour les prévisualiser.")
    else:
        st.dataframe(
            pd.DataFrame(
                {
                    "Fichier": [f.name for f in charges],
                    "Taille": [ui.taille_lisible(f.size) for f in charges],
                }
            ),
            hide_index=True,
            use_container_width=True,
        )
        choix = st.selectbox("Coupe à prévisualiser", [f.name for f in charges])
        selection = next(f for f in charges if f.name == choix)
        apercu(selection.getvalue(), choix)

with onglet_depot:
    racine = ui.pipeline_root()
    dossier_irm = os.path.join(racine, "data_example", "MRIs") if racine else ""

    if not dossier_irm or not os.path.isdir(dossier_irm):
        st.warning(
            "Répertoire data_example/MRIs introuvable. "
            "Vérifiez le chemin du dépôt sur la page d'accueil."
        )
    else:
        coupes = sorted(
            p for p in Path(dossier_irm).rglob("*") if p.suffix.lower() == ".dcm"
        )
        if not coupes:
            st.info(f"Aucun fichier .DCM sous {dossier_irm}.")
        else:
            table = pd.DataFrame(
                {
                    "Patient": [p.relative_to(dossier_irm).parts[0] for p in coupes],
                    "Fichier": [str(p.relative_to(dossier_irm)) for p in coupes],
                    "Taille": [ui.taille_lisible(p.stat().st_size) for p in coupes],
                }
            )
            st.caption(f"{len(coupes)} fichiers sous {dossier_irm}")

            patient = st.selectbox("Patient", ["Tous"] + sorted(table["Patient"].unique()))
            vue = table if patient == "Tous" else table[table["Patient"] == patient]
            st.dataframe(vue, hide_index=True, use_container_width=True)

            choix = st.selectbox("Coupe à prévisualiser", vue["Fichier"].tolist())
            apercu(Path(dossier_irm, choix).read_bytes(), choix)
