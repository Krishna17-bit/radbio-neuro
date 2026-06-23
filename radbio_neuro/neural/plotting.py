import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import numpy as np

def plot_neural_results(endpoint: pd.DataFrame, timecourse: pd.DataFrame, example_results: dict, fig_dir: Path):
    """Plot neural model outputs and networks dynamics."""
    fig_dir.mkdir(exist_ok=True, parents=True)
    
    # 1. Endpoint firing rate vs shielding
    fig, ax = plt.subplots(figsize=(8, 5))
    for scenario, group in endpoint.groupby('scenario'):
        g = group.sort_values('shield_mm_Al')
        ax.plot(g['shield_mm_Al'], g['mean_firing_rate_hz'], marker='o', label=scenario)
    ax.set_xscale('log')
    ax.set_xlabel('Al shielding thickness (mm)')
    ax.set_ylabel('Modelled neural network firing rate (Hz)')
    ax.set_title('Modelled neural network firing rate (Research Prototype)')
    ax.legend()
    ax.grid(True, which='both', alpha=0.3)
    fig.tight_layout()
    fig.savefig(fig_dir / 'endpoint_firing_rate_vs_shielding.png', dpi=200)
    plt.close(fig)

    # 2. Timecourse firing rate at 10 mm Al
    fig, ax = plt.subplots(figsize=(8, 5))
    for scenario, group in timecourse.groupby('scenario'):
        g = group.sort_values('day')
        ax.plot(g['day'], g['mean_firing_rate_hz'], marker='o', label=scenario)
    ax.set_xlabel('Mission day')
    ax.set_ylabel('Modelled neural network firing rate (Hz)')
    ax.set_title('Modelled firing rate timecourse at 10 mm Al (Research Prototype)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(fig_dir / 'timecourse_firing_rate_10mm.png', dpi=200)
    plt.close(fig)

    # 3. Effective drive vs shielding
    fig, ax = plt.subplots(figsize=(8, 5))
    for scenario, group in endpoint.groupby('scenario'):
        g = group.sort_values('shield_mm_Al')
        ax.plot(g['shield_mm_Al'], g['drive_eff_mV'], marker='o', label=f'{scenario} drive')
    ax.set_xscale('log')
    ax.set_xlabel('Al shielding thickness (mm)')
    ax.set_ylabel('Effective drive term (mV equivalent) (Research Prototype)')
    ax.set_title('Bioenergetic drive entering the neural model (Research Prototype)')
    ax.legend()
    ax.grid(True, which='both', alpha=0.3)
    fig.tight_layout()
    fig.savefig(fig_dir / 'effective_drive_vs_shielding.png', dpi=200)
    plt.close(fig)

    # 4. Raster examples
    def plot_raster(result, fname, title):
        fig, ax = plt.subplots(figsize=(8, 4))
        st = result['spike_times_ms']
        sn = result['spike_neurons']
        if len(st) > 0:
            ax.scatter(st, sn, s=2)
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Neuron index')
        ax.set_title(title + ' (Research Prototype)')
        fig.tight_layout()
        fig.savefig(fig_dir / fname, dpi=200)
        plt.close(fig)

    # 5. Voltage trace examples
    def plot_voltage(result, fname, title):
        fig, ax = plt.subplots(figsize=(8, 4))
        t = result['trace_time_ms']
        traces = result['voltage_traces_mV']
        for i in range(traces.shape[1]):
            ax.plot(t, traces[:, i], linewidth=0.8, alpha=0.8)
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Membrane potential (mV)')
        ax.set_title(title + ' (Research Prototype)')
        fig.tight_layout()
        fig.savefig(fig_dir / fname, dpi=200)
        plt.close(fig)

    # Plot Control, LEO 10mm and VAB 10mm
    if 'Healthy_control_no_radiation' in example_results:
        plot_raster(example_results['Healthy_control_no_radiation'], 'raster_healthy_control.png', 'Raster: healthy control')
        plot_voltage(example_results['Healthy_control_no_radiation'], 'voltage_healthy_control.png', 'Voltage traces: healthy control')
        
    for scenario in ['LEO_ISS_like', 'VAB_RBSP_like']:
        if scenario in example_results:
            plot_raster(example_results[scenario], f'raster_{scenario}_10mm.png', f'Raster: {scenario}, 10 mm Al, day 180')
            plot_voltage(example_results[scenario], f'voltage_{scenario}_10mm.png', f'Voltage traces: {scenario}, 10 mm Al, day 180')
