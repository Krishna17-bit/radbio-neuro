from pathlib import Path
import pandas as pd
from ..config import RAW_DATA_DIR, PHYSICS_DIR, BIOLOGY_DIR, NEURAL_DIR

def check_required_files() -> dict:
    """Check existence of raw SPENVIS directories and key intermediate files."""
    results = {}
    
    # 1. Raw directories check
    raw_dirs = [
        "01_leo_orbit", "02_leo_trapped_radiation", "03_leo_gcr", 
        "04_leo_ionizing_dose_tissue", "05_leo_effective_dose_trapped", 
        "06_vab_orbit", "07_vab_trapped_radiation", "08_vab_gcr", 
        "09_vab_ionizing_dose_tissue", "10_vab_effective_dose_trapped"
    ]
    for d in raw_dirs:
        results[f"raw_dir_{d}"] = (RAW_DATA_DIR / d).is_dir()
        
    # 2. Key CSV files check
    phys_data = PHYSICS_DIR / "data"
    results["csv_shieldose2_dose"] = (phys_data / "shieldose2_tissue_dose_by_shielding.csv").is_file()
    results["csv_comparison"] = (phys_data / "leo_vs_vab_shieldose2_comparison.csv").is_file()
    results["csv_eff_audit"] = (phys_data / "effective_dose_output_audit.csv").is_file()
    
    bio_data = BIOLOGY_DIR / "data"
    results["csv_validation_targets"] = (bio_data / "validation_targets.csv").is_file()
    
    return results

def check_non_negative_doses(df: pd.DataFrame, dose_cols: list) -> bool:
    """Ensure all specified dose/dose-rate columns have non-negative values."""
    for col in dose_cols:
        if col in df.columns:
            if (df[col] < 0.0).any():
                return False
    return True
