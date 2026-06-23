# Scientific Limitations & Warnings (Research Prototype)

> [!WARNING]
> **CRITICAL DISCLAIMER**: This software is a computational research prototype. All ROS, mitochondrial, and neural network outputs are modeled metrics and **must not** be used for clinical diagnosis, medical prognosis, astronaut health monitoring, or spacecraft mission operational planning.

The following sections detail the core scientific limitations, fallbacks, and extrapolation boundaries of this model:

## 1. Physics Input: SHIELDOSE-2 Absorbed Dose
- **Active Physics Input**: The physics layer uses **SHIELDOSE-2 tissue absorbed dose** (Gy over 180 days) as the active forcing variable.
- **Limitation**: Absorbed dose (Gy) does not account for radiation quality factors (LET/RBE) of high-energy trapped protons, galactic cosmic rays (GCR), or secondary neutrons. The actual biological damage equivalent (Sv) may be significantly higher than modeled.

## 2. SPENVIS Effective-Dose MC NaN Fallback
- **Status**: The SPENVIS effective-dose Monte Carlo raw outputs contain non-numeric `NaN` values.
- **Action**: These Monte Carlo results are audited, flagged as unusable, and **not** passed to the biological calibration layer.
- **Remediation**: Re-simulation with verified configurations is required to obtain reliable Sievert (Sv) dose-equivalent outputs.

## 3. Extrapolation Beyond Calibration Domain
- **Validated Domain**: The primary biological validation domain is anchored to chronic low-dose-rate space environments ($0.1$ to $10.0$ mGy/day), referencing mouse neuroelectrophysiology data (Acharya et al., eNeuro 2019).
- **Extrapolation**: Projections for dose rates outside the $[0.1, 10.0]$ mGy/day range are mathematically extrapolated.
- **Van Allen belt crossing**: Thin-shielded VAB scenarios (>100 mGy/day) represent extreme dose rates. These projections constitute a stress-test only; the biological model is not validated under these conditions.

## 4. Scaffold Model Nature
- **Status**: The ROS/mitochondria/ATP kinetic model and integrate-and-fire network are mathematical scaffolds designed for testing pipeline software and comparative shielding, rather than complete experimental physiological validation.
