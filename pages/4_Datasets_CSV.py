"""
Page 4 — Tableau de bord des datasets CSV
"""

import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="Datasets · MRI Asymmetry", page_icon="🗃️", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
    .stApp { background: #0a0e1a; color: #e8eaf6; }
    [data-testid="stSidebar"] { background: #050c18 !important; border-right: 1px solid #1565c0 !important; }
    .page-title { font-family:'Syne',sans-serif; font-weight:800; font-size:2rem; color:#e3f2fd; margin-bottom:0.2rem; }
    .page-sub { font-family:'Space Mono',monospace; font-size:0.78rem; color:#64b5f6; margin-bottom:1.5rem; }
    .dataset-badge {
        display:inline-block; padding:0.2rem 0.8rem; border-radius:999px;
        font-family:'Space Mono',monospace; font-size:0.68rem; font-weight:700;
        margin-bottom:0.8rem;
    }
    .badge-train { background:#1a3a2a; color:#66bb6a; border:1px solid #388e3c; }
    .badge-val   { background:#1a2a3a; color:#64b5f6; border:1px solid #1565c0; }
    .badge-runs  { background:#2a1a2a; color:#ce93d8; border:1px solid #7b1fa2; }
    .badge-csv   { background:#2a2a1a; color:#ffd54f; border:1px solid #f57f17; }
    .stat-row {
        display:flex; gap:1rem; margin-bottom:1rem; flex-wrap:wrap;
    }
    .stat-chip {
        background:#0a1628; border:1px solid #1565c0; border-radius:8px;
        padding:0.4rem 0.8rem; font-family:'Space Mono',monospace; font-size:0.72rem;
    }
    .stat-chip .label { color:#64b5f6; }
    .stat-chip .val   { color:#e3f2fd; font-weight:700; }
    .stButton > button {
        background: linear-gradient(135deg, #1565c0, #0d47a1);
        color: #e3f2fd; border: 1px solid #1976d2; border-radius: 8px;
        font-family: 'Space Mono', monospace; font-size: 0.8rem;
    }
    div[data-testid="stDataFrame"] { border-radius: 10px !important; }
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


st.markdown('<div class="page-title">🗃️ Datasets CSV</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Exploration des datasets train / validation / runs & CSV intermédiaires</div>', unsafe_allow_html=True)

pipeline_root = st.session_state.get("pipeline_root", "")

if not pipeline_root:
    st.warning("⚠️ Configurez le chemin du pipeline sur la page **Accueil**.")
    st.stop()

# ── Datasets connus ──────────────────────────────────────────────────────────
KNOWN_DATASETS = [
    {
        "id": "train",
        "label": "Train Dataset",
        "badge": "badge-train",
        "path": os.path.join(pipeline_root, "data_example", "train_dataset.csv"),
        "desc": "Dataset d'entraînement pour la régression logistique.",
    },
    {
        "id": "val",
        "label": "Validation Dataset",
        "badge": "badge-val",
        "path": os.path.join(pipeline_root, "data_example", "validation_dataset.csv"),
        "desc": "Dataset de validation / prédiction.",
    },
    {
        "id": "runs",
        "label": "Runs Dataset",
        "badge": "badge-runs",
        "path": os.path.join(pipeline_root, "data_example", "Runs_dataset.csv"),
        "desc": "Métadonnées des runs / sessions IRM.",
    },
]

# Chercher aussi les CSV dans CSV_files/
csv_dir = os.path.join(pipeline_root, "data_example", "CSV_files")
extra_csvs = []
if os.path.isdir(csv_dir):
    for f in os.listdir(csv_dir):
        if f.endswith(".csv"):
            extra_csvs.append({
                "id": f"csv_{f}",
                "label": f,
                "badge": "badge-csv",
                "path": os.path.join(csv_dir, f),
                "desc": "CSV intermédiaire généré par le pipeline.",
            })

all_datasets = KNOWN_DATASETS + extra_csvs

# ── Résumé des datasets ─────────────────────────────────────────────────────
st.markdown("### 📋 Vue d'ensemble")
cols = st.columns(len(KNOWN_DATASETS))
for col, ds in zip(cols, KNOWN_DATASETS):
    with col:
        exists = os.path.isfile(ds["path"])
        if exists:
            df_tmp = pd.read_csv(ds["path"])
            rows, c_ = df_tmp.shape
            size = os.path.getsize(ds["path"]) / 1024
            status_icon = "✅"
            status_color = "#66bb6a"
        else:
            rows, c_, size = "—", "—", "—"
            status_icon = "❌"
            status_color = "#ef5350"

        st.markdown(
            f"""
            <div style="background:#0d1b2a;border:1px solid #1565c0;border-radius:12px;padding:1.2rem;">
                <span class="dataset-badge {ds['badge']}">{ds['label']}</span>
                <div style="font-size:1.6rem;font-weight:800;color:#e3f2fd;">{rows}</div>
                <div style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#64b5f6;">lignes</div>
                <div style="margin-top:0.5rem;font-family:'Space Mono',monospace;font-size:0.7rem;color:{status_color};">
                    {status_icon} {"Disponible" if exists else "Introuvable"}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ── Exploration interactive ───────────────────────────────────────────────────
st.markdown("### 🔍 Explorer un dataset")

available = [d for d in all_datasets if os.path.isfile(d["path"])]

if not available:
    st.markdown(
        """
        <div style="text-align:center;padding:2.5rem;border:2px dashed #1565c0;border-radius:14px;color:#37474f;">
            <div style="font-size:2.5rem">📭</div>
            <p style="font-family:'Space Mono',monospace;font-size:0.8rem;margin-top:0.5rem">
                Aucun dataset CSV trouvé.<br>Vérifiez le chemin du pipeline.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    sel_label = st.selectbox(
        "Sélectionner un dataset",
        [d["label"] for d in available],
        label_visibility="collapsed",
    )
    sel_ds = next(d for d in available if d["label"] == sel_label)

    df = pd.read_csv(sel_ds["path"])
    n_rows, n_cols = df.shape

    # Stats rapides
    st.markdown(
        f"""
        <div class="stat-row">
            <div class="stat-chip"><span class="label">Lignes </span><span class="val">{n_rows}</span></div>
            <div class="stat-chip"><span class="label">Colonnes </span><span class="val">{n_cols}</span></div>
            <div class="stat-chip"><span class="label">Taille </span><span class="val">{os.path.getsize(sel_ds['path'])/1024:.1f} Ko</span></div>
            <div class="stat-chip"><span class="label">Valeurs NaN </span><span class="val">{int(df.isnull().sum().sum())}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_data, tab_stats, tab_plot = st.tabs(["📄 Données", "📈 Statistiques", "📊 Visualisation"])

    with tab_data:
        col_filter, col_rows = st.columns([3, 1])
        with col_filter:
            search_col = st.text_input("🔍 Filtrer les colonnes", placeholder="Nom de colonne…")
        with col_rows:
            max_rows = st.number_input("Lignes à afficher", min_value=5, max_value=500, value=50, step=10)

        display_df = df
        if search_col:
            matching = [c for c in df.columns if search_col.lower() in c.lower()]
            display_df = df[matching] if matching else df

        st.dataframe(
            display_df.head(max_rows),
            use_container_width=True,
            height=400,
        )

        with open(sel_ds["path"], "rb") as f:
            st.download_button(
                label="⬇ Télécharger le CSV",
                data=f,
                file_name=os.path.basename(sel_ds["path"]),
                mime="text/csv",
            )

    with tab_stats:
        st.markdown("**Résumé statistique (colonnes numériques)**")
        num_df = df.select_dtypes(include="number")
        if num_df.empty:
            st.info("Aucune colonne numérique détectée.")
        else:
            st.dataframe(num_df.describe().T.style.format("{:.3f}"), use_container_width=True)

        st.markdown("**Types de colonnes**")
        dtype_df = pd.DataFrame({"Colonne": df.columns, "Type": df.dtypes.astype(str), "NaN": df.isnull().sum()})
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    with tab_plot:
        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        if not num_cols:
            st.info("Aucune colonne numérique disponible pour la visualisation.")
        else:
            plot_type = st.radio("Type de graphique", ["Histogramme", "Scatter plot", "Boxplot"], horizontal=True)

            if plot_type == "Histogramme":
                col = st.selectbox("Colonne", num_cols)
                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(figsize=(8, 4), facecolor="#0a0e1a")
                ax.set_facecolor("#0d1b2a")
                ax.hist(df[col].dropna(), bins=30, color="#1565c0", edgecolor="#64b5f6", alpha=0.85)
                ax.set_xlabel(col, color="#90caf9")
                ax.set_ylabel("Fréquence", color="#90caf9")
                ax.set_title(f"Distribution de {col}", color="#e3f2fd", fontsize=13)
                ax.tick_params(colors="#90caf9")
                for spine in ax.spines.values():
                    spine.set_edgecolor("#1565c0")
                fig.tight_layout()
                st.pyplot(fig)

            elif plot_type == "Scatter plot":
                c1, c2 = st.columns(2)
                with c1:
                    x_col = st.selectbox("Axe X", num_cols, key="sx")
                with c2:
                    y_col = st.selectbox("Axe Y", num_cols, index=min(1, len(num_cols)-1), key="sy")
                color_col = st.selectbox("Couleur (optionnel)", ["Aucun"] + cat_cols + num_cols)

                import matplotlib
                matplotlib.use("Agg")
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots(figsize=(8, 5), facecolor="#0a0e1a")
                ax.set_facecolor("#0d1b2a")
                if color_col != "Aucun" and color_col in cat_cols:
                    for val in df[color_col].unique():
                        sub = df[df[color_col] == val]
                        ax.scatter(sub[x_col], sub[y_col], label=str(val), alpha=0.75, s=30)
                    ax.legend(facecolor="#0d1b2a", labelcolor="#e3f2fd", fontsize=8)
                else:
                    ax.scatter(df[x_col], df[y_col], color="#64b5f6", alpha=0.6, s=25)
                ax.set_xlabel(x_col, color="#90caf9")
                ax.set_ylabel(y_col, color="#90caf9")
                ax.set_title(f"{x_col} vs {y_col}", color="#e3f2fd", fontsize=13)
                ax.tick_params(colors="#90caf9")
                for spine in ax.spines.values():
                    spine.set_edgecolor("#1565c0")
                fig.tight_layout()
                st.pyplot(fig)

            elif plot_type == "Boxplot":
                selected_cols = st.multiselect("Colonnes", num_cols, default=num_cols[:min(5, len(num_cols))])
                if selected_cols:
                    import matplotlib
                    matplotlib.use("Agg")
                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots(figsize=(max(6, len(selected_cols) * 1.5), 5), facecolor="#0a0e1a")
                    ax.set_facecolor("#0d1b2a")
                    bp = ax.boxplot(
                        [df[c].dropna() for c in selected_cols],
                        labels=selected_cols,
                        patch_artist=True,
                        medianprops=dict(color="#64b5f6", linewidth=2),
                    )
                    for patch in bp["boxes"]:
                        patch.set_facecolor("#1565c0")
                        patch.set_alpha(0.7)
                    ax.tick_params(colors="#90caf9", rotation=20)
                    for spine in ax.spines.values():
                        spine.set_edgecolor("#1565c0")
                    ax.set_title("Boxplots", color="#e3f2fd", fontsize=13)
                    fig.tight_layout()
                    st.pyplot(fig)
