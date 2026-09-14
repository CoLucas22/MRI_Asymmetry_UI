# MRI Asymmetry Analysis — interface

Interface Streamlit pour le pipeline
[MRI_Asymmetry_Analysis_Pipeline](https://github.com/CoLucas22/MRI_Asymmetry_Analysis_Pipeline) :
analyse d'asymétrie sur IRM axiales dans le cadre de la maladie de Crohn.

## Modules

- **Upload DICOM** — chargement de fichiers `.DCM`, lecture des métadonnées, aperçu des coupes,
  parcours du répertoire `data_example/MRIs` du dépôt pipeline.
- **Exécution du pipeline** — lancement de `preprocess.py`, `extract_features.py`, `visualize.py`
  et `classification_task.R` via `subprocess`, avec journal des sorties standard et d'erreur.
- **Résultats** — galerie des figures de `results/figures/`, filtre par nom, téléchargement.
- **Datasets CSV** — exploration des jeux d'entraînement, de validation et des CSV intermédiaires :
  aperçu tabulaire, résumé statistique, histogrammes, nuages de points, boîtes à moustaches.

## Installation

```bash
git clone https://github.com/CoLucas22/MRI_Asymmetry_UI.git
cd MRI_Asymmetry_UI

python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py
```

L'exécution de `classification_task.R` suppose que `Rscript` est accessible depuis le `PATH`.
Un environnement conda incluant R évite d'avoir à gérer les deux installations séparément.

## Configuration

Au premier lancement, renseignez sur la page d'accueil le chemin absolu vers votre clone du
pipeline :

```
/home/user/MRI_Asymmetry_Analysis_Pipeline
```

Le chemin est enregistré dans `config.json`, à la racine de ce dépôt, et réutilisé aux lancements
suivants. Si le pipeline est cloné dans ce répertoire, il est détecté automatiquement. Ajoutez
`config.json` à votre `.gitignore`, le chemin étant propre à chaque poste.

## Arborescence

```
MRI_Asymmetry_UI/
├── app.py                        # accueil et configuration du chemin du pipeline
├── ui.py                         # en-tête, barre latérale, résolution du chemin
├── pages/
│   ├── 1_Upload_DICOM.py
│   ├── 2_Pipeline.py
│   ├── 3_Resultats.py
│   └── 4_Datasets_CSV.py
├── .streamlit/config.toml        # thème de l'application
├── requirements.txt
└── README.md
```

## Dépendances

`streamlit`, `pandas`, `numpy`, `matplotlib`, `pydicom`. Les scripts R sont appelés par
`subprocess`, sans passer par `rpy2`.

## Auteur

Corentin Lucas, doctorant, équipe BioGraphs, IRISA / Inria Rennes.
Interface développée en complément du pipeline d'analyse d'asymétrie IRM.
