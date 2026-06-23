import json
from pathlib import Path
import pandas as pd
from .calibrated_ros_mito_model import calibrate_to_targets, params_to_dict, score_params, simulate_constant_exposure, RosMitoParams
from ..config import BIOLOGY_DIR
from ..io_utils import load_csv, ensure_dir

def calibrate_and_save(out_dir: Path) -> RosMitoParams:
    """Run model calibration and save parameter JSON and target reports."""
    ensure_dir(out_dir)
    data_dir = BIOLOGY_DIR / "data"
    
    # Load targets
    targets = load_csv(data_dir / "validation_targets.csv")
    
    # Run calibration
    params = calibrate_to_targets(targets, n_random=5000, seed=7)
    
    # Save parameter dictionary
    with open(out_dir / "calibrated_parameters.json", "w") as f:
        json.dump(params_to_dict(params), f, indent=2)
        
    # Model vs targets comparison table
    fit_rows = []
    for _, row in targets.iterrows():
        if 'fit_anchor' not in str(row.get('calibration_role', '')):
            continue
        sim = simulate_constant_exposure(float(row['dose_rate_mGy_day']), int(row['exposure_days']), params)
        pred = float(sim[row['model_target_variable']].iloc[-1])
        fit_rows.append({
            'target_id': row['target_id'],
            'model_target_variable': row['model_target_variable'],
            'target_ratio_to_control': row['target_ratio_to_control'],
            'target_uncertainty_1sigma': row['target_uncertainty_1sigma'],
            'model_prediction': pred,
            'absolute_error': abs(pred - row['target_ratio_to_control']),
            'status': row['status'],
        })
    fit_df = pd.DataFrame(fit_rows)
    fit_df.to_csv(out_dir / "model_vs_validation_targets.csv", index=False)
    
    return params, fit_df
