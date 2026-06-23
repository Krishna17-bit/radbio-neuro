# Data Dictionary

This document details the main CSV data files generated throughout the radiation modelling pipeline and defines their column headers, data types, and units.

---

## 1. Physics Forcing Table
- **Files**:
  - `06_INTEGRATED_PIPELINE/outputs/biology_ready_dose_forcing_table.csv`
  - `02_RADBIO_NEURO_001_PHYSICS_LAYER/RADBIO_NEURO_001_NOTEBOOK_BUILD/outputs/biology_ready_dose_forcing_table.csv`

### Column Definitions
| Column Name | Type | Description |
| :--- | :--- | :--- |
| `scenario` | String | Orbit name: `LEO_ISS_like` or `VAB_RBSP_like` |
| `shield_mm_Al` | Float | Aluminium equivalent shielding thickness (mm) |
| `mission_days` | Float | Mission duration (days, default 180.0) |
| `total_dose_Gy` | Float | Total SHIELDOSE-2 tissue absorbed dose (Gy) over the mission |
| `total_dose_rate_Gy_day` | Float | Daily dose-rate in Gray per day (Gy/day) |
| `total_dose_rate_mGy_day` | Float | Daily dose-rate in milligray per day (mGy/day) |
| `electron_dose_rate_mGy_day`| Float | Absorbed dose-rate contribution from trapped electrons (mGy/day) |
| `brems_dose_rate_mGy_day` | Float | Absorbed dose-rate contribution from bremsstrahlung (mGy/day) |
| `trapped_proton_dose_rate_mGy_day` | Float | Absorbed dose-rate contribution from trapped protons (mGy/day) |
| `ros_forcing_index_log01` | Float | Logarithmic scale normalization of dose-rate [0.0 - 1.0] for prototype ROS induction |
| `forcing_regime_label` | String | Descriptive dose-rate categorization (e.g. `low_model_forcing`, `extreme_model_forcing`) |
| `recommended_use` | String | Contextual tag indicating scenario stress-test status |

---

## 2. Biology Calibration Outputs
- **Files**:
  - `06_INTEGRATED_PIPELINE/outputs/biology_calibrated_endpoint_predictions.csv`
  - `06_INTEGRATED_PIPELINE/outputs/selected_shielding_biology_summary.csv`

### Column Definitions
| Column Name | Type | Description |
| :--- | :--- | :--- |
| `scenario` | String | Orbit name: `LEO_ISS_like` or `VAB_RBSP_like` |
| `shield_mm_Al` | Float | Aluminium equivalent shielding thickness (mm) |
| `mission_days` | Float | Mission duration (days) |
| `total_dose_Gy` | Float | Total SHIELDOSE-2 absorbed dose (Gy) |
| `dose_rate_mGy_day` | Float | Daily dose-rate input (mGy/day) |
| `ros_norm_day_end` | Float | Dimensionless ROS burden index at mission end (can exceed 1.0 under high doses) |
| `mito_integrity_day_end` | Float | Bounded mitochondrial integrity at mission end [0.0 - 1.0] |
| `atp_proxy_day_end` | Float | Estimated cellular ATP production fraction at mission end [0.0 - 1.0] |
| `fast_excitability_delta_day_end` | Float | Fast redox-driven change in neural excitability |
| `slow_mito_atp_suppression_day_end` | Float | Slow bioenergetics-driven neural drive reduction |
| `excitability_ratio_day_end` | Float | Ratio of target neural excitability relative to control [0.0 - 2.0] |
| `ltp_proxy_day_end` | Float | Long-Term Potentiation (LTP) fraction relative to control [0.0 - 1.5] |
| `structural_neural_integrity_proxy_day_end` | Float | Structural dendritic integrity relative to control [0.0 - 1.2] |
| `dose_rate_to_primary_validation_ratio` | Float | Ratio of the scenario dose rate to the primary chronic validation target (1.0 mGy/day) |
| `calibration_domain_flag` | String | Extrapolation warning flag (e.g. `outside_primary_validation_domain_high_dose_rate`) |
| `model_status` | String | Model validity classification label |

---

## 3. Neural Simulation Summaries
- **Files**:
  - `06_INTEGRATED_PIPELINE/outputs/neural_endpoint_simulation_summary.csv`
  - `06_INTEGRATED_PIPELINE/outputs/neural_timecourse_10mm_summary.csv`

### Column Definitions
| Column Name | Type | Description |
| :--- | :--- | :--- |
| `scenario` | String | Orbit name: `LEO_ISS_like` or `VAB_RBSP_like` |
| `shield_mm_Al` | Float | Aluminium equivalent shielding thickness (mm) |
| `day` | Float | Timepoint day of simulation |
| `dose_rate_mGy_day` | Float | Daily dose-rate input (mGy/day) |
| `ros_norm` | Float | Input dimensionless ROS burden index mapped from biology (can exceed 1.0) |
| `mito_integrity` | Float | Input mitochondrial integrity mapped from biology |
| `atp_proxy` | Float | Input ATP level mapped from biology |
| `fast_excitability_delta` | Float | Fast redox delta mapped from biology |
| `slow_mito_atp_suppression` | Float | Slow ATP suppression mapped from biology |
| `tau_eff_ms` | Float | Mapped membrane integration time constant of neurons (ms) |
| `v_threshold_eff_mV` | Float | Mapped membrane firing threshold potential (eff_mV) |
| `drive_eff_mV` | Float | Mapped baseline drive current amplitude (mV equivalent) |
| `mean_firing_rate_hz` | Float | Mean firing rate across simulated neuron population (Hz) |
| `total_spikes` | Integer | Total count of action potentials during simulation |
| `synchrony_proxy_cv_10ms_bins` | Float | Coefficient of variation of population spiking binned at 10 ms |
| `isi_cv_mean` | Float | Coefficient of variation of inter-spike intervals, averaged across active neurons |
| `calibration_domain_flag` | String | Extrapolation warning flag |
| `model_status` | String | Model status label |
