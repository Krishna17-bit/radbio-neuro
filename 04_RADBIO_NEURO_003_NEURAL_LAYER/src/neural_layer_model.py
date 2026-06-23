
"""
RADBIO_NEURO_003 neural layer model.

This module converts RADBIO_NEURO_002 daily biology states into a small
conductance-aware leaky integrate-and-fire network simulation.

Scientific status:
- This is a neural simulation scaffold, not a validated human clinical predictor.
- Biology inputs are absorbed-dose-derived and still need stronger experimental calibration.
- The model deliberately separates acute ROS/channel effects from slow mitochondrial/ATP suppression.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Tuple, Optional
import numpy as np
import pandas as pd


@dataclass
class NeuralSimConfig:
    n_neurons: int = 80
    sim_ms: float = 2000.0
    dt_ms: float = 0.1
    seed: int = 1337
    # Membrane model in mV/ms units; a compact LIF equivalent of a conductance model.
    v_rest_mV: float = -65.0
    v_reset_mV: float = -65.0
    v_threshold_mV: float = -50.0
    tau_m_ms: float = 20.0
    refractory_ms: float = 5.0
    # Effective drive term; tuned to produce a healthy control rate around tens of Hz,
    # then reduced by mitochondrial/ATP stress.
    baseline_drive_mV: float = 22.0
    fast_ros_drive_gain_mV: float = 8.0
    damage_threshold_shift_mV: float = 7.0
    damage_leak_gain: float = 1.5
    noise_mV: float = 3.0


def _safe_float(row: pd.Series, key: str, default: float) -> float:
    value = row.get(key, default)
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def state_to_neural_parameters(row: pd.Series, cfg: NeuralSimConfig) -> Dict[str, float]:
    """Map calibrated biology state to neural membrane parameters.

    Fast term: ROS/channel oxidation can transiently increase drive.
    Slow term: mitochondrial injury and ATP depletion lower drive, shorten membrane integration,
    and shift threshold upward.
    """
    ros = max(_safe_float(row, 'ros_norm_day_end', _safe_float(row, 'ros_norm', 0.0)), 0.0)
    mito = min(max(_safe_float(row, 'mito_integrity_day_end', _safe_float(row, 'mito_integrity', 1.0)), 0.0), 1.0)
    atp = min(max(_safe_float(row, 'atp_proxy_day_end', _safe_float(row, 'atp_proxy', mito)), 0.0), 1.0)
    fast_delta = max(_safe_float(row, 'fast_excitability_delta_day_end', _safe_float(row, 'fast_excitability_delta', 0.0)), 0.0)
    slow_supp = min(max(_safe_float(row, 'slow_mito_atp_suppression_day_end', _safe_float(row, 'slow_mito_atp_suppression', 0.0)), 0.0), 1.0)

    tau_eff = cfg.tau_m_ms / (1.0 + cfg.damage_leak_gain * (1.0 - atp))
    v_threshold_eff = cfg.v_threshold_mV + cfg.damage_threshold_shift_mV * (1.0 - atp)
    # ATP preserves drive. ROS fast term can add transient excitation, but it cannot rescue
    # severe ATP collapse because baseline drive remains bioenergetically limited.
    drive_eff = cfg.baseline_drive_mV * (0.08 + 0.92 * atp) + cfg.fast_ros_drive_gain_mV * fast_delta
    noise_eff = cfg.noise_mV * (0.30 + 0.70 * atp)

    return {
        'ros_norm': ros,
        'mito_integrity': mito,
        'atp_proxy': atp,
        'fast_excitability_delta': fast_delta,
        'slow_mito_atp_suppression': slow_supp,
        'tau_eff_ms': tau_eff,
        'v_threshold_eff_mV': v_threshold_eff,
        'drive_eff_mV': drive_eff,
        'noise_eff_mV': noise_eff,
    }


def run_lif_network(row: pd.Series, cfg: Optional[NeuralSimConfig] = None) -> Dict[str, object]:
    """Run a stochastic LIF population for one biology state row."""
    cfg = cfg or NeuralSimConfig()
    pars = state_to_neural_parameters(row, cfg)
    rng = np.random.default_rng(cfg.seed)
    n_steps = int(cfg.sim_ms / cfg.dt_ms)
    n = int(cfg.n_neurons)
    v = cfg.v_rest_mV + rng.normal(0.0, 1.0, size=n)
    refractory = np.zeros(n, dtype=float)
    spike_times = []
    spike_neurons = []
    # Track a subset of membrane traces for plotting.
    trace_count = min(5, n)
    traces = np.zeros((n_steps, trace_count), dtype=float)

    tau_eff = pars['tau_eff_ms']
    v_thr = pars['v_threshold_eff_mV']
    drive_eff = pars['drive_eff_mV']
    noise_eff = pars['noise_eff_mV']

    for step in range(n_steps):
        t_ms = step * cfg.dt_ms
        active = refractory <= 0.0
        # LIF update with effective conductance/leak via tau_eff. Noise is scaled by dt/tau.
        noise = rng.normal(0.0, noise_eff * np.sqrt(cfg.dt_ms / max(tau_eff, 1e-9)), size=n)
        dv = (cfg.dt_ms / max(tau_eff, 1e-9)) * ((cfg.v_rest_mV - v) + drive_eff) + noise
        v[active] += dv[active]
        v[~active] = cfg.v_reset_mV
        refractory[refractory > 0.0] -= cfg.dt_ms
        spiking = (v >= v_thr) & active
        if np.any(spiking):
            idx = np.where(spiking)[0]
            spike_times.extend([t_ms] * len(idx))
            spike_neurons.extend(idx.tolist())
            v[spiking] = cfg.v_reset_mV
            refractory[spiking] = cfg.refractory_ms
        traces[step, :] = v[:trace_count]

    total_spikes = len(spike_times)
    mean_rate_hz = total_spikes / (n * (cfg.sim_ms / 1000.0))

    # Population synchrony proxy: coefficient of variation of 10 ms binned spike counts.
    if total_spikes > 0:
        bins = np.arange(0, cfg.sim_ms + 10.0, 10.0)
        counts, _ = np.histogram(spike_times, bins=bins)
        synchrony_proxy = float(np.std(counts) / (np.mean(counts) + 1e-9))
    else:
        synchrony_proxy = 0.0

    # ISI CV averaged over neurons with enough spikes.
    cv_vals = []
    if total_spikes > 0:
        st = np.asarray(spike_times)
        sn = np.asarray(spike_neurons)
        for neuron_id in np.unique(sn):
            times = np.sort(st[sn == neuron_id])
            if len(times) >= 3:
                isi = np.diff(times)
                cv_vals.append(float(np.std(isi) / (np.mean(isi) + 1e-9)))
    isi_cv_mean = float(np.mean(cv_vals)) if cv_vals else np.nan

    return {
        **pars,
        'n_neurons': n,
        'sim_ms': cfg.sim_ms,
        'dt_ms': cfg.dt_ms,
        'total_spikes': int(total_spikes),
        'mean_firing_rate_hz': float(mean_rate_hz),
        'synchrony_proxy_cv_10ms_bins': synchrony_proxy,
        'isi_cv_mean': isi_cv_mean,
        'spike_times_ms': np.asarray(spike_times, dtype=float),
        'spike_neurons': np.asarray(spike_neurons, dtype=int),
        'voltage_traces_mV': traces,
        'trace_time_ms': np.arange(n_steps) * cfg.dt_ms,
        'config': asdict(cfg),
    }


def summarize_result(row: pd.Series, result: Dict[str, object]) -> Dict[str, object]:
    """Flatten simulation output to CSV-friendly summary."""
    return {
        'scenario': row.get('scenario', 'unknown'),
        'shield_mm_Al': _safe_float(row, 'shield_mm_Al', np.nan),
        'day': _safe_float(row, 'day', _safe_float(row, 'mission_days', np.nan)),
        'dose_rate_mGy_day': _safe_float(row, 'dose_rate_mGy_day', np.nan),
        'ros_norm': result['ros_norm'],
        'mito_integrity': result['mito_integrity'],
        'atp_proxy': result['atp_proxy'],
        'fast_excitability_delta': result['fast_excitability_delta'],
        'slow_mito_atp_suppression': result['slow_mito_atp_suppression'],
        'tau_eff_ms': result['tau_eff_ms'],
        'v_threshold_eff_mV': result['v_threshold_eff_mV'],
        'drive_eff_mV': result['drive_eff_mV'],
        'mean_firing_rate_hz': result['mean_firing_rate_hz'],
        'total_spikes': result['total_spikes'],
        'synchrony_proxy_cv_10ms_bins': result['synchrony_proxy_cv_10ms_bins'],
        'isi_cv_mean': result['isi_cv_mean'],
        'calibration_domain_flag': row.get('calibration_domain_flag', 'unknown'),
        'model_status': row.get('model_status', 'neural_scaffold_downstream_of_calibrated_biology_layer'),
    }
