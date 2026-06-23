import pandas as pd
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
INT_OUT_DIR = BASE_DIR / "06_INTEGRATED_PIPELINE" / "outputs"

def test_biology_outputs_and_flags():
    pred_path = INT_OUT_DIR / "biology_calibrated_endpoint_predictions.csv"
    assert pred_path.is_file()
    
    df = pd.read_csv(pred_path)
    assert 'calibration_domain_flag' in df.columns
    assert 'ros_norm_day_end' in df.columns
    assert 'mito_integrity_day_end' in df.columns
    
    # ROS should be non-negative; Mito integrity should be bounded in [0, 1]
    assert (df['ros_norm_day_end'] >= 0.0).all()
    assert (df['mito_integrity_day_end'] >= 0.0).all() and (df['mito_integrity_day_end'] <= 1.0).all()

def test_parameters_exist():
    param_path = INT_OUT_DIR / "calibrated_parameters.json"
    assert param_path.is_file()
    
    with open(param_path, "r") as f:
        p = json.load(f)
    assert "k_ros_prod" in p
    assert "k_mito_damage" in p
