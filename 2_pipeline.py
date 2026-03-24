"""
Page 2 — Lancement du pipeline via subprocess
"""

import streamlit as st
import subprocess
import os
import sys
import threading
import time
from datetime import datetime

st.set_page_config(page_title="Pipeline · MRI Asymmetry", page_icon="⚙️", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
    .stApp { background: #0a0e1a; color: #e8eaf6; }
    [data-testid="stSidebar"] { background: #050c18 !important; border-right: 1px solid #1565c0 !important; }
    .page-title { font-family:'Syne',sans-serif; font-weight:800; font-size:2rem; color:#e3f2fd; margin-bottom:0.2rem; }
    .page-sub { font-family:'Space Mono',monospace; font-size:0.78rem; color:#64b5f6; margin-bottom:1.5rem; }
    .script-card {
        background: #0d1b2a; border: 1px solid #1565c0; border-radius: 14px;
        padding: 1.5rem; height: 100%;
    }
    .script-card h4 { color: #e3f2fd; margin: 0 0 0.4rem 0; font-size: 1rem; }
    .script-card .lang-badge {
        display: inline-block; padding: 0.15rem 0.6rem;
        border-radius: 999px; font-family:'Space Mono',monospace;
        font-size: 0.65rem; font-weight:700; margin-bottom:0.6rem;
    }
    .lang-py { background:#1a3a2a; color:#80cbc4; border:1px solid #388e3c; }
    .lang-r  { background:#1a2a3a; color:#64b5f6; border:1px solid #1565c0; }
    .script-card p { color:#90caf9; font-size:0.82rem; margin:0 0 1rem 0; }
    .script-card code { color:#80cbc4; font-family:'Space Mono',monospace; font-size:0.75rem; }
    .log-box {
        background: #050c18; border: 1px solid #1565c0; border-radius: 10px;
        padding: 1rem 1.2rem; font-family:'Space Mono',monospace; font-size:0.75rem;
        color: #80cbc4; max-height: 320px; overflow-y: auto; white-space: pre-wrap;
    }
    .status-ok   { color: #66bb6a; }
    .status-err  { color: #ef5350; }
    .status-run  { color: #ffa726; }
    .stButton > button {
        background: linear-gradient(135deg, #1565c0, #0d47a1);
        color: #e3f2fd; border: 1px solid #1976d2; border-radius: 8px;
        font-family: 'Space Mono', monospace; font-size: 0.8rem;
        width: 100%; margin-top: 0.5rem;
    }
    .stButton > button:hover { background: linear-gradient(135deg,#1976d2,#1565c0); border-color:#64b5f6; }
    .stTextInput > div > input {
        background: #0d1b2a !important; color: #e3f2fd !important;
        border: 1px solid #1565c0 !important; border-radius: 8px !important;
        font-family: 'Space Mono', monospace !important; font-size: 0.82rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### 🧠 MRI Asymmetry")
    st.page_link("app.py", label="🏠  Accueil")
    st.page_link("pages/1_upload.py", label="📂  Upload DICOM")
    st.page_link("pages/2_pipeline.py", label="⚙️  Lancer le Pipeline")
    st.page_link("pages/3_results.py", label="📊  Résultats & Figures")
    st.page_link("pages/4_datasets.py", label="🗃️  Datasets CSV")

st.markdown('<div class="page-title">⚙️ Lancer le Pipeline</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Exécution des scripts Python & R via subprocess</div>', unsafe_allow_html=True)

pipeline_root = st.session_state.get("pipeline_root", "")

if not pipeline_root:
    st.warning("⚠️ Configurez le chemin du pipeline sur la page **Accueil** avant de lancer les scripts.")
    st.stop()

# ── Helpers ───────────────────────────────────────────────────────────────────
def run_script(cmd: list, cwd: str) -> tuple[int, str, str]:
    """Run a subprocess and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "⏱ Timeout : le script a dépassé 5 minutes."
    except FileNotFoundError as e:
        return -1, "", f"Commande introuvable : {e}"
    except Exception as e:
        return -1, "", str(e)


def log_entry(icon, text, color="#80cbc4"):
    ts = datetime.now().strftime("%H:%M:%S")
    return f'<span style="color:#37474f">[{ts}]</span> {icon} <span style="color:{color}">{text}</span>\n'


# ── Initialisation session ─────────────────────────────────────────────────
if "logs" not in st.session_state:
    st.session_state["logs"] = ""


# ── Script cards ──────────────────────────────────────────────────────────────
scripts = [
    {
        "id": "preprocess",
        "title": "preprocess.py",
        "lang": "Python",
        "badge": "lang-py",
        "desc": "Prétraitement des images IRM DICOM. Normalisation, recadrage et export des arrays.",
        "default_args": "--input data_example/MRIs/Patient_1/MRI_1/export_00062.DCM",
        "cmd_template": [sys.executable, "python_scripts/preprocess.py"],
    },
    {
        "id": "extract",
        "title": "extract_features.py",
        "lang": "Python",
        "badge": "lang-py",
        "desc": "Extraction des features d'asymétrie gauche/droite sur les coupes axiales.",
        "default_args": "",
        "cmd_template": [sys.executable, "python_scripts/extract_features.py"],
    },
    {
        "id": "visualize",
        "title": "visualize.py",
        "lang": "Python",
        "badge": "lang-py",
        "desc": "Génération des figures et heatmaps d'asymétrie. Outputs dans results/figures/.",
        "default_args": "--input data_example/MRIs/Patient_1/MRI_1/export_00062.DCM",
        "cmd_template": [sys.executable, "python_scripts/visualize.py"],
    },
    {
        "id": "r_class",
        "title": "classification_task.R",
        "lang": "R",
        "badge": "lang-r",
        "desc": "Régression logistique sur train_dataset.csv, prédictions sur validation_dataset.csv.",
        "default_args": "data_example/train_dataset.csv data_example/validation_dataset.csv",
        "cmd_template": ["Rscript", "R_scripts/classification_task.R"],
    },
]

# ── Run all ───────────────────────────────────────────────────────────────────
st.markdown("### 🚀 Exécution globale")
col_all1, col_all2, col_all3 = st.columns([2, 1, 1])
with col_all1:
    st.markdown(
        "<p style='color:#90caf9;font-size:0.85rem;margin-top:0.6rem'>"
        "Lance tous les scripts dans l'ordre : preprocess → extract → visualize → R</p>",
        unsafe_allow_html=True,
    )
with col_all2:
    run_all = st.button("▶ Lancer tout le pipeline")
with col_all3:
    clear_logs = st.button("🗑 Effacer les logs")

if clear_logs:
    st.session_state["logs"] = ""

st.divider()

# ── Script individuel cards ───────────────────────────────────────────────────
st.markdown("### 📋 Scripts individuels")

cols = st.columns(2)
args_store = {}

for i, s in enumerate(scripts):
    with cols[i % 2]:
        st.markdown(
            f"""
            <div class="script-card">
                <span class="lang-badge {s['badge']}">{s['lang']}</span>
                <h4>🔧 {s['title']}</h4>
                <p>{s['desc']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        args_key = f"args_{s['id']}"
        if args_key not in st.session_state:
            st.session_state[args_key] = s["default_args"]

        args = st.text_input(
            f"Arguments pour {s['title']}",
            value=st.session_state[args_key],
            key=args_key,
            label_visibility="collapsed",
            placeholder=f"Arguments optionnels…",
        )
        args_store[s["id"]] = args

        if st.button(f"▶ Lancer {s['title']}", key=f"run_{s['id']}"):
            with st.spinner(f"Exécution de {s['title']}…"):
                cmd = s["cmd_template"][:]
                if args.strip():
                    cmd += args.strip().split()
                rc, out, err = run_script(cmd, cwd=pipeline_root)
                if rc == 0:
                    st.session_state["logs"] += log_entry("✅", f"{s['title']} terminé avec succès.", "#66bb6a")
                    if out:
                        st.session_state["logs"] += out + "\n"
                    st.success(f"✅ {s['title']} terminé (code {rc})")
                else:
                    st.session_state["logs"] += log_entry("❌", f"{s['title']} échoué (code {rc}).", "#ef5350")
                    if err:
                        st.session_state["logs"] += err + "\n"
                    st.error(f"❌ Erreur lors de l'exécution (code {rc})")

        st.markdown("<br>", unsafe_allow_html=True)

# ── Run All logic ──────────────────────────────────────────────────────────
if run_all:
    progress = st.progress(0, text="Démarrage du pipeline…")
    for idx, s in enumerate(scripts):
        progress.progress((idx) / len(scripts), text=f"Exécution : {s['title']}…")
        cmd = s["cmd_template"][:]
        args = st.session_state.get(f"args_{s['id']}", s["default_args"])
        if args.strip():
            cmd += args.strip().split()
        rc, out, err = run_script(cmd, cwd=pipeline_root)
        if rc == 0:
            st.session_state["logs"] += log_entry("✅", f"{s['title']} OK", "#66bb6a")
            if out:
                st.session_state["logs"] += out + "\n"
        else:
            st.session_state["logs"] += log_entry("❌", f"{s['title']} FAILED (code {rc})", "#ef5350")
            if err:
                st.session_state["logs"] += err + "\n"
            st.error(f"Pipeline interrompu à l'étape {s['title']}")
            progress.empty()
            break
    else:
        progress.progress(1.0, text="✅ Pipeline complet !")
        st.success("🎉 Tous les scripts ont été exécutés avec succès.")

# ── Console de logs ──────────────────────────────────────────────────────────
st.divider()
st.markdown("### 📟 Console de sortie")

logs_html = st.session_state.get("logs", "<span style='color:#37474f'>Aucune sortie pour l'instant…</span>")
st.markdown(f'<div class="log-box">{logs_html}</div>', unsafe_allow_html=True)
