"""Éléments communs aux pages de l'interface MRI Asymmetry."""

from __future__ import annotations

import json
import os
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
CONFIG_FILE = APP_DIR / "config.json"
PIPELINE_VOISIN = APP_DIR / "MRI_Asymmetry_Analysis_Pipeline"

NOM_APP = "MRI Asymmetry Analysis"
VERSION = "1.0.0"


def header(titre: str, description: str = "") -> None:
    """Configure la page et affiche son en-tête. À appeler en premier."""
    st.set_page_config(page_title=f"{titre} - {NOM_APP}", layout="wide")
    with st.sidebar:
        st.caption(f"{NOM_APP} {VERSION}")
        st.caption("Équipe BioGraphs, IRISA / Inria Rennes")
    st.title(titre)
    if description:
        st.caption(description)


def pipeline_root() -> str:
    """Chemin du dépôt pipeline, mémorisé d'une session à l'autre."""
    if "pipeline_root" not in st.session_state:
        st.session_state["pipeline_root"] = _chemin_enregistre()
    return st.session_state["pipeline_root"]


def set_pipeline_root(chemin: str) -> str:
    """Normalise, mémorise et enregistre le chemin saisi."""
    propre = os.path.normpath(os.path.expanduser(chemin.strip())) if chemin.strip() else ""
    st.session_state["pipeline_root"] = propre
    try:
        CONFIG_FILE.write_text(json.dumps({"pipeline_root": propre}), encoding="utf-8")
    except OSError:
        pass  # le chemin reste valable pour la session en cours
    return propre


def require_pipeline_root() -> str:
    """Arrête la page tant que le dépôt pipeline n'est pas configuré."""
    racine = pipeline_root()
    if not racine or not os.path.isdir(racine):
        st.warning("Renseignez le chemin du dépôt pipeline sur la page d'accueil.")
        st.stop()
    return racine


def taille_lisible(octets: float) -> str:
    """Formate une taille de fichier en Ko ou Mo."""
    if octets < 1_000_000:
        return f"{octets / 1024:.1f} Ko"
    return f"{octets / 1_000_000:.1f} Mo"


def _chemin_enregistre() -> str:
    try:
        enregistre = json.loads(CONFIG_FILE.read_text(encoding="utf-8")).get("pipeline_root", "")
    except (OSError, ValueError):
        enregistre = ""
    if enregistre:
        return enregistre
    return str(PIPELINE_VOISIN) if PIPELINE_VOISIN.is_dir() else ""
