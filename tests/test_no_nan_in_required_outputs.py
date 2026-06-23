import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INT_OUT_DIR = BASE_DIR / "06_INTEGRATED_PIPELINE" / "outputs"

def test_no_nan_in_forcing():
    df = pd.read_csv(INT_OUT_DIR / "biology_ready_dose_forcing_table.csv")
    required = ['total_dose_Gy', 'total_dose_rate_mGy_day', 'ros_forcing_index_log01']
    for col in required:
        assert not df[col].isna().any(), f"Unexpected NaN in forcing column {col}"

def test_no_nan_in_biology():
    df = pd.read_csv(INT_OUT_DIR / "biology_calibrated_endpoint_predictions.csv")
    required = ['ros_norm_day_end', 'mito_integrity_day_end', 'atp_proxy_day_end', 'excitability_ratio_day_end']
    for col in required:
        assert not df[col].isna().any(), f"Unexpected NaN in biology column {col}"

def test_no_nan_in_neural():
    df = pd.read_csv(INT_OUT_DIR / "neural_endpoint_simulation_summary.csv")
    required = ['mean_firing_rate_hz', 'drive_eff_mV', 'tau_eff_ms', 'v_threshold_eff_mV']
    for col in required:
        assert not df[col].isna().any(), f"Unexpected NaN in neural column {col}"

def test_effective_dose_flagged():
    df = pd.read_csv(BASE_DIR / "02_RADBIO_NEURO_001_PHYSICS_LAYER" / "RADBIO_NEURO_001_NOTEBOOK_BUILD" / "data" / "effective_dose_output_audit.csv")
    # Verify that the audit lists effective dose as unusable due to NaNs
    usable = df['usable_numeric_effective_dose'].fillna(False).astype(bool).any()
    assert not usable, "Effective dose MC outputs are expected to contain NaNs and be marked unusable in this dataset"

def test_no_nan_in_scenario_interpretation_flags():
    df = pd.read_csv(INT_OUT_DIR / "scenario_interpretation_flags.csv")
    required = ['scenario', 'shield_mm_Al', 'dose_rate_mGy_day', 'calibration_domain_flag', 'interpretation_class', 'recommended_user_message']
    for col in required:
        assert not df[col].isna().any(), f"Unexpected NaN in scenario interpretation flags column {col}"

