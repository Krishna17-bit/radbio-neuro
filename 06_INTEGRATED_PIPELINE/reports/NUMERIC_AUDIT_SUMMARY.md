# RADBIO_NEURO Numeric Audit Summary Report

**Audit Run Timestamp**: 2026-06-23 21:26:35
**Project Root Path**: `D:\Downloads\Radiation modelling`

---

## 1. File Inventory and Properties

| Filename | Status | Rows | Columns |
| :--- | :---: | :---: | :---: |
| `pipeline_status_flags.csv` | ✔️ Exists | 3 | 2 |
| `biology_ready_dose_forcing_table.csv` | ✔️ Exists | 50 | 12 |
| `biology_calibrated_endpoint_predictions.csv` | ✔️ Exists | 50 | 16 |
| `biology_calibrated_daily_timecourses_all_scenarios.csv` | ✔️ Exists | 9050 | 12 |
| `neural_endpoint_simulation_summary.csv` | ✔️ Exists | 10 | 18 |
| `neural_timecourse_10mm_summary.csv` | ✔️ Exists | 26 | 18 |
| `scenario_interpretation_flags.csv` | ✔️ Exists | 50 | 6 |

---

## 2. Scientific Fallbacks & Warning Indicators

- **Monte Carlo Effective-Dose NaN Fallback**: 
  - **Status**: ⚠️ **FLAGGED**. The SPENVIS effective-dose Monte Carlo raw outputs contain NaN/non-numeric values and are audited but **not** used. The pipeline has successfully defaulted to **SHIELDOSE-2 tissue absorbed dose** as the active physics forcing input.

- **Van Allen Belt Extrapolation Warning**:
  - **Status**: ⚠️ **FLAGGED**. Thin-shielded Van Allen scenario cases exceed 10.0 mGy/day. These outputs are correctly flagged with `outside_primary_validation_domain_high_dose_rate` because they constitute a mathematical extrapolation far outside the primary chronic low-dose biological validation range (0.1 to 10.0 mGy/day).

- **Clinical Validation Disclaimer**:
  - **Status**: ⚠️ **DECLARED**. This software is a computational research prototype. All ROS, mitochondrial, and neural outputs are calibrated research-prototype metrics and **not** clinical, medical, or astronaut operational health predictions.

---

## 3. Detailed Numeric Column Metrics

### File: `pipeline_status_flags.csv`

| Column Name | Type | Rows | Min | Max | Mean | NaNs |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `layer` | `object` | 3 | - | - | - | 0 |
| `status` | `object` | 3 | - | - | - | 0 |

### File: `biology_ready_dose_forcing_table.csv`

| Column Name | Type | Rows | Min | Max | Mean | NaNs |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `scenario` | `object` | 50 | - | - | - | 0 |
| `shield_mm_Al` | `float64` | 50 | 0.05 | 20 | 5.678 | 0 |
| `mission_days` | `float64` | 50 | 180 | 180 | 180 | 0 |
| `total_dose_Gy` | `float64` | 50 | 0.20255 | 1.2009e+06 | 50663.4 | 0 |
| `total_dose_rate_Gy_day` | `float64` | 50 | 0.00112528 | 6671.67 | 281.463 | 0 |
| `total_dose_rate_mGy_day` | `float64` | 50 | 1.12528 | 6.67167e+06 | 281463 | 0 |
| `electron_dose_rate_mGy_day` | `float64` | 50 | 0 | 4.31906e+06 | 215684 | 0 |
| `brems_dose_rate_mGy_day` | `float64` | 50 | 0.00958556 | 10806.1 | 525.988 | 0 |
| `trapped_proton_dose_rate_mGy_day` | `float64` | 50 | 1.11572 | 2.342e+06 | 65256.8 | 0 |
| `ros_forcing_index_log01` | `float64` | 50 | 0.0479784 | 1 | 0.397696 | 0 |
| `forcing_regime_label` | `object` | 50 | - | - | - | 0 |
| `recommended_use` | `object` | 50 | - | - | - | 0 |

### File: `biology_calibrated_endpoint_predictions.csv`

