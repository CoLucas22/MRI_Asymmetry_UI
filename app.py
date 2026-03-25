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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stApp {
        background: #f8f9fa;
        color: #1a1d23;
    }
    .main-header {
        background: #ffffff;
        border-radius: 10px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e5ea;
    }
    .main-header h1 {
        font-weight: 700;
        font-size: 1.75rem;
        color: #111318;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .main-header p {
        color: #6b7280;
        font-size: 0.875rem;
        margin-top: 0.3rem;
        font-weight: 400;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e5ea;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        text-align: center;
    }
    .metric-card .label {
        font-size: 0.75rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 500;
    }
    .metric-card .value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #111318;
        line-height: 1.3;
    }
    .nav-card {
        background: #ffffff;
        border: 1px solid #e2e5ea;
        border-radius: 8px;
        padding: 1.5rem;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
        cursor: pointer;
        height: 100%;
    }
    .nav-card:hover {
        border-color: #c5cad3;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .nav-card .icon {
        font-size: 1.5rem;
        margin-bottom: 0.75rem;
    }
    .nav-card h3 {
        font-weight: 600;
        color: #111318;
        margin: 0 0 0.3rem 0;
        font-size: 0.95rem;
    }
    .nav-card p {
        color: #6b7280;
        font-size: 0.8rem;
        margin: 0;
    }
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e2e5ea !important;
    }
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0 1.5rem;
        border-bottom: 1px solid #e2e5ea;
        margin-bottom: 1rem;
    }
    .sidebar-logo span {
        font-size: 2rem;
    }
    .sidebar-logo p {
        font-size: 0.7rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.3rem;
        font-weight: 500;
    }
    div[data-testid="stMetricValue"] {
        color: #111318 !important;
        font-weight: 700 !important;
    }
    .stButton > button {
        background: #111318;
        color: #ffffff;
        border: 1px solid #111318;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 500;
        letter-spacing: 0.02em;
        padding: 0.55rem 1.4rem;
        transition: background 0.15s, border-color 0.15s;
    }
    .stButton > button:hover {
        background: #2d3240;
        border-color: #2d3240;
    }
    .pipeline-step {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem 1rem;
        border-left: 2px solid #d1d5db;
        margin-bottom: 0.4rem;
        background: #ffffff;
        border-radius: 0 6px 6px 0;
    }
    .pipeline-step .step-num {
        color: #374151;
        font-weight: 600;
        font-size: 0.95rem;
        min-width: 1.5rem;
    }
    .pipeline-step .step-text {
        color: #4b5563;
        font-size: 0.875rem;
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
    ("📂", "Upload DICOM", "Charger des fichiers `.DCM` et prévisualiser les coupes IRM.", "1_Upload_DICOM"),
    ("⚙️", "Lancer le Pipeline", "Exécuter `preprocess.py`, `extract_features.py`, `visualize.py` et le script R.", "2_Pipeline"),
    ("📊", "Résultats & Figures", "Explorer les figures exportées et les métriques d'asymétrie.", "3_Resultats"),
    ("🗃️", "Datasets CSV", "Consulter train, validation et runs datasets.", "4_Datasets_CSV"),
]

for col, (icon, title, desc, page) in zip([c1, c2, c3, c4], cards):
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
        if st.button("Ouvrir →", key=f"btn_{page}"):
            st.switch_page(f"pages/{page}.py")

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
                <code style="color:#111318;font-size:0.85rem;">{script}</code>
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