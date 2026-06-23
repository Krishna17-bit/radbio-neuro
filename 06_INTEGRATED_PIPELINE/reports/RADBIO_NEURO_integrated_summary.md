# RADBIO_NEURO Integrated Pipeline Summary Report

**Date**: 2026-06-23
**Disclaimer**: Research prototype only. Not for medical, operational, or astronaut health decision-making.

---

## 1. Project Summary
This pipeline integrates radiation environment analysis (SPENVIS) with biological cellular modeling (ROS, mitochondrial integrity, ATP) and leaky integrate-and-fire neural network simulations to project biological risks associated with space radiation.

## 2. Dataset Summary
- **Scenario A (LEO_ISS_like)**: Circular 400 km orbit, 51.6° inclination, 180 days.
- **Scenario B (VAB_RBSP_like)**: Perigee 600 km, apogee 30600 km (Van Allen Belt crossing), 10° inclination, 180 days.
- **Shielding Depth Options**: 1, 2, 5, 10, and 20 mm Aluminium equivalent.

## 3. Dose vs Shielding & Dose-Rate Summary
*Current effective-dose Monte Carlo files showed NaN and are not used. SHIELDOSE-2 tissue absorbed dose is used as the current physics input.*

### Dose-Rate Table
| Scenario | Shielding (mm Al) | Total Dose (Gy) | Daily Dose-Rate (mGy/day) | Regime |
| :--- | :---: | :---: | :---: | :---: |
| LEO_ISS_like | 1.0 | 12.0720 | 67.0667 | high_model_forcing |
| LEO_ISS_like | 2.0 | 4.4483 | 24.7128 | high_model_forcing |
| LEO_ISS_like | 5.0 | 0.6783 | 3.7682 | moderate_model_forcing |
| LEO_ISS_like | 10.0 | 0.2794 | 1.5521 | moderate_model_forcing |
| LEO_ISS_like | 20.0 | 0.2026 | 1.1253 | moderate_model_forcing |
| VAB_RBSP_like | 1.0 | 25203.0000 | 140016.6667 | extreme_model_forcing |
| VAB_RBSP_like | 2.0 | 6965.1000 | 38695.0000 | extreme_model_forcing |
| VAB_RBSP_like | 5.0 | 409.6100 | 2275.6111 | extreme_model_forcing |
| VAB_RBSP_like | 10.0 | 33.7840 | 187.6889 | extreme_model_forcing |
| VAB_RBSP_like | 20.0 | 18.3930 | 102.1833 | extreme_model_forcing |

---

## 4. Biological Calibration Layer Outputs
*The ROS/mitochondria model is a calibration scaffold with literature anchors (Acharya et al., 2019), not complete experimental validation. Note: ROS burden index is a dimensionless ROS accumulation metric, not a bounded 0-1 value.*

### Endpoint Biology Metrics (Day 180)
| Scenario | Shielding (mm Al) | ROS Burden Index | Mito Integrity | ATP Proxy | Domain Flag |
| :--- | :---: | :---: | :---: | :---: | :---: |
| LEO_ISS_like | 1.0 | 3.5863 | 0.0303 | 0.0136 | outside_primary_validation_domain_high_dose_rate |
| LEO_ISS_like | 2.0 | 2.7591 | 0.0920 | 0.0533 | outside_primary_validation_domain_high_dose_rate |
| LEO_ISS_like | 5.0 | 1.3273 | 0.6177 | 0.5532 | near_primary_validation_domain |
| LEO_ISS_like | 10.0 | 0.7961 | 0.8178 | 0.7810 | near_primary_validation_domain |
| LEO_ISS_like | 20.0 | 0.6406 | 0.8640 | 0.8356 | near_primary_validation_domain |
| VAB_RBSP_like | 1.0 | 10.0690 | 0.0018 | 0.0004 | outside_primary_validation_domain_high_dose_rate |
| VAB_RBSP_like | 2.0 | 8.9762 | 0.0018 | 0.0004 | outside_primary_validation_domain_high_dose_rate |
| VAB_RBSP_like | 5.0 | 6.5689 | 0.0018 | 0.0004 | outside_primary_validation_domain_high_dose_rate |
| VAB_RBSP_like | 10.0 | 4.4527 | 0.0110 | 0.0039 | outside_primary_validation_domain_high_dose_rate |
| VAB_RBSP_like | 20.0 | 3.9398 | 0.0201 | 0.0082 | outside_primary_validation_domain_high_dose_rate |

---

## 5. Neural Simulation Layer Outputs
*The LIF neural simulation layer simulates functional network excitability under mapped bioenergetic constraints.*

### Endpoint Neural Metrics (Day 180)
| Scenario | Shielding (mm Al) | Firing Rate (Hz) | tau_eff (ms) | V_threshold (mV) | Drive (mV) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| LEO_ISS_like | 1.0 | 0.00 | 8.07 | -43.10 | 2.34 |
| LEO_ISS_like | 2.0 | 0.00 | 8.26 | -43.37 | 3.13 |
| LEO_ISS_like | 5.0 | 0.23 | 11.97 | -46.87 | 13.19 |
| LEO_ISS_like | 10.0 | 24.91 | 15.05 | -48.47 | 17.76 |
| LEO_ISS_like | 20.0 | 29.12 | 16.04 | -48.85 | 18.84 |
| VAB_RBSP_like | 1.0 | 0.00 | 8.00 | -43.00 | 2.11 |
| VAB_RBSP_like | 2.0 | 0.00 | 8.00 | -43.00 | 2.11 |
| VAB_RBSP_like | 5.0 | 0.00 | 8.00 | -43.00 | 2.10 |
| VAB_RBSP_like | 10.0 | 0.00 | 8.02 | -43.03 | 2.16 |
| VAB_RBSP_like | 20.0 | 0.00 | 8.04 | -43.06 | 2.24 |

---

## 6. Scientific Limitations & Domain Flags
- **Monte Carlo NaN Audit**: Mulassis effective-dose files contained non-numeric entries; tissue absorbed dose (SHIELDOSE-2) is the active physics input.
- **Van Allen Belt Extrapolation**: Forcing levels >10 mGy/day are far outside the primary chronic low-dose validation domain (~1 mGy/day) and represent mathematical extrapolation.
- **No Clinical Diagnostics**: This prototype must not be used to predict clinical astronaut health outcomes or operational safety.
- **Research Prototyping**: ROS, mitochondrial, and neural outputs are comparative research-prototype outputs, not clinical or operational predictions.

## 7. Next Steps
1. Rerun SPENVIS Monte Carlo files to resolve non-NaN Sievert equivalents.
2. Incorporate high-LET proton/GCR weighting factor (RBE).
3. Calibrate cellular kinetic rates against multiple in-vitro and in-vivo literature studies.
