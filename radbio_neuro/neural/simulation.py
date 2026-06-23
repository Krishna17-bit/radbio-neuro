import numpy as np
import pandas as pd
from .neural_layer_model import NeuralSimConfig, run_lif_network, summarize_result

def run_neural_pipeline(selected_biology: pd.DataFrame, daily_biology: pd.DataFrame):
    """Run endpoint, timecourse, and control neural population simulations."""
    
    cfg_endpoint = NeuralSimConfig(n_neurons=80, sim_ms=2000.0, dt_ms=0.1, seed=202603)
    
    # 1. Endpoint simulations
    endpoint_rows = []
    example_results = {}
    for _, row in selected_biology.iterrows():
        # Vary seed deterministically by scenario/shield to avoid identical noise traces
        seed_val = int(1000 + row['shield_mm_Al'] * 10 + (0 if row['scenario']=='LEO_ISS_like' else 500))
        cfg = NeuralSimConfig(**{**cfg_endpoint.__dict__, 'seed': seed_val})
        result = run_lif_network(row, cfg)
        endpoint_rows.append(summarize_result(row, result))
        if float(row['shield_mm_Al']) == 10.0:
            example_results[row['scenario']] = result
            
    endpoint_df = pd.DataFrame(endpoint_rows)
    
    # 2. Timecourse simulations for 10 mm Al in LEO and VAB
    time_rows = []
    for scenario in ['LEO_ISS_like', 'VAB_RBSP_like']:
        # Filter for 10 mm
        sub = daily_biology[(daily_biology['scenario'] == scenario) & (daily_biology['shield_mm_Al'].round(6) == 10.0)].copy()
        if sub.empty:
            continue
        # Sample every 15 days plus day 180
        sample_days = sorted(set(list(range(0, 181, 15)) + [180]))
        for day in sample_days:
            # Find closest day index
            closest_idx = (sub['day'] - day).abs().argmin()
            row = sub.iloc[closest_idx].copy()
            # Map daily columns to endpoint names
            row['ros_norm_day_end'] = row['ros_norm']
            row['mito_integrity_day_end'] = row['mito_integrity']
            row['atp_proxy_day_end'] = row['atp_proxy']
            row['fast_excitability_delta_day_end'] = row['fast_excitability_delta']
            row['slow_mito_atp_suppression_day_end'] = row['slow_mito_atp_suppression']
            row['calibration_domain_flag'] = 'timecourse_from_biology_layer'
            row['model_status'] = 'neural_scaffold_timecourse'
            
            cfg = NeuralSimConfig(n_neurons=60, sim_ms=1000.0, dt_ms=0.1, seed=int(3000 + day + (0 if scenario=='LEO_ISS_like' else 500)))
            result = run_lif_network(row, cfg)
            time_rows.append(summarize_result(row, result))
            
    timecourse_df = pd.DataFrame(time_rows)
    
    # 3. Control simulation (Healthy, no radiation)
    control_row = pd.Series({
        'scenario': 'Healthy_control_no_radiation',
        'shield_mm_Al': np.nan,
        'day': 0,
        'dose_rate_mGy_day': 0.0,
        'ros_norm_day_end': 0.0,
        'mito_integrity_day_end': 1.0,
        'atp_proxy_day_end': 1.0,
        'fast_excitability_delta_day_end': 0.0,
        'slow_mito_atp_suppression_day_end': 0.0,
        'calibration_domain_flag': 'control',
        'model_status': 'simulation_control'
    })
    
    control_res = run_lif_network(control_row, NeuralSimConfig(n_neurons=80, sim_ms=2000, dt_ms=0.1, seed=4040))
    example_results['Healthy_control_no_radiation'] = control_res
    control_df = pd.DataFrame([summarize_result(control_row, control_res)])
    
    return endpoint_df, timecourse_df, control_df, example_results
