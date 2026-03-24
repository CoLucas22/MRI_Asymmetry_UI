"""
Page 3 — Résultats & Figures
"""

import streamlit as st
import os
import glob
from pathlib import Path

st.set_page_config(page_title="Résultats · MRI Asymmetry", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
    .stApp { background: #0a0e1a; color: #e8eaf6; }
    [data-testid="stSidebar"] { background: #050c18 !important; border-right: 1px solid #1565c0 !important; }
    .page-title { font-family:'Syne',sans-serif; font-weight:800; font-size:2rem; color:#e3f2fd; margin-bottom:0.2rem; }
    .page-sub { font-family:'Space Mono',monospace; font-size:0.78rem; color:#64b5f6; margin-bottom:1.5rem; }
    .fig-card {
        background: #0d1b2a; border: 1px solid #1565c0; border-radius: 12px;
        overflow: hidden; transition: all 0.2s;
    }
    .fig-card:hover { border-color: #64b5f6; }
    .fig-meta {
        padding: 0.6rem 0.8rem;
        border-top: 1px solid #1565c0;
    }
    .fig-meta .fname { font-family:'Space Mono',monospace; color:#80cbc4; font-size:0.72rem; }
    .fig-meta .fsize { color:#64b5f6; font-size:0.68rem; }
    .stButton > button {
        background: linear-gradient(135deg, #1565c0, #0d47a1);
        color: #e3f2fd; border: 1px solid #1976d2; border-radius: 8px;
        font-family: 'Space Mono', monospace; font-size: 0.8rem;
    }
    .empty-state {
        text-align: center; padding: 3rem; color: #37474f;
        border: 2px dashed #1565c0; border-radius: 14px;
    }
    .empty-state .icon { font-size: 3rem; margin-bottom: 0.8rem; }
    .empty-state p { font-family:'Space Mono',monospace; font-size:0.8rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### 🧠 MRI Asymmetry")
    st.markdown("Naviguez via le **menu à gauche** ↑")
    st.divider()
    st.markdown(
        "<p style='font-family:Space Mono,monospace;font-size:0.65rem;color:#37474f;'>v1.0.0 · Dyliss · INRIA Rennes</p>",
        unsafe_allow_html=True,
    )


st.markdown('<div class="page-title">📊 Résultats & Figures</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Figures exportées par le pipeline · results/figures/</div>', unsafe_allow_html=True)

pipeline_root = st.session_state.get("pipeline_root", "")

if not pipeline_root:
    st.warning("⚠️ Configurez le chemin du pipeline sur la page **Accueil**.")
    st.stop()

# ── Chemin figures ─────────────────────────────────────────────────────────
figures_dir = os.path.join(pipeline_root, "results", "figures")
os.makedirs(figures_dir, exist_ok=True)

# Tous les fichiers image
exts = ["*.png", "*.jpg", "*.jpeg", "*.svg", "*.pdf"]
all_figures = []
for ext in exts:
    all_figures += glob.glob(os.path.join(figures_dir, "**", ext), recursive=True)
    all_figures += glob.glob(os.path.join(figures_dir, ext))

all_figures = sorted(set(all_figures), key=os.path.getmtime, reverse=True)

# ── Toolbar ────────────────────────────────────────────────────────────────
top_col1, top_col2, top_col3 = st.columns([2, 1, 1])
with top_col1:
    st.markdown(
        f"<p style='color:#90caf9;font-size:0.85rem;margin-top:0.5rem'>"
        f"📁 Répertoire : <code style='color:#80cbc4'>{figures_dir}</code></p>",
        unsafe_allow_html=True,
    )
with top_col2:
    if st.button("🔄 Rafraîchir"):
        st.rerun()
with top_col3:
    cols_count = st.selectbox("Colonnes", [2, 3, 4], index=1, label_visibility="collapsed")

st.divider()

if not all_figures:
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon">🖼️</div>
            <p>Aucune figure trouvée dans results/figures/</p>
            <p style="margin-top:0.5rem;color:#546e7a">Lancez d'abord visualize.py depuis le module Pipeline</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(f"**{len(all_figures)} figure(s) disponible(s)**")

    # ── Filtre ────────────────────────────────────────────────────────────
    search = st.text_input("🔍 Rechercher", placeholder="Nom de fichier…", label_visibility="collapsed")
    if search:
        all_figures = [f for f in all_figures if search.lower() in os.path.basename(f).lower()]

    # ── Grille ────────────────────────────────────────────────────────────
    cols = st.columns(cols_count)
    for idx, fig_path in enumerate(all_figures):
        with cols[idx % cols_count]:
            fname = os.path.basename(fig_path)
            fsize = os.path.getsize(fig_path)
            fsize_str = f"{fsize/1024:.1f} Ko" if fsize < 1_000_000 else f"{fsize/1_000_000:.1f} Mo"
            ext = Path(fig_path).suffix.lower()

            if ext in [".png", ".jpg", ".jpeg"]:
                st.image(fig_path, use_container_width=True)
                st.markdown(
                    f"""
                    <div class="fig-meta">
                        <div class="fname">🖼 {fname}</div>
                        <div class="fsize">{fsize_str}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                with open(fig_path, "rb") as f:
                    st.download_button(
                        label="⬇ Télécharger",
                        data=f,
                        file_name=fname,
                        mime="image/png",
                        key=f"dl_{idx}",
                    )
            else:
                st.markdown(
                    f"""
                    <div class="fig-card" style="padding:1.5rem;text-align:center;">
                        <div style="font-size:2.5rem">📄</div>
                        <div class="fig-meta">
                            <div class="fname">{fname}</div>
                            <div class="fsize">{fsize_str} · {ext}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                with open(fig_path, "rb") as f:
                    st.download_button(
                        label="⬇ Télécharger",
                        data=f,
                        file_name=fname,
                        key=f"dl_{idx}",
                    )

    st.divider()

    # ── Vue détaillée ─────────────────────────────────────────────────────
    st.markdown("### 🔬 Vue détaillée")
    image_files = [f for f in all_figures if Path(f).suffix.lower() in [".png", ".jpg", ".jpeg"]]
    if image_files:
        selected = st.selectbox(
            "Sélectionner une figure",
            image_files,
            format_func=os.path.basename,
        )
        st.image(selected, use_container_width=True, caption=os.path.basename(selected))
    else:
        st.info("Aucune image disponible pour la vue détaillée.")
