#!/usr/bin/env python
"""
Main integrated pipeline runner for radbio_neuro.
Runs physics parsing, biological calibration, neural network LIF simulation, and reports creation.
"""
import sys
from pathlib import Path
import pandas as pd

# Add root folder to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from radbio_neuro.config import INT_OUT_DIR, INT_FIG_DIR, INT_REP_DIR
from radbio_neuro.io_utils import ensure_dir, save_csv
from radbio_neuro.physics import load_shieldose2_data, audit_effective_dose, process_dose_forcing, plot_dose_curves
from radbio_neuro.biology import calibrate_and_save, predict_for_forcing_table, plot_biology_results
from radbio_neuro.neural import run_neural_pipeline, plot_neural_results
from radbio_neuro.reporting import build_reports

def run_pipeline():
    print("=" * 60)
    print("STARTING RADBIO_NEURO INTEGRATED PIPELINE RUNNER")
    print("=" * 60)

    # Ensure output folders exist
    ensure_dir(INT_OUT_DIR)
    ensure_dir(INT_FIG_DIR)
    ensure_dir(INT_REP_DIR)

    # 1. Physics Layer
    print("\n[1/5] Executing Physics Layer...")
    dose, comparison, selected, eff_audit = load_shieldose2_data()
    
    # Audit effective dose
    any_usable = audit_effective_dose(eff_audit)
    print(f" - Audit effective dose. Any usable Sievert values? {any_usable}")
    if not any_usable:
        print(" - MC effective dose contains NaNs and is unusable. Falling back to SHIELDOSE-2 tissue absorbed dose.")
    
    # Process forcing table
    forcing_df = process_dose_forcing(dose)
    save_csv(forcing_df, INT_OUT_DIR / "biology_ready_dose_forcing_table.csv")
    print(f" - Saved biology-ready dose forcing table to {INT_OUT_DIR / 'biology_ready_dose_forcing_table.csv'}")

    # Generate physics plots
    plot_dose_curves(dose, forcing_df, INT_FIG_DIR)
    print(f" - Saved physics plots to {INT_FIG_DIR}")

    # 2. Biology Layer
    print("\n[2/5] Executing Biology Calibration Layer...")
    # Run calibration
    params, fit_df = calibrate_and_save(INT_OUT_DIR)
    print(f" - Calibrated params: {params}")
    
    # Predict endpoints and timecourses on full forcing table
    predictions, timecourses = predict_for_forcing_table(forcing_df, params)
    
    save_csv(predictions, INT_OUT_DIR / "biology_calibrated_endpoint_predictions.csv")
    save_csv(timecourses, INT_OUT_DIR / "biology_calibrated_daily_timecourses_all_scenarios.csv")
    
    # Select subset summary
    bio_selected = predictions[predictions['shield_mm_Al'].isin([1, 2, 5, 10, 20])].copy()
    save_csv(bio_selected, INT_OUT_DIR / "selected_shielding_biology_summary.csv")
    
    print(f" - Saved biology calibrated endpoint predictions to {INT_OUT_DIR}")
    
    # Generate biology plots
    plot_biology_results(fit_df, predictions, timecourses, INT_FIG_DIR)
    print(f" - Saved biology plots to {INT_FIG_DIR}")

    # 3. Neural Layer
    print("\n[3/5] Executing Neural Simulation Layer...")
    endpoint_df, timecourse_df, control_df, example_results = run_neural_pipeline(bio_selected, timecourses)
    
    save_csv(endpoint_df, INT_OUT_DIR / "neural_endpoint_simulation_summary.csv")
    save_csv(timecourse_df, INT_OUT_DIR / "neural_timecourse_10mm_summary.csv")
    save_csv(control_df, INT_OUT_DIR / "healthy_control_neural_summary.csv")
    
    print(f" - Saved neural simulation outputs to {INT_OUT_DIR}")
    
    # Generate neural plots
    plot_neural_results(endpoint_df, timecourse_df, example_results, INT_FIG_DIR)
    print(f" - Saved neural network plots (rasters & voltage traces) to {INT_FIG_DIR}")

    # 4. Save pipeline status flags
    print("\n[4/5] Saving scientific flags & status logs...")
    status = pd.DataFrame([
        {'layer': 'RADBIO_NEURO_001', 'status': 'SPENVIS absorbed tissue dose available; effective dose MC NaN/audit only'},
        {'layer': 'RADBIO_NEURO_002', 'status': 'Biology calibration scaffold available; anchored to chronic low-dose neural target; many cases extrapolative'},
        {'layer': 'RADBIO_NEURO_003', 'status': 'Neural simulation scaffold built; not yet validated against electrophysiology/raster data'},
    ])
    save_csv(status, INT_OUT_DIR / "pipeline_status_flags.csv")
    print(f" - Saved status flags to {INT_OUT_DIR / 'pipeline_status_flags.csv'}")

    # Generate and save scenario interpretation flags
    interpretation_rows = []
    for _, r in predictions.iterrows():
        dr = float(r['dose_rate_mGy_day'])
        flag = r['calibration_domain_flag']
        if 0.1 <= dr <= 10.0:
            interp_class = 'calibration_near_domain'
            msg = "Dose rate is within the primary biological validation domain of 0.1 to 10.0 mGy/day. Projections are anchored on chronic low-dose mouse neural data."
        elif dr < 0.1:
            interp_class = 'moderate_extrapolation'
            msg = "Dose rate is lower than the primary validation anchors. Relies on low-dose model extrapolation."
        elif 10.0 < dr <= 100.0:
            interp_class = 'moderate_extrapolation'
            msg = "Dose rate moderately exceeds primary validation anchors. Relies on high-dose model extrapolation."
        else:
            interp_class = 'severe_extrapolation_stress_test'
            msg = "Dose rate is extremely high, representing severe extrapolation. Projections constitute a stress-test only; biological cells are not validated under these extreme rates."
            
        interpretation_rows.append({
            'scenario': r['scenario'],
            'shield_mm_Al': r['shield_mm_Al'],
            'dose_rate_mGy_day': dr,
            'calibration_domain_flag': flag,
            'interpretation_class': interp_class,
            'recommended_user_message': msg
        })
    interp_df = pd.DataFrame(interpretation_rows)
    save_csv(interp_df, INT_OUT_DIR / "scenario_interpretation_flags.csv")
    print(f" - Saved scenario interpretation flags to {INT_OUT_DIR / 'scenario_interpretation_flags.csv'}")

    # 5. Reporting Layer
    print("\n[5/5] Generating Integrated Reports...")
    build_reports(forcing_df, predictions, endpoint_df, INT_REP_DIR)
    
    print("\n" + "=" * 60)
    print("INTEGRATED PIPELINE RUN COMPLETED SUCCESSFULLY.")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
