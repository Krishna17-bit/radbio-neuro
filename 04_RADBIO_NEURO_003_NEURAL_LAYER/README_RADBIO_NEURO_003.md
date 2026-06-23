# RADBIO_NEURO_003 — Neural Simulation Layer

This package builds the first neural simulation layer downstream of RADBIO_NEURO_001 and RADBIO_NEURO_002.

## Purpose

RADBIO_NEURO_003 takes the calibrated biology-state outputs from RADBIO_NEURO_002 and maps them into a small conductance-aware leaky integrate-and-fire network. The model explicitly separates:

- **Fast term:** acute ROS/channel oxidation effects that can transiently increase excitability.
- **Slow term:** mitochondrial injury and ATP depletion that suppress baseline drive, shorten integration time, increase effective threshold, and can reduce firing.

This replaces the earlier toy assumption that ROS directly and monotonically suppresses firing.

## Main files

- `RADBIO_NEURO_003_brian2_neural_layer.ipynb` — notebook-style workflow.
- `run_neural_layer.py` — script to regenerate outputs and figures.
- `src/neural_layer_model.py` — reusable neural model functions.
- `data/` — copied RADBIO_NEURO_002 biology inputs.
- `outputs/neural_endpoint_simulation_summary.csv` — endpoint firing-rate summary.
- `outputs/neural_timecourse_10mm_summary.csv` — neural timecourse at 10 mm Al.
- `figures/` — firing, raster, and voltage plots.

## Scientific status

This is a **neural simulation scaffold**, not a validated clinical or astronaut-health prediction. It is suitable for model development and product architecture, but it still needs:

1. stronger numeric calibration of ROS/mitochondria parameters,
2. dose-equivalent or LET-weighted inputs instead of absorbed tissue dose only,
3. experimental electrophysiology targets for firing-rate, excitability, LTP, and synaptic plasticity,
4. a real Brian2/NEURON implementation for publication-quality conductance-channel simulations.

## How to run

```bash
pip install -r requirements.txt
python run_neural_layer.py
```

## Current interpretation

The package shows how shielded SPENVIS dose can be translated into downstream neural simulation states. LEO-like scenarios with thicker shielding retain more firing activity, while the Van Allen/RBSP-like case lies far outside the current validation domain and collapses the scaffold excitability output. Those Van Allen outputs should be treated as **out-of-domain stress tests**, not validated biology claims.
