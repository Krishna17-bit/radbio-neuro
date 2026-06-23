# Model Card: ROS/Mito & Neural LIF Scaffolds (Research Prototype)

> [!WARNING]
> **COMPUTATIONAL PROTOTYPE ONLY**: All cellular and network outputs represent comparative mathematical scaffolds and are not clinically validated. Do not make medical or operational health claims based on this model.

## Model Details
- **Model Type**: Bounded cellular kinetic dynamics coupled to a stochastic Leaky Integrate-and-Fire (LIF) network.
- **Physics Forcing Input**: SHIELDOSE-2 tissue absorbed dose (Gy/day, converted to mGy/day).
- **Consolidated Package**: `radbio_neuro/` is the canonical source.

## Assumptions & Fallbacks
1. **Effective-Dose MC NaN Fallback**: Raw SPENVIS effective-dose files contained non-numeric NaN values. They are audited and flagged as unusable. The pipeline falls back to SHIELDOSE-2 tissue absorbed dose as the active physics forcing input.
2. **Dimensionless ROS Index**: The ROS value (`ros_norm`) is simulated as a dimensionless **ROS burden index**, not a bounded 0–1 normalized value. It can grow logarithmically with dose rate.
3. **No Clinical Validity**: The model is fit to sparse literature mouse targets (Acharya et al., eNeuro 2019) at chronic low-dose rates (~1.0 mGy/day). It is not clinically validated for clinical diagnoses.

## Domain & Extrapolation
- **Primary Calibration Domain**: $0.1$ to $10.0$ mGy/day.
- **Extrapolation Bounds**: Values $< 0.1$ or $> 10.0$ mGy/day are flagged as extrapolations.
- **Van Allen Belt Stress Test**: Thin-shielded VAB scenarios (>100 mGy/day) represent extreme extrapolation stress tests where biological cell response limits have not been validated.
- **Zero-Firing State**: Under severe VAB stress, complete bioenergetic ATP depletion shuts down LIF neural network firing (zero firing), which represents an extreme stress-test state, not missing data.
