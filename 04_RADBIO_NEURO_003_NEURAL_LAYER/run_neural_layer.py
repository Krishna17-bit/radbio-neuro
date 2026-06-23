
from __future__ import annotations
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.neural_layer_model import NeuralSimConfig, run_lif_network, summarize_result

BASE = Path(__file__).resolve().parent
DATA = BASE / 'data'
OUT = BASE / 'outputs'
FIG = BASE / 'figures'
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

selected = pd.read_csv(DATA / 'selected_shielding_biology_summary.csv')
daily = pd.read_csv(DATA / 'biology_calibrated_daily_timecourses_all_scenarios.csv')

cfg_endpoint = NeuralSimConfig(n_neurons=80, sim_ms=2000.0, dt_ms=0.1, seed=202603)

# Endpoint network simulations for selected shielding depths.
endpoint_rows = []
example_results = {}
for _, row in selected.iterrows():
    # Vary seed deterministically by scenario/shield to avoid identical noise traces.
    cfg = NeuralSimConfig(**{**cfg_endpoint.__dict__, 'seed': int(1000 + row['shield_mm_Al'] * 10 + (0 if row['scenario']=='LEO_ISS_like' else 500))})
    result = run_lif_network(row, cfg)
    endpoint_rows.append(summarize_result(row, result))
    if float(row['shield_mm_Al']) == 10.0:
        example_results[row['scenario']] = result

endpoint = pd.DataFrame(endpoint_rows)
endpoint.to_csv(OUT / 'neural_endpoint_simulation_summary.csv', index=False)

# Timecourse neural simulation at selected day intervals for 10 mm Al in each scenario.
time_rows = []
for scenario in ['LEO_ISS_like', 'VAB_RBSP_like']:
    sub = daily[(daily['scenario'] == scenario) & (daily['shield_mm_Al'] == 10.0)].copy()
    # Sample every 15 days plus final day.
    sample_days = sorted(set(list(range(0, 181, 15)) + [180]))
    for day in sample_days:
        row = sub.iloc[(sub['day'] - day).abs().argmin()].copy()
        # Rename daily columns into endpoint-compatible names.
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

timecourse = pd.DataFrame(time_rows)
timecourse.to_csv(OUT / 'neural_timecourse_10mm_summary.csv', index=False)

# Compact control simulation: biology state with no injury.
control_row = pd.Series({
    'scenario': 'Healthy_control_no_radiation',
    'shield_mm_Al': np.nan,
    'day': 0,
    'dose_rate_mGy_day': 0,
    'ros_norm_day_end': 0,
    'mito_integrity_day_end': 1,
    'atp_proxy_day_end': 1,
    'fast_excitability_delta_day_end': 0,
    'slow_mito_atp_suppression_day_end': 0,
    'calibration_domain_flag': 'control',
    'model_status': 'simulation_control'
})
control = run_lif_network(control_row, NeuralSimConfig(n_neurons=80, sim_ms=2000, dt_ms=0.1, seed=4040))
pd.DataFrame([summarize_result(control_row, control)]).to_csv(OUT / 'healthy_control_neural_summary.csv', index=False)

# Figures
plt.figure(figsize=(8, 5))
for scenario, group in endpoint.groupby('scenario'):
    g = group.sort_values('shield_mm_Al')
    plt.plot(g['shield_mm_Al'], g['mean_firing_rate_hz'], marker='o', label=scenario)
plt.xscale('log')
plt.xlabel('Al shielding thickness (mm)')
plt.ylabel('Mean firing rate (Hz)')
plt.title('Endpoint neural firing rate after 180 days')
plt.legend()
plt.grid(True, which='both', alpha=0.3)
plt.tight_layout()
plt.savefig(FIG / 'endpoint_firing_rate_vs_shielding.png', dpi=200)
plt.close()

plt.figure(figsize=(8, 5))
for scenario, group in timecourse.groupby('scenario'):
    g = group.sort_values('day')
    plt.plot(g['day'], g['mean_firing_rate_hz'], marker='o', label=scenario)
plt.xlabel('Mission day')
plt.ylabel('Mean firing rate (Hz)')
plt.title('Neural simulation timecourse at 10 mm Al')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIG / 'timecourse_firing_rate_10mm.png', dpi=200)
plt.close()

plt.figure(figsize=(8, 5))
for scenario, group in endpoint.groupby('scenario'):
    g = group.sort_values('shield_mm_Al')
    plt.plot(g['shield_mm_Al'], g['drive_eff_mV'], marker='o', label=f'{scenario} drive')
plt.xscale('log')
plt.xlabel('Al shielding thickness (mm)')
plt.ylabel('Effective drive term (mV equivalent)')
plt.title('Bioenergetic drive entering the neural model')
plt.legend()
plt.grid(True, which='both', alpha=0.3)
plt.tight_layout()
plt.savefig(FIG / 'effective_drive_vs_shielding.png', dpi=200)
plt.close()

# Raster examples for 10 mm and healthy control.
def plot_raster(result, name, title):
    plt.figure(figsize=(8, 4))
    st = result['spike_times_ms']
    sn = result['spike_neurons']
    if len(st) > 0:
        plt.scatter(st, sn, s=2)
    plt.xlabel('Time (ms)')
    plt.ylabel('Neuron index')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(FIG / name, dpi=200)
    plt.close()

plot_raster(control, 'raster_healthy_control.png', 'Raster: healthy control')
for scenario, result in example_results.items():
    plot_raster(result, f'raster_{scenario}_10mm.png', f'Raster: {scenario}, 10 mm Al, day 180')

# Voltage trace examples.
def plot_voltage(result, name, title):
    plt.figure(figsize=(8,4))
    t = result['trace_time_ms']
    traces = result['voltage_traces_mV']
    for i in range(traces.shape[1]):
        plt.plot(t, traces[:, i], linewidth=0.8, alpha=0.8)
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane potential (mV)')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(FIG / name, dpi=200)
    plt.close()
plot_voltage(control, 'voltage_healthy_control.png', 'Voltage traces: healthy control')
for scenario, result in example_results.items():
    plot_voltage(result, f'voltage_{scenario}_10mm.png', f'Voltage traces: {scenario}, 10 mm Al, day 180')

# README-style status CSV
status = pd.DataFrame([
    {'layer': 'RADBIO_NEURO_001', 'status': 'SPENVIS absorbed tissue dose available; effective dose MC NaN/audit only'},
    {'layer': 'RADBIO_NEURO_002', 'status': 'Biology calibration scaffold available; anchored to chronic low-dose neural target; many cases extrapolative'},
    {'layer': 'RADBIO_NEURO_003', 'status': 'Neural simulation scaffold built; not yet validated against electrophysiology/raster data'},
])
status.to_csv(OUT / 'pipeline_status_flags.csv', index=False)

print('RADBIO_NEURO_003 neural layer completed.')
print(endpoint[['scenario','shield_mm_Al','mean_firing_rate_hz','atp_proxy','calibration_domain_flag']])
