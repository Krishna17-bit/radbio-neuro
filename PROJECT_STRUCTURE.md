# Project Structure Guide

This document describes the layout of the repository and the roles of individual directories and key files.

```
Radiation modelling/
├── README.md
├── PROJECT_STRUCTURE.md
├── SCIENTIFIC_LIMITATIONS.md
├── DATA_DICTIONARY.md
├── MODEL_CARD.md
├── RUN_ORDER.md
├── run_full_pipeline.py
├── run_001_physics_layer.bat
├── run_002_biology_calibration.bat
├── run_003_neural_layer.bat
├── run_full_pipeline.bat
├── run_dashboard.bat
├── run_tests.bat
│
├── 00_project_notes/
│   ├── README_DATASET.txt
│   ├── folder_structure_before_antigravity.txt
│   ├── folder_structure_after_antigravity.txt
│   └── ANTIGRAVITY_PROGRESS_LOG.md
│
├── 01_SPENVIS_RAW_DATA/         # Raw SPENVIS data files (never modified)
│   ├── 01_leo_orbit/
│   ├── 02_leo_trapped_radiation/
│   ├── 03_leo_gcr/
│   ├── 04_leo_ionizing_dose_tissue/
│   ├── 05_leo_effective_dose_trapped/
│   ├── 06_vab_orbit/
│   ├── 07_vab_trapped_radiation/
│   ├── 08_vab_gcr/
│   ├── 09_vab_ionizing_dose_tissue/
│   └── 10_vab_effective_dose_trapped/
│
├── 02_RADBIO_NEURO_001_PHYSICS_LAYER/
│   └── RADBIO_NEURO_001_NOTEBOOK_BUILD/
│       ├── data/
│       ├── figures/
│       ├── outputs/
│       ├── README_NOTEBOOK_BUILD.md
│       ├── README_FIRST_PASS.md
│       ├── RADBIO_NEURO_001_physics_to_biology_notebook.ipynb
│       └── RADBIO_NEURO_001_physics_to_biology_analysis.py
│
├── 03_RADBIO_NEURO_002_BIOLOGY_CALIBRATION/
│   ├── data/                    # Forcing tables and validation targets
│   ├── figures/                 # Calibration plots
│   ├── outputs/                 # Calibrated endpoints and timecourses
│   ├── src/                     # Source modules (calibrated_ros_mito_model.py)
│   ├── RADBIO_NEURO_002_biology_calibration_layer.ipynb
│   ├── README_RADBIO_NEURO_002.md
│   ├── requirements.txt
│   └── run_biology_calibration.py
│
├── 04_RADBIO_NEURO_003_NEURAL_LAYER/
│   ├── data/                    # Input files from biology calibration
│   ├── figures/                 # Neural raster and voltage traces
│   ├── outputs/                 # Neural simulation endpoint & timecourse summary
│   ├── src/                     # Source modules (neural_layer_model.py)
│   ├── METHOD_NEURAL_LAYER.md
│   ├── RADBIO_NEURO_003_brian2_neural_layer.ipynb
│   ├── README_RADBIO_NEURO_003.md
│   ├── requirements.txt
│   └── run_neural_layer.py
│
├── 05_PRODUCT_DASHBOARD_API/
│   ├── streamlit_app.py         # Streamlit visual UI dashboard
│   ├── api.py                   # FastAPI REST API backend
│   ├── requirements.txt         # Package dependencies for products
│   ├── run_dashboard.bat        # Windows runner for Streamlit app
│   └── run_api.bat              # Windows runner for FastAPI
│
├── 06_INTEGRATED_PIPELINE/      # Outputs, plots, and reports from full pipeline
│   ├── outputs/
│   ├── figures/
│   └── reports/
│
├── 99_ARCHIVES/                 # Zip archives of the codebase
│
├── radbio_neuro/                # Consolidated pipeline source library
│   ├── __init__.py
│   ├── config.py
│   ├── io_utils.py
│   ├── physics/
│   ├── biology/
│   ├── neural/
│   ├── reporting/
│   └── validation/
│
└── tests/                       # Unit and integration test suite
    ├── test_file_structure.py
    ├── test_physics_outputs.py
    ├── test_biology_outputs.py
    ├── test_neural_outputs.py
    └── test_no_nan_in_required_outputs.py
```
