import pandas as pd
from ..config import PHYSICS_DIR
from ..io_utils import load_csv

def load_shieldose2_data():
    """Load parsed SHIELDOSE-2 and comparison tables."""
    data_dir = PHYSICS_DIR / "data"
    dose = load_csv(data_dir / "shieldose2_tissue_dose_by_shielding.csv")
    comparison = load_csv(data_dir / "leo_vs_vab_shieldose2_comparison.csv")
    selected = load_csv(data_dir / "selected_shielding_depth_summary.csv")
    eff_audit = load_csv(data_dir / "effective_dose_output_audit.csv")
    return dose, comparison, selected, eff_audit

def audit_effective_dose(eff_audit: pd.DataFrame) -> bool:
    """Audit effective dose Monte Carlo table. Returns True if any usable numeric dose is found."""
    return eff_audit['usable_numeric_effective_dose'].fillna(False).astype(bool).any()
