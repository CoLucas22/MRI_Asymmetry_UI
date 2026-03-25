"""
Page 1 — Upload & prévisualisation de fichiers DICOM
"""

import streamlit as st
import os
import tempfile
import numpy as np

st.set_page_config(page_title="Upload DICOM · MRI Asymmetry", page_icon="📂", layout="wide")

# ── CSS partagé ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: '', sans-serif; }
    .stApp { background: #f8f9fa; color: #1a1d23; }
    [data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #e2e5ea !important; }
    .page-title { font-family:'',sans-serif; font-weight:800; font-size:2rem; color:#111318; margin-bottom:0.2rem; }
    .page-sub { font-family:'Space Mono',monospace; font-size:0.78rem; color:#6b7280; margin-bottom:1.5rem; }
    .file-card {
        background: #ffffff; border: 1px solid #e2e5ea; border-radius: 12px;
        padding: 1rem 1.2rem; margin-bottom: 0.6rem;
    }
    .file-card .fname { font-family:'Space Mono',monospace; color:#111318; font-size:0.85rem; }
    .file-card .fmeta { color:#6b7280; font-size:0.75rem; margin-top:0.2rem; }
    .stButton > button {
        background: linear-gradient(135deg, #e2e5ea, #111318);
        color: #111318; border: 1px solid #2d3240; border-radius: 8px;
        font-family: 'Space Mono', monospace; font-size: 0.8rem;
    }
    .stButton > button:hover { background: linear-gradient(135deg,#2d3240,#e2e5ea); border-color:#6b7280; }
    div[data-testid="stFileUploadDropzone"] {
        background: #ffffff !important; border: 2px dashed #e2e5ea !important;
        border-radius: 12px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### 🧠 MRI Asymmetry")
    st.markdown("Naviguez via le **menu à gauche** ↑")
    st.divider()
    st.markdown(
        "<p style='font-family:Space Mono,monospace;font-size:0.65rem;color:#37474f;'>v1.0.0 · BioGraphs · INRIA Rennes</p>",
        unsafe_allow_html=True,
    )


st.markdown('<div class="page-title">📂 Upload DICOM</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Chargez des fichiers .DCM et prévisualisez les coupes IRM</div>', unsafe_allow_html=True)

# ── Onglets ───────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["⬆️  Upload de fichiers", "📁  Parcourir le répertoire local"])

# ─── TAB 1 : Upload ────────────────────────────────────────────────────────
with tab1:
    uploaded = st.file_uploader(
        "Glissez-déposez vos fichiers DICOM (.DCM)",
        type=["dcm", "DCM"],
        accept_multiple_files=True,
        help="Formats acceptés : .dcm, .DCM",
    )

    if uploaded:
        st.success(f"✅ {len(uploaded)} fichier(s) chargé(s)")

        cols = st.columns(3)
        for i, f in enumerate(uploaded):
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div class="file-card">
                        <div class="fname">🗂 {f.name}</div>
                        <div class="fmeta">Taille : {f.size / 1024:.1f} Ko</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.divider()
        st.markdown("#### 🔍 Prévisualisation d'une coupe")

        selected = st.selectbox("Sélectionner un fichier à visualiser", [f.name for f in uploaded])
        sel_file = next(f for f in uploaded if f.name == selected)

        try:
            import pydicom
            with tempfile.NamedTemporaryFile(suffix=".dcm", delete=False) as tmp:
                tmp.write(sel_file.read())
                tmp_path = tmp.name

            ds = pydicom.dcmread(tmp_path)
            pixel_array = ds.pixel_array

            col_info, col_img = st.columns([1, 2])
            with col_info:
                st.markdown("**Métadonnées DICOM**")
                meta = {
                    "Patient ID": getattr(ds, "PatientID", "N/A"),
                    "Modality": getattr(ds, "Modality", "N/A"),
                    "Rows × Cols": f"{getattr(ds, 'Rows', '?')} × {getattr(ds, 'Columns', '?')}",
                    "Pixel Spacing": str(getattr(ds, "PixelSpacing", "N/A")),
                    "Slice Thickness": str(getattr(ds, "SliceThickness", "N/A")),
                    "Study Date": str(getattr(ds, "StudyDate", "N/A")),
                }
                for k, v in meta.items():
                    st.markdown(
                        f"<div style='display:flex;justify-content:space-between;padding:0.3rem 0;"
                        f"border-bottom:1px solid #e2e5ea;font-size:0.82rem;'>"
                        f"<span style='color:#6b7280;font-family:Space Mono,monospace'>{k}</span>"
                        f"<span style='color:#111318'>{v}</span></div>",
                        unsafe_allow_html=True,
                    )

            with col_img:
                # Normalize for display
                arr = pixel_array.astype(float)
                arr = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8) * 255
                st.image(arr.astype(np.uint8), caption=f"Coupe IRM — {selected}", use_container_width=True, clamp=True)

            os.unlink(tmp_path)

        except ImportError:
            st.warning("⚠️ `pydicom` n'est pas installé. Installez-le avec `pip install pydicom`.")
            st.info("Aperçu indisponible — les métadonnées seront affichées une fois pydicom installé.")
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier DICOM : {e}")

    else:
        st.info("Aucun fichier chargé. Glissez-déposez des fichiers `.DCM` ci-dessus.")

# ─── TAB 2 : Parcourir répertoire local ───────────────────────────────────
with tab2:
    
    default_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MRI_Asymmetry_Analysis_Pipeline")
    pipeline_root = st.session_state.get("pipeline_root", os.path.normpath(default_root))

    if not pipeline_root:
        st.warning("⚠️ Configurez d'abord le chemin du pipeline sur la page **Accueil**.")
    else:
        mri_dir = os.path.join(pipeline_root, "data_example", "MRIs")
        if not os.path.isdir(mri_dir):
            st.error(f"Répertoire introuvable : `{mri_dir}`")
        else:
            dcm_files = []
            for root_d, _, files in os.walk(mri_dir):
                for f in files:
                    if f.lower().endswith(".dcm"):
                        dcm_files.append(os.path.join(root_d, f))

            if not dcm_files:
                st.info("Aucun fichier .DCM trouvé dans le répertoire.")
            else:
                st.success(f"✅ {len(dcm_files)} fichier(s) DICOM trouvé(s) dans `{mri_dir}`")

                # Arborescence
                tree = {}
                for path in dcm_files:
                    rel = os.path.relpath(path, mri_dir)
                    parts = rel.split(os.sep)
                    patient = parts[0] if len(parts) > 1 else "Racine"
                    tree.setdefault(patient, []).append(path)

                for patient, files_list in tree.items():
                    with st.expander(f"📁 {patient}  ({len(files_list)} fichiers)"):
                        for fp in files_list:
                            rel = os.path.relpath(fp, mri_dir)
                            size = os.path.getsize(fp) / 1024
                            st.markdown(
                                f"<div class='file-card'>"
                                f"<div class='fname'>🗂 {rel}</div>"
                                f"<div class='fmeta'>{size:.1f} Ko · {fp}</div>"
                                f"</div>",
                                unsafe_allow_html=True,
                            )
