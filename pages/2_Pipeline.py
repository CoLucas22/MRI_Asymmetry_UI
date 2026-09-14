"""Exécution des scripts du pipeline."""

from __future__ import annotations

import glob
import shutil
import subprocess
import sys
from datetime import datetime

import streamlit as st

import ui

DELAI_MAX = 300  # secondes par script


def chemin_rscript() -> str:
    """Localise Rscript dans le PATH, puis dans les installations Windows."""
    trouve = shutil.which("Rscript")
    if trouve:
        return trouve
    installations = sorted(glob.glob(r"C:\Program Files\R\R-*\bin\Rscript.exe"))
    return installations[-1] if installations else "Rscript"


ui.header("Exécution du pipeline", "Lancement des scripts Python et R dans le dépôt configuré.")
racine = ui.require_pipeline_root()

SCRIPTS = [
    {
        "id": "preprocess",
        "nom": "preprocess.py",
        "langage": "Python",
        "description": "Prétraitement des IRM DICOM : normalisation, recadrage, export des tableaux.",
        "commande": [sys.executable, "python_scripts/preprocess.py"],
        "arguments": "--input data_example/MRIs/Patient_1/MRI_1/export_00062.DCM",
    },
    {
        "id": "extract",
        "nom": "extract_features.py",
        "langage": "Python",
        "description": "Extraction des descripteurs d'asymétrie gauche/droite sur les coupes axiales.",
        "commande": [sys.executable, "python_scripts/extract_features.py"],
        "arguments": "",
    },
    {
        "id": "visualize",
        "nom": "visualize.py",
        "langage": "Python",
        "description": "Génération des figures et des cartes d'asymétrie dans results/figures/.",
        "commande": [sys.executable, "python_scripts/visualize.py"],
        "arguments": "--input data_example/MRIs/Patient_1/MRI_1/export_00062.DCM",
    },
    {
        "id": "classification",
        "nom": "classification_task.R",
        "langage": "R",
        "description": "Régression logistique sur train_dataset.csv, prédiction sur validation_dataset.csv.",
        "commande": [chemin_rscript(), "R_scripts/classification_task.R"],
        "arguments": "data_example/train_dataset.csv data_example/validation_dataset.csv",
    },
]

st.session_state.setdefault("journal", [])


def journaliser(ligne: str) -> None:
    st.session_state["journal"].append(f"[{datetime.now():%H:%M:%S}] {ligne}")


def executer(script: dict, arguments: str) -> bool:
    """Lance un script et consigne sa sortie. Renvoie True en cas de succès."""
    commande = script["commande"] + arguments.split()
    try:
        resultat = subprocess.run(
            commande,
            cwd=racine,
            capture_output=True,
            text=True,
            timeout=DELAI_MAX,
        )
    except subprocess.TimeoutExpired:
        journaliser(f"{script['nom']} : délai de {DELAI_MAX} s dépassé.")
        return False
    except OSError as erreur:
        journaliser(f"{script['nom']} : commande introuvable ({erreur}).")
        return False

    if resultat.returncode == 0:
        journaliser(f"{script['nom']} : terminé.")
    else:
        journaliser(f"{script['nom']} : échec, code {resultat.returncode}.")
    for bloc in (resultat.stdout, resultat.stderr):
        if bloc and bloc.strip():
            st.session_state["journal"].append(bloc.strip())
    return resultat.returncode == 0


col_tout, col_vider = st.columns([1, 3])
lancer_tout = col_tout.button("Exécuter les quatre scripts", type="primary")
if col_vider.button("Effacer le journal"):
    st.session_state["journal"] = []

colonnes = st.columns(2)
for index, script in enumerate(SCRIPTS):
    with colonnes[index % 2].container(border=True):
        st.markdown(f"**{script['nom']}** ({script['langage']})")
        st.caption(script["description"])
        arguments = st.text_input(
            "Arguments",
            value=script["arguments"],
            key=f"args_{script['id']}",
            placeholder="Arguments de ligne de commande",
        )
        if st.button(f"Exécuter {script['nom']}", key=f"run_{script['id']}"):
            with st.spinner(f"Exécution de {script['nom']}"):
                executer(script, arguments)

if lancer_tout:
    with st.status("Exécution du pipeline", expanded=True) as etat:
        for script in SCRIPTS:
            st.write(script["nom"])
            arguments = st.session_state.get(f"args_{script['id']}", script["arguments"])
            if not executer(script, arguments):
                etat.update(label=f"Interrompu à l'étape {script['nom']}", state="error")
                break
        else:
            etat.update(label="Pipeline terminé", state="complete")

st.subheader("Journal")
journal = st.session_state["journal"]
st.code("\n".join(journal) if journal else "Aucune sortie pour le moment.", language=None)