| Column Name | Type | Rows | Min | Max | Mean | NaNs |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `scenario` | `object` | 50 | - | - | - | 0 |
| `shield_mm_Al` | `float64` | 50 | 0.05 | 20 | 5.678 | 0 |
| `mission_days` | `int64` | 50 | 180 | 180 | 180 | 0 |
| `total_dose_Gy` | `float64` | 50 | 0.20255 | 1.2009e+06 | 50663.4 | 0 |
| `dose_rate_mGy_day` | `float64` | 50 | 1.12528 | 6.67167e+06 | 281463 | 0 |
| `ros_norm_day_end` | `float64` | 50 | 0.640621 | 13.3523 | 5.31015 | 0 |
| `mito_integrity_day_end` | `float64` | 50 | 0.00182961 | 0.864026 | 0.199982 | 0 |
| `atp_proxy_day_end` | `float64` | 50 | 0.000432696 | 0.83562 | 0.183014 | 0 |
| `fast_excitability_delta_day_end` | `float64` | 50 | 0.0211089 | 0.0437817 | 0.0367941 | 0 |
| `slow_mito_atp_suppression_day_end` | `float64` | 50 | 0.244786 | 1.4885 | 1.21661 | 0 |
| `excitability_ratio_day_end` | `float64` | 50 | 0 | 0.776323 | 0.147697 | 0 |
| `ltp_proxy_day_end` | `float64` | 50 | 0 | 0.717958 | 0.129301 | 0 |
| `structural_neural_integrity_proxy_day_end` | `float64` | 50 | 0 | 0.850428 | 0.183532 | 0 |
| `dose_rate_to_primary_validation_ratio` | `float64` | 50 | 1.12528 | 6.67167e+06 | 281463 | 0 |
| `calibration_domain_flag` | `object` | 50 | - | - | - | 0 |
| `model_status` | `object` | 50 | - | - | - | 0 |

### File: `biology_calibrated_daily_timecourses_all_scenarios.csv`

| Column Name | Type | Rows | Min | Max | Mean | NaNs |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `day` | `float64` | 9050 | 0 | 180 | 90 | 0 |
| `dose_rate_mGy_day` | `float64` | 9050 | 1.12528 | 6.67167e+06 | 281463 | 0 |
| `ros_norm` | `float64` | 9050 | 0 | 13.3523 | 5.25359 | 0 |
| `mito_integrity` | `float64` | 9050 | 0 | 1 | 0.25513 | 0 |
| `atp_proxy` | `float64` | 9050 | 0 | 1 | 0.239982 | 0 |
| `fast_excitability_delta` | `float64` | 9050 | 0 | 0.0437817 | 0.0365464 | 0 |
| `slow_mito_atp_suppression` | `float64` | 9050 | 0 | 1.48914 | 1.13177 | 0 |
| `excitability_ratio` | `float64` | 9050 | 0 | 1.01621 | 0.209248 | 0 |
| `ltp_proxy` | `float64` | 9050 | 0 | 1 | 0.188674 | 0 |
| `structural_neural_integrity_proxy` | `float64` | 9050 | 0 | 1 | 0.240392 | 0 |
| `scenario` | `object` | 9050 | - | - | - | 0 |
| `shield_mm_Al` | `float64` | 9050 | 0.05 | 20 | 5.678 | 0 |

### File: `neural_endpoint_simulation_summary.csv`

| Column Name | Type | Rows | Min | Max | Mean | NaNs |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `scenario` | `object` | 10 | - | - | - | 0 |
| `shield_mm_Al` | `float64` | 10 | 1 | 20 | 7.6 | 0 |
| `day` | `float64` | 10 | 180 | 180 | 180 | 0 |
| `dose_rate_mGy_day` | `float64` | 10 | 1.12528 | 140017 | 18137.5 | 0 |
| `ros_norm` | `float64` | 10 | 0.640621 | 10.069 | 4.31161 | 0 |
| `mito_integrity` | `float64` | 10 | 0.00182961 | 0.864026 | 0.245828 | 0 |
| `atp_proxy` | `float64` | 10 | 0.000432696 | 0.83562 | 0.225016 | 0 |
| `fast_excitability_delta` | `float64` | 10 | 0.0211089 | 0.0430223 | 0.0353927 | 0 |
| `slow_mito_atp_suppression` | `float64` | 10 | 0.244786 | 1 | 0.823626 | 0 |
| `tau_eff_ms` | `float64` | 10 | 8.00208 | 16.044 | 9.94679 | 0 |
| `v_threshold_eff_mV` | `float64` | 10 | -48.8493 | -43.003 | -44.5751 | 0 |
| `drive_eff_mV` | `float64` | 10 | 2.10047 | 18.8418 | 6.59746 | 0 |
| `mean_firing_rate_hz` | `float64` | 10 | 0 | 29.1187 | 5.42625 | 0 |
| `total_spikes` | `int64` | 10 | 0 | 4659 | 868.2 | 0 |
| `synchrony_proxy_cv_10ms_bins` | `float64` | 10 | 0 | 2.29825 | 0.272624 | 0 |
| `isi_cv_mean` | `float64` | 10 | 0.228089 | 0.280432 | 0.254261 | 8 |
| `calibration_domain_flag` | `object` | 10 | - | - | - | 0 |
| `model_status` | `object` | 10 | - | - | - | 0 |

