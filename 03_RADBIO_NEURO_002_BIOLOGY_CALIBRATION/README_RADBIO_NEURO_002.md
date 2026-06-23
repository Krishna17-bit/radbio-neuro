# RADBIO_NEURO_002 — Biology Calibration Layer

This package builds the second layer after `RADBIO_NEURO_001`: a calibration scaffold that maps SPENVIS-derived absorbed tissue dose rates into separated fast and slow biology states.

## What this package adds

- `data/validation_targets.csv` — initial validation targets from radiation-biology and neurobiology literature.
- `data/parameter_provenance.csv` — parameter/source/provenance table.
- `src/calibrated_ros_mito_model.py` — reusable Python model separating acute ROS/channel effects from chronic mitochondrial/ATP failure.
- `RADBIO_NEURO_002_biology_calibration_layer.ipynb` — runnable notebook.
- `run_biology_calibration.py` — script version of the notebook workflow.
- `outputs/` — calibration outputs and biology endpoint predictions.
- `figures/` — model-vs-target and scenario comparison plots.

## Model logic

The old prototype structure was:

```text
dose_rate -> ROS -> mitochondrial damage -> risk proxy
```

This package changes it to:

```text
absorbed tissue dose-rate / cumulative dose
-> acute ROS production and clearance
-> chronic mitochondrial injury and repair
-> ATP / bioenergetic stress proxy
-> fast excitability term + slow suppression term
```

The key scientific correction is that ROS is not forced to always suppress firing. The model has:

1. **Fast term** — acute ROS/channel oxidation can increase excitability in some contexts.
2. **Slow term** — chronic mitochondrial/ATP failure suppresses excitability and synaptic plasticity.

## Current calibration status

This is a **calibrated scaffold**, not a final validated radiobiology model. The first two neural targets use approximate operational ratios because the primary papers report effects such as diminished excitability/disrupted LTP, but exact numeric values still need figure/table digitization.

Do not use the output as a medical or astronaut-health prediction yet. Use it as the next engineering layer for building a defensible product pipeline.

## Key sources used for target/provenance design

- Acharya et al., 2019, eNeuro: chronic 18 cGy over 180 days, approximately 1 mGy/day, with diminished hippocampal excitability and disrupted LTP.
- Baulch et al., 2015 and Tseng et al., 2014: persistent oxidative stress in neural stem/progenitor radiation contexts.
- Selivanov et al., PLOS Computational Biology: mitochondrial respiratory-chain ROS modeling/bistability concept.
- Datta et al., 2012, PLOS ONE: high-LET heavy-ion persistent ROS/mitochondrial dysfunction benchmark.
- Parihar et al., 2016, Scientific Reports: low-cGy charged-particle exposure associated with persistent cognitive and neuronal structural deficits.


## Calibration-domain warning

The only current numeric fit anchor is around **1 mGy/day for 180 days**. Any SPENVIS scenario much above this, especially thin shielding and the Van Allen/RBSP-like case, is an extrapolation. The code therefore adds `calibration_domain_flag` and `dose_rate_to_primary_validation_ratio` to the endpoint output table.

## Recommended next step

1. Digitize exact effect sizes from the primary figures/tables.
2. Replace the approximate values in `validation_targets.csv`.
3. Rerun `python run_biology_calibration.py`.
4. Build `RADBIO_NEURO_003` using Brian2/NEURON with conductance-level fast/slow coupling.