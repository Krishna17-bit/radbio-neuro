# RADBIO_NEURO_001 Notebook Build

This package contains the first executable physics-to-biology analysis notebook built from the parsed SPENVIS CSV outputs.

## Main file

- `RADBIO_NEURO_001_physics_to_biology_notebook.ipynb`

## What it does

- Loads parsed SPENVIS SHIELDOSE-2 tissue absorbed dose tables.
- Audits effective-dose Monte Carlo output and flags it as unusable because it contains NaN values.
- Compares ISS-like LEO vs Van Allen/RBSP-like orbit.
- Converts 180-day absorbed dose to Gy/day and mGy/day.
- Builds a biology-ready forcing table.
- Runs a provisional ROS/mitochondria input-layer simulation.
- Exports figures and CSV outputs.

## Important scientific limitation

The ROS/mitochondria layer is a prototype scaffold, not a validated biological model. It is included so the product pipeline has a working input-output structure. Final biological interpretation requires dose-equivalent/LET information and calibration against real experimental dose-response data.

## Outputs

See:

- `outputs/biology_ready_dose_forcing_table.csv`
- `outputs/selected_shielding_dose_rate_summary.csv`
- `outputs/prototype_ros_mito_daily_timecourses.csv`
- `outputs/prototype_ros_mito_endpoints_selected_shielding.csv`
- `figures/*.png`
