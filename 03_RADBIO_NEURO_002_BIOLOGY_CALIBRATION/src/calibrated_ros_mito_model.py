
"""
RADBIO_NEURO_002 calibrated ROS/mitochondria biology scaffold.

This module intentionally separates fast ROS/channel effects from slow
mitochondrial/ATP failure. It is not a final validated biological model.
It is a calibration scaffold that should be refit after primary-paper figure
values are digitized.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import numpy as np
import pandas as pd

@dataclass
class RosMitoParams:
    # ROS kinetics, per day; forcing is dose_rate_mGy_day relative to ref_dose_rate_mGy_day
    k_ros_prod: float = 0.22
    k_ros_clear: float = 0.45
    ros_ec50: float = 0.6
    ref_dose_rate_mGy_day: float = 1.0

    # Mitochondrial injury/repair, per day
    k_mito_damage: float = 0.0013
    k_mito_ros_amplification: float = 0.15
    k_mito_repair: float = 0.00025
    atp_exponent: float = 1.4

    # Neural proxies
    fast_excitability_gain: float = 0.045   # acute ROS/channel term: can increase excitability
    slow_suppression_gain: float = 1.55     # chronic ATP/mitochondria term: suppresses excitability
    ltp_mito_gain: float = 1.80
    ltp_ros_gain: float = 0.06

    # Numerical safety
    min_excitability_ratio: float = 0.0
    max_excitability_ratio: float = 2.0


def simulate_constant_exposure(
    dose_rate_mGy_day: float,
    days: int = 180,
    params: RosMitoParams | None = None,
    dt_day: float = 1.0,
) -> pd.DataFrame:
    """Simulate daily ROS, mitochondrial integrity, ATP proxy, and neural proxies."""
    if params is None:
        params = RosMitoParams()
    steps = int(np.ceil(days / dt_day)) + 1
    t = np.arange(steps) * dt_day
    ros = np.zeros(steps)
    mito = np.ones(steps)

    forcing = max(float(dose_rate_mGy_day), 0.0) / max(params.ref_dose_rate_mGy_day, 1e-12)
    for i in range(1, steps):
        # Acute ROS with clearance. Production is sublinear to avoid explosive behavior at extreme VAB doses.
        prod = params.k_ros_prod * np.log1p(forcing)
        d_ros = prod - params.k_ros_clear * ros[i-1]
        ros[i] = max(0.0, ros[i-1] + dt_day * d_ros)

        # Chronic injury and repair. Damage depends on dose-rate and ROS amplification.
        damage_rate = params.k_mito_damage * forcing * (1.0 + params.k_mito_ros_amplification * ros[i-1])
        repair_rate = params.k_mito_repair * (1.0 - mito[i-1])
        d_mito = -damage_rate * mito[i-1] + repair_rate
        mito[i] = float(np.clip(mito[i-1] + dt_day * d_mito, 0.0, 1.0))

    atp = np.clip(mito ** params.atp_exponent, 0.0, 1.0)
    fast = params.fast_excitability_gain * ros / (params.ros_ec50 + ros + 1e-12)
    slow = params.slow_suppression_gain * (1.0 - atp)
    excit = np.clip(1.0 + fast - slow, params.min_excitability_ratio, params.max_excitability_ratio)
    ltp = np.clip(1.0 - params.ltp_mito_gain * (1.0 - mito) - params.ltp_ros_gain * ros/(params.ros_ec50 + ros + 1e-12), 0.0, 1.5)
    structural = np.clip(1.0 - 1.10 * (1.0 - mito), 0.0, 1.2)

    return pd.DataFrame({
        'day': t,
        'dose_rate_mGy_day': dose_rate_mGy_day,
        'ros_norm': ros,
        'mito_integrity': mito,
        'atp_proxy': atp,
        'fast_excitability_delta': fast,
        'slow_mito_atp_suppression': slow,
        'excitability_ratio': excit,
        'ltp_proxy': ltp,
        'structural_neural_integrity_proxy': structural,
    })


def score_params(params: RosMitoParams, targets: pd.DataFrame) -> float:
    """Weighted squared error for numeric targets marked as fit anchors."""
    score = 0.0
    used = 0
    for _, row in targets.iterrows():
        role = str(row.get('calibration_role', ''))
        if 'fit_anchor' not in role:
            continue
        target = row.get('target_ratio_to_control')
        sigma = row.get('target_uncertainty_1sigma')
        var = row.get('model_target_variable')
        dose_rate = row.get('dose_rate_mGy_day')
        days = row.get('exposure_days')
        if pd.isna(target) or pd.isna(dose_rate) or pd.isna(days) or not isinstance(var, str):
            continue
        sim = simulate_constant_exposure(float(dose_rate), int(days), params)
        pred = float(sim[var].iloc[-1])
        sigma = float(sigma) if not pd.isna(sigma) and float(sigma) > 0 else 0.2
        score += ((pred - float(target)) / sigma) ** 2
        used += 1
    return score / max(used, 1)


def calibrate_to_targets(targets: pd.DataFrame, n_random: int = 5000, seed: int = 7) -> RosMitoParams:
    """Lightweight random search calibration for the current scaffold targets."""
    rng = np.random.default_rng(seed)
    best = RosMitoParams()
    best_score = score_params(best, targets)
    for _ in range(n_random):
        p = RosMitoParams(
            k_ros_prod=float(rng.uniform(0.08, 0.45)),
            k_ros_clear=float(rng.uniform(0.25, 0.85)),
            ros_ec50=float(rng.uniform(0.25, 1.2)),
            k_mito_damage=float(10 ** rng.uniform(-3.7, -2.1)),
            k_mito_ros_amplification=float(rng.uniform(0.0, 0.5)),
            k_mito_repair=float(10 ** rng.uniform(-4.5, -2.6)),
            atp_exponent=float(rng.uniform(1.0, 2.4)),
            fast_excitability_gain=float(rng.uniform(0.0, 0.10)),
            slow_suppression_gain=float(rng.uniform(0.8, 2.6)),
            ltp_mito_gain=float(rng.uniform(0.8, 3.0)),
            ltp_ros_gain=float(rng.uniform(0.0, 0.12)),
        )
        s = score_params(p, targets)
        if s < best_score:
            best = p
            best_score = s
    return best


def predict_for_forcing_table(forcing_table: pd.DataFrame, params: RosMitoParams, days_col: str = 'mission_days') -> pd.DataFrame:
    rows = []
    timecourses = []
    for _, r in forcing_table.iterrows():
        days = int(round(float(r.get(days_col, 180)))) if days_col in r else 180
        dose_rate = float(r['total_dose_rate_mGy_day'])
        sim = simulate_constant_exposure(dose_rate, days=days, params=params)
        sim['scenario'] = r['scenario']
        sim['shield_mm_Al'] = r['shield_mm_Al']
        timecourses.append(sim)
        end = sim.iloc[-1].to_dict()
        rows.append({
            'scenario': r['scenario'],
            'shield_mm_Al': r['shield_mm_Al'],
            'mission_days': days,
            'total_dose_Gy': r.get('total_dose_Gy', np.nan),
            'dose_rate_mGy_day': dose_rate,
            'ros_norm_day_end': end['ros_norm'],
            'mito_integrity_day_end': end['mito_integrity'],
            'atp_proxy_day_end': end['atp_proxy'],
            'fast_excitability_delta_day_end': end['fast_excitability_delta'],
            'slow_mito_atp_suppression_day_end': end['slow_mito_atp_suppression'],
            'excitability_ratio_day_end': end['excitability_ratio'],
            'ltp_proxy_day_end': end['ltp_proxy'],
            'structural_neural_integrity_proxy_day_end': end['structural_neural_integrity_proxy'],
            'dose_rate_to_primary_validation_ratio': dose_rate / 1.0,
            'calibration_domain_flag': (
                'near_primary_validation_domain' if 0.1 <= dose_rate <= 10.0 else
                'outside_primary_validation_domain_high_dose_rate' if dose_rate > 10.0 else
                'outside_primary_validation_domain_low_dose_rate'
            ),
            'model_status': 'calibrated_scaffold_absorbed_dose_only_not_validated_risk_claim',
        })
    return pd.DataFrame(rows), pd.concat(timecourses, ignore_index=True)


def params_to_dict(params: RosMitoParams) -> dict:
    return asdict(params)
