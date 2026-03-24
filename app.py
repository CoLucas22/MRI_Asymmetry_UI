"""
MRI Asymmetry Analysis — Streamlit UI
Entry point: runs the main dashboard.
"""

import streamlit as st

st.set_page_config(
    page_title="MRI Asymmetry Analysis",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Syne', sans-serif;
    }
    .stApp {
        background: #0a0e1a;
        color: #e8eaf6;
    }
    .main-header {
        background: linear-gradient(135deg, #0d1b2a 0%, #1a237e 50%, #0d47a1 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        border: 1px solid #1565c0;
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(100,181,246,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .main-header h1 {
        font-family: 'Syne', sans-serif;
        font-weight: 800;
        font-size: 2.4rem;
        color: #e3f2fd;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .main-header p {
        color: #90caf9;
        font-size: 1rem;
        margin-top: 0.4rem;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
    }
    .metric-card {
        background: #0d1b2a;
        border: 1px solid #1565c0;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }
    .metric-card .label {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        color: #64b5f6;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: 800;
        color: #e3f2fd;
        line-height: 1.2;
    }
    .nav-card {
        background: #0d1b2a;
        border: 1px solid #1565c0;
        border-radius: 14px;
        padding: 1.5rem;
        transition: all 0.2s ease;
        cursor: pointer;
        height: 100%;
    }
    .nav-card:hover {
        border-color: #64b5f6;
        background: #132030;
        transform: translateY(-2px);
    }
    .nav-card .icon {
        font-size: 2rem;
        margin-bottom: 0.8rem;
    }
    .nav-card h3 {
        font-weight: 700;
        color: #e3f2fd;
        margin: 0 0 0.4rem 0;
    }
    .nav-card p {
        color: #90caf9;
        font-size: 0.85rem;
        margin: 0;
        font-family: 'Space Mono', monospace;
    }
    [data-testid="stSidebar"] {
        background: #050c18 !important;
        border-right: 1px solid #1565c0 !important;
    }
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0 1.5rem;
        border-bottom: 1px solid #1565c0;
        margin-bottom: 1rem;
    }
    .sidebar-logo span {
        font-size: 2.5rem;
    }
    .sidebar-logo p {
        font-family: 'Space Mono', monospace;
        font-size: 0.7rem;
        color: #64b5f6;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.3rem;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Space Mono', monospace !important;
        color: #64b5f6 !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1565c0, #0d47a1);
        color: #e3f2fd;
        border: 1px solid #1976d2;
        border-radius: 8px;
        font-family: 'Space Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 0.05em;
        padding: 0.6rem 1.5rem;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1976d2, #1565c0);
        border-color: #64b5f6;
        transform: translateY(-1px);
    }
    .pipeline-step {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.8rem 1rem;
        border-left: 3px solid #1565c0;
        margin-bottom: 0.5rem;
        background: #0a1628;
        border-radius: 0 8px 8px 0;
    }
    .pipeline-step .step-num {
        font-family: 'Space Mono', monospace;
        color: #64b5f6;
        font-weight: 700;
        font-size: 1.1rem;
        min-width: 2rem;
    }
    .pipeline-step .step-text {
        color: #b3c5e0;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-logo">
            <span>🧠</span>
            <p>MRI Asymmetry</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("Naviguez via le **menu ci-dessus** ↑")
    st.divider()
    st.markdown(
        "<p style=\'font-family:Space Mono,monospace;font-size:0.65rem;color:#37474f;text-align:center;\'>v1.0.0 · Dyliss Team · INRIA Rennes</p>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown(
        """
        <p style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#37474f;text-align:center;">
        v1.0.0 · Dyliss Team · INRIA Rennes
        </p>
        """,
        unsafe_allow_html=True,
    )

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="main-header">
        <h1>🧠 MRI Asymmetry Analysis</h1>
        <p>Pipeline d'analyse d'asymétrie sur IRM axiales — Biomarqueurs microbiome & Maladie de Crohn</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Metrics rapides ───────────────────────────────────────────────────────────
import os, glob

pipeline_root = st.session_state.get("pipeline_root", "")

def count_files(pattern):
    if not pipeline_root:
        return "—"
    files = glob.glob(os.path.join(pipeline_root, pattern), recursive=True)
    return len(files)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Fichiers DICOM", count_files("data_example/MRIs/**/*.DCM"))
with col2:
    st.metric("CSV disponibles", count_files("data_example/CSV_files/*.csv"))
with col3:
    st.metric("Figures générées", count_files("results/figures/*.png") if pipeline_root else "—")
with col4:
    st.metric("Scripts Python", "4")

st.divider()

# ── Navigation cards ──────────────────────────────────────────────────────────
st.markdown("### Modules disponibles")
c1, c2, c3, c4 = st.columns(4)

cards = [
    ("📂", "Upload DICOM", "Charger des fichiers `.DCM` et prévisualiser les coupes IRM.", "pages/1_upload.py"),
    ("⚙️", "Lancer le Pipeline", "Exécuter `preprocess.py`, `extract_features.py`, `visualize.py` et le script R.", "pages/2_pipeline.py"),
    ("📊", "Résultats & Figures", "Explorer les figures exportées et les métriques d'asymétrie.", "pages/3_results.py"),
    ("🗃️", "Datasets CSV", "Consulter train, validation et runs datasets.", "pages/4_datasets.py"),
]

for col, (icon, title, desc, _) in zip([c1, c2, c3, c4], cards):
    with col:
        st.markdown(
            f"""
            <div class="nav-card">
                <div class="icon">{icon}</div>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ── Pipeline overview ─────────────────────────────────────────────────────────
st.markdown("### Vue d'ensemble du pipeline")

steps = [
    ("01", "preprocess.py", "Prétraitement des images IRM (DICOM → array normalisé)"),
    ("02", "extract_features.py", "Extraction des features d'asymétrie gauche/droite"),
    ("03", "visualize.py", "Génération des figures et heatmaps"),
    ("04", "classification_task.R", "Régression logistique & prédictions (script R)"),
]

for num, script, desc in steps:
    st.markdown(
        f"""
        <div class="pipeline-step">
            <span class="step-num">{num}</span>
            <div>
                <code style="color:#80cbc4;font-size:0.85rem;">{script}</code>
                <div class="step-text">{desc}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ── Config du chemin racine ───────────────────────────────────────────────────
st.markdown("### ⚙️ Configuration")
with st.expander("Chemin vers le repo MRI_Asymmetry_Analysis_Pipeline"):
    root = st.text_input(
        "Chemin absolu du pipeline",
        value=st.session_state.get("pipeline_root", ""),
        placeholder="/home/user/MRI_Asymmetry_Analysis_Pipeline",
    )
    if st.button("💾 Enregistrer"):
        st.session_state["pipeline_root"] = root
        st.success(f"Chemin enregistré : `{root}`")
