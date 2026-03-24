# 🧠 MRI Asymmetry Analysis — Interface Utilisateur

Interface Streamlit pour le pipeline [MRI_Asymmetry_Analysis_Pipeline](https://github.com/CoLucas22/MRI_Asymmetry_Analysis_Pipeline).

---

## ✨ Fonctionnalités

| Module              | Description                                                                                                                                  |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 📂 **Upload DICOM** | Chargement de fichiers `.DCM`, prévisualisation des coupes IRM, exploration du répertoire local                                              |
| ⚙️ **Pipeline**     | Lancement de `preprocess.py`, `extract_features.py`, `visualize.py` et `classification_task.R` via subprocess, console de logs en temps réel |
| 📊 **Résultats**    | Galerie des figures générées dans `results/figures/`, téléchargement, vue détaillée                                                          |
| 🗃️ **Datasets CSV** | Exploration interactive des datasets train/validation/runs, statistiques, histogrammes, scatter plots, boxplots                              |

---

## 🚀 Installation

```bash
# 1. Cloner ce repo UI
git clone https://github.com/<CoLucas22/MRI_Asymmetry_UI.git
cd MRI_Asymmetry_UI

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
streamlit run app.py
```

---

## ⚙️ Configuration

Au premier lancement, rendez-vous sur la page **Accueil** et renseignez le chemin absolu vers votre clone de `MRI_Asymmetry_Analysis_Pipeline` :

```
/home/user/MRI_Asymmetry_Analysis_Pipeline
```

Ce chemin est sauvegardé en session et utilisé par tous les modules pour lancer les scripts et lire les données.

---

## 🗂️ Structure du repo UI

```
MRI_Asymmetry_UI/
├── app.py                  # Page d'accueil & configuration
├── pages/
│   ├── 1_upload.py         # Upload & prévisualisation DICOM
│   ├── 2_pipeline.py       # Lancement des scripts
│   ├── 3_results.py        # Résultats & figures
│   └── 4_datasets.py       # Tableau de bord CSV
├── requirements.txt
└── README.md
```

---

## 📦 Dépendances

- `streamlit` — framework UI
- `pandas` — manipulation des CSV
- `matplotlib` — visualisations
- `pydicom` — lecture des fichiers DICOM
- `numpy` — traitement des arrays

> **Note R** : Pour lancer `classification_task.R`, `Rscript` doit être disponible dans votre `PATH`.

---

## 🔗 Repo pipeline associé

[CoLucas22/MRI_Asymmetry_Analysis_Pipeline](https://github.com/CoLucas22/MRI_Asymmetry_Analysis_Pipeline)

---

## 👤 Auteur pipeline

Développé par **Corentin Lucas**, Doctorant INRIA Rennes – Équipe Dyliss.  
Interface UI développée en complément du pipeline d'analyse d'asymétrie IRM.