### File: `neural_timecourse_10mm_summary.csv`

| Column Name | Type | Rows | Min | Max | Mean | NaNs |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `scenario` | `object` | 26 | - | - | - | 0 |
| `shield_mm_Al` | `float64` | 26 | 10 | 10 | 10 | 0 |
| `day` | `float64` | 26 | 0 | 180 | 90 | 0 |
| `dose_rate_mGy_day` | `float64` | 26 | 1.55211 | 187.689 | 94.6205 | 0 |
| `ros_norm` | `float64` | 26 | 0 | 4.45272 | 2.42255 | 0 |
| `mito_integrity` | `float64` | 26 | 0.010974 | 1 | 0.496702 | 0 |
| `atp_proxy` | `float64` | 26 | 0.00390968 | 1 | 0.481947 | 0 |
| `fast_excitability_delta` | `float64` | 26 | 0 | 0.0395075 | 0.0291351 | 0 |
| `slow_mito_atp_suppression` | `float64` | 26 | 0 | 1 | 0.550689 | 0 |
| `tau_eff_ms` | `float64` | 26 | 8.01881 | 20 | 13.0212 | 0 |
| `v_threshold_eff_mV` | `float64` | 26 | -50 | -43.0274 | -46.3736 | 0 |
| `drive_eff_mV` | `float64` | 26 | 2.15519 | 22 | 11.7477 | 0 |
| `mean_firing_rate_hz` | `float64` | 26 | 0 | 35.9333 | 16.8423 | 0 |
| `total_spikes` | `int64` | 26 | 0 | 2156 | 1010.54 | 0 |
| `synchrony_proxy_cv_10ms_bins` | `float64` | 26 | 0 | 0.269077 | 0.128707 | 0 |
| `isi_cv_mean` | `float64` | 26 | 0.181809 | 0.257589 | 0.215944 | 12 |
| `calibration_domain_flag` | `object` | 26 | - | - | - | 0 |
| `model_status` | `object` | 26 | - | - | - | 0 |

### File: `scenario_interpretation_flags.csv`

| Column Name | Type | Rows | Min | Max | Mean | NaNs |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `scenario` | `object` | 50 | - | - | - | 0 |
| `shield_mm_Al` | `float64` | 50 | 0.05 | 20 | 5.678 | 0 |
| `dose_rate_mGy_day` | `float64` | 50 | 1.12528 | 6.67167e+06 | 281463 | 0 |
| `calibration_domain_flag` | `object` | 50 | - | - | - | 0 |
| `interpretation_class` | `object` | 50 | - | - | - | 0 |
| `recommended_user_message` | `object` | 50 | - | - | - | 0 |


---

## 4. Plain-Language Explanation of Outputs

1. **biology_ready_dose_forcing_table.csv**:
   Contains parsed ionizing radiation doses over 180 days from SHIELDOSE-2 and daily equivalent dose rates in mGy/day. These rates serve as the input forcing variables for biological cells.
   
2. **biology_calibrated_endpoint_predictions.csv**:
   Outputs the steady-state biological proxies at Day 180. The excitability ratio and LTP proxies show how cellular stress compromises electrical functions. Low values represent deficits.
   
3. **biology_calibrated_daily_timecourses_all_scenarios.csv**:
   Shows how ROS builds up and how mitochondrial integrity degrades day-by-day. In high-exposure cases, ROS rises quickly while mitochondria fail over weeks.
   
4. **neural_endpoint_simulation_summary.csv**:
   Summarizes the functional firing rates of the leaky integrate-and-fire network simulation. Suppressed ATP levels cause the population firing rates to decline dramatically.
   
5. **neural_timecourse_10mm_summary.csv**:
   Shows daily changes in network excitability parameters (threshold, baseline drive, and membrane tau) and population firing rates at 10 mm Al.
   
6. **scenario_interpretation_flags.csv**:
   Provides scenario/shielding-specific warnings and flags (e.g. validated vs. extrapolated vs. extreme stress), and recommended user messages for dashboard presentation.
