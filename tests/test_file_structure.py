import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def test_raw_folders_exist():
    raw_dir = BASE_DIR / "01_SPENVIS_RAW_DATA"
    assert raw_dir.is_dir(), "01_SPENVIS_RAW_DATA directory missing"
    
    subfolders = [
        "01_leo_orbit", "02_leo_trapped_radiation", "03_leo_gcr",
        "04_leo_ionizing_dose_tissue", "05_leo_effective_dose_trapped",
        "06_vab_orbit", "07_vab_trapped_radiation", "08_vab_gcr",
        "09_vab_ionizing_dose_tissue", "10_vab_effective_dose_trapped"
    ]
    for folder in subfolders:
        assert (raw_dir / folder).is_dir(), f"Raw subfolder {folder} is missing"

def test_key_csvs_exist():
    # Intermediate files
    assert (BASE_DIR / "02_RADBIO_NEURO_001_PHYSICS_LAYER" / "RADBIO_NEURO_001_NOTEBOOK_BUILD" / "data" / "shieldose2_tissue_dose_by_shielding.csv").is_file()
    assert (BASE_DIR / "03_RADBIO_NEURO_002_BIOLOGY_CALIBRATION" / "data" / "validation_targets.csv").is_file()
    
    # Integrated output files
    out_dir = BASE_DIR / "06_INTEGRATED_PIPELINE" / "outputs"
    assert (out_dir / "biology_ready_dose_forcing_table.csv").is_file()
    assert (out_dir / "biology_calibrated_endpoint_predictions.csv").is_file()
    assert (out_dir / "neural_endpoint_simulation_summary.csv").is_file()
    assert (out_dir / "scenario_interpretation_flags.csv").is_file()
