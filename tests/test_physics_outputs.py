import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INT_OUT_DIR = BASE_DIR / "06_INTEGRATED_PIPELINE" / "outputs"

def test_physics_dose_non_negative():
    forcing_path = INT_OUT_DIR / "biology_ready_dose_forcing_table.csv"
    assert forcing_path.is_file(), "forcing table not found"
    
    df = pd.read_csv(forcing_path)
    dose_cols = [
        'total_dose_Gy', 'total_dose_rate_Gy_day', 'total_dose_rate_mGy_day',
        'electron_dose_rate_mGy_day', 'brems_dose_rate_mGy_day', 'trapped_proton_dose_rate_mGy_day'
    ]
    for col in dose_cols:
        assert (df[col] >= 0.0).all(), f"Dose column {col} contains negative values"

def test_scenario_counts():
    forcing_path = INT_OUT_DIR / "biology_ready_dose_forcing_table.csv"
    df = pd.read_csv(forcing_path)
    assert len(df['scenario'].unique()) == 2, "Should contain LEO and VAB scenarios"
