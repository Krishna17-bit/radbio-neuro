import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

def plot_dose_curves(dose_df: pd.DataFrame, forcing_df: pd.DataFrame, fig_dir: Path):
    """Plot dose and dose-rate relationships vs shielding depth."""
    fig_dir.mkdir(exist_ok=True, parents=True)
    
    # 1. Dose vs Shielding Total Gy
    fig, ax = plt.subplots(figsize=(8, 5))
    for scenario, g in dose_df.groupby('scenario'):
        g = g.sort_values('shield_mm_Al')
        ax.plot(g['shield_mm_Al'], g['total_dose_Gy'], marker='o', label=scenario)
    ax.set_yscale('log')
    ax.set_xlabel('Al shielding depth (mm)')
    ax.set_ylabel('Total absorbed tissue dose over 180 days (Gy)')
    ax.set_title('SPENVIS SHIELDOSE-2 tissue dose vs shielding')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(fig_dir / 'dose_vs_shielding_total_Gy_log.png', dpi=220)
    plt.close(fig)

    # 2. Dose-rate vs Shielding mGy/day
    fig, ax = plt.subplots(figsize=(8, 5))
    for scenario, g in forcing_df.groupby('scenario'):
        g = g.sort_values('shield_mm_Al')
        ax.plot(g['shield_mm_Al'], g['total_dose_rate_mGy_day'], marker='o', label=scenario)
    ax.set_yscale('log')
    ax.set_xlabel('Al shielding depth (mm)')
    ax.set_ylabel('Absorbed tissue dose rate (mGy/day)')
    ax.set_title('Biology-ready absorbed dose-rate input')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(fig_dir / 'biology_ready_dose_rate_vs_shielding_mGy_day.png', dpi=220)
    plt.close(fig)
