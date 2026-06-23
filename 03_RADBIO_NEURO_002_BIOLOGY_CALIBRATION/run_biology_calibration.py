
from pathlib import Path
import sys, json
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
from calibrated_ros_mito_model import calibrate_to_targets, score_params, simulate_constant_exposure, predict_for_forcing_table, params_to_dict

DATA = ROOT / 'data'
OUT = ROOT / 'outputs'
FIG = ROOT / 'figures'
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

forcing = pd.read_csv(DATA / 'biology_ready_dose_forcing_table.csv')
targets = pd.read_csv(DATA / 'validation_targets.csv')
params = calibrate_to_targets(targets, n_random=5000, seed=7)
with open(OUT / 'calibrated_parameters.json', 'w') as f:
    json.dump(params_to_dict(params), f, indent=2)

# Model vs targets
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
fit_df.to_csv(OUT / 'model_vs_validation_targets.csv', index=False)

# Run model on SPENVIS forcing table
predictions, timecourses = predict_for_forcing_table(forcing, params)
predictions.to_csv(OUT / 'biology_calibrated_endpoint_predictions.csv', index=False)
timecourses.to_csv(OUT / 'biology_calibrated_daily_timecourses_all_scenarios.csv', index=False)

# Selected human-readable summary
selected = predictions[predictions['shield_mm_Al'].isin([1,2,5,10,20])].copy()
selected.to_csv(OUT / 'selected_shielding_biology_summary.csv', index=False)

# Plots: one figure per chart; no explicit colors/styles.
ax = fit_df.plot(x='target_id', y=['target_ratio_to_control','model_prediction'], kind='bar', figsize=(10,5))
ax.set_ylabel('Ratio to control')
ax.set_xlabel('Validation target')
ax.set_title('Model vs current validation targets')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig(FIG / 'model_vs_validation_targets.png', dpi=200)
plt.close()

sel = predictions[predictions['shield_mm_Al'].isin([1,2,5,10,20])]
for metric, ylabel, fname in [
    ('mito_integrity_day_end','Mitochondrial integrity at day 180','mito_integrity_vs_shielding.png'),
    ('excitability_ratio_day_end','Excitability ratio at day 180','excitability_vs_shielding.png'),
    ('ltp_proxy_day_end','LTP proxy at day 180','ltp_proxy_vs_shielding.png'),
]:
    pivot = sel.pivot(index='shield_mm_Al', columns='scenario', values=metric).sort_index()
    ax = pivot.plot(marker='o', figsize=(8,5))
    ax.set_xscale('log')
    ax.set_xlabel('Al shielding depth (mm)')
    ax.set_ylabel(ylabel)
    ax.set_title(ylabel + ' vs shielding')
    plt.tight_layout()
    plt.savefig(FIG / fname, dpi=200)
    plt.close()

# Timecourses for 10 mm Al
subset = timecourses[timecourses['shield_mm_Al'].round(6).eq(10.0)]
for metric, ylabel, fname in [
    ('ros_norm','ROS state','timecourse_ros_10mm.png'),
    ('mito_integrity','Mitochondrial integrity','timecourse_mito_10mm.png'),
    ('excitability_ratio','Excitability ratio','timecourse_excitability_10mm.png'),
]:
    fig, ax = plt.subplots(figsize=(8,5))
    for scenario, grp in subset.groupby('scenario'):
        ax.plot(grp['day'], grp[metric], label=scenario)
    ax.set_xlabel('Mission day')
    ax.set_ylabel(ylabel)
    ax.set_title(ylabel + ' timecourse at 10 mm Al')
    ax.legend()
    plt.tight_layout()
    plt.savefig(FIG / fname, dpi=200)
    plt.close()

print('RADBIO_NEURO_002 complete')
print('Parameter score:', score_params(params, targets))
print(fit_df)
