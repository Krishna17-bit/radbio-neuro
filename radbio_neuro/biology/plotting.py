import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

def plot_biology_results(fit_df: pd.DataFrame, predictions: pd.DataFrame, timecourses: pd.DataFrame, fig_dir: Path):
    """Plot biological calibration fits and endpoints."""
    fig_dir.mkdir(exist_ok=True, parents=True)
    
    # 1. Model vs targets
    fig, ax = plt.subplots(figsize=(10, 5))
    fit_df.plot(x='target_id', y=['target_ratio_to_control', 'model_prediction'], kind='bar', ax=ax)
    ax.set_ylabel('Ratio to control')
    ax.set_xlabel('Validation target')
    ax.set_title('Model vs current validation targets')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    fig.savefig(fig_dir / 'model_vs_validation_targets.png', dpi=200)
    plt.close(fig)

    # 2. Shielding metrics (mito_integrity, excitability, ltp) vs shielding depth
    sel = predictions[predictions['shield_mm_Al'].isin([1, 2, 5, 10, 20])]
    for metric, ylabel, fname in [
        ('mito_integrity_day_end', 'Mitochondrial integrity index at day 180 (Research Prototype)', 'mito_integrity_vs_shielding.png'),
        ('excitability_ratio_day_end', 'Excitability ratio at day 180 (Research Prototype)', 'excitability_vs_shielding.png'),
        ('ltp_proxy_day_end', 'LTP-like synaptic function proxy at day 180 (Research Prototype)', 'ltp_proxy_vs_shielding.png'),
    ]:
        pivot = sel.pivot(index='shield_mm_Al', columns='scenario', values=metric).sort_index()
        fig, ax = plt.subplots(figsize=(8, 5))
        pivot.plot(marker='o', ax=ax)
        ax.set_xscale('log')
        ax.set_xlabel('Al shielding depth (mm)')
        ax.set_ylabel(ylabel)
        ax.set_title(ylabel + ' vs shielding')
        plt.tight_layout()
        fig.savefig(fig_dir / fname, dpi=200)
        plt.close(fig)

    # 3. Timecourses at 10 mm Al
    subset = timecourses[timecourses['shield_mm_Al'].round(6).eq(10.0)]
    for metric, ylabel, fname in [
        ('ros_norm', 'ROS burden index (Research Prototype)', 'timecourse_ros_10mm.png'),
        ('mito_integrity', 'Mitochondrial integrity index (Research Prototype)', 'timecourse_mito_10mm.png'),
        ('excitability_ratio', 'Excitability ratio (Research Prototype)', 'timecourse_excitability_10mm.png'),
    ]:
        fig, ax = plt.subplots(figsize=(8, 5))
        for scenario, grp in subset.groupby('scenario'):
            ax.plot(grp['day'], grp[metric], label=scenario)
        ax.set_xlabel('Mission day')
        ax.set_ylabel(ylabel)
        ax.set_title(ylabel + ' timecourse at 10 mm Al')
        ax.legend()
        plt.tight_layout()
        fig.savefig(fig_dir / fname, dpi=200)
        plt.close(fig)
