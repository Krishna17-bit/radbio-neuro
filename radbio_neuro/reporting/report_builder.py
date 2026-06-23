import os
from pathlib import Path
import pandas as pd

def build_reports(
    forcing_df: pd.DataFrame,
    biology_endpoints: pd.DataFrame,
    neural_endpoints: pd.DataFrame,
    report_dir: Path
):
    """Generate integrated HTML and Markdown report summaries."""
    report_dir.mkdir(exist_ok=True, parents=True)
    
    # 1. Prepare HTML Tables
    dose_rate_summary = forcing_df[forcing_df['shield_mm_Al'].isin([1, 2, 5, 10, 20])].copy()
    
    # Create HTML table for dose rate summary
    dose_rate_html = dose_rate_summary[[
        'scenario', 'shield_mm_Al', 'total_dose_Gy', 'total_dose_rate_mGy_day', 'forcing_regime_label'
    ]].to_html(classes='dataframe table table-striped', index=False)
    
    # Create HTML table for biology endpoints
    bio_endpoints_html = biology_endpoints[biology_endpoints['shield_mm_Al'].isin([1, 2, 5, 10, 20])][[
        'scenario', 'shield_mm_Al', 'ros_norm_day_end', 'mito_integrity_day_end', 'atp_proxy_day_end', 'calibration_domain_flag'
    ]].to_html(classes='dataframe table table-striped', index=False)
    
    # Create HTML table for neural endpoints
    neural_endpoints_html = neural_endpoints[[
        'scenario', 'shield_mm_Al', 'mean_firing_rate_hz', 'tau_eff_ms', 'v_threshold_eff_mV', 'drive_eff_mV'
    ]].to_html(classes='dataframe table table-striped', index=False)

    # 2. Build Markdown content
    md_content = f"""# RADBIO_NEURO Integrated Pipeline Summary Report

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
"""
    for _, r in dose_rate_summary.iterrows():
        md_content += f"| {r['scenario']} | {r['shield_mm_Al']} | {r['total_dose_Gy']:.4f} | {r['total_dose_rate_mGy_day']:.4f} | {r['forcing_regime_label']} |\n"

    md_content += f"""
---

## 4. Biological Calibration Layer Outputs
*The ROS/mitochondria model is a calibration scaffold with literature anchors (Acharya et al., 2019), not complete experimental validation. Note: ROS burden index is a dimensionless ROS accumulation metric, not a bounded 0-1 value.*

### Endpoint Biology Metrics (Day 180)
| Scenario | Shielding (mm Al) | ROS Burden Index | Mito Integrity | ATP Proxy | Domain Flag |
| :--- | :---: | :---: | :---: | :---: | :---: |
"""
    for _, r in biology_endpoints[biology_endpoints['shield_mm_Al'].isin([1, 2, 5, 10, 20])].iterrows():
        md_content += f"| {r['scenario']} | {r['shield_mm_Al']} | {r['ros_norm_day_end']:.4f} | {r['mito_integrity_day_end']:.4f} | {r['atp_proxy_day_end']:.4f} | {r['calibration_domain_flag']} |\n"

    md_content += f"""
---

## 5. Neural Simulation Layer Outputs
*The LIF neural simulation layer simulates functional network excitability under mapped bioenergetic constraints.*

### Endpoint Neural Metrics (Day 180)
| Scenario | Shielding (mm Al) | Firing Rate (Hz) | tau_eff (ms) | V_threshold (mV) | Drive (mV) |
| :--- | :---: | :---: | :---: | :---: | :---: |
"""
    for _, r in neural_endpoints.iterrows():
        md_content += f"| {r['scenario']} | {r['shield_mm_Al']} | {r['mean_firing_rate_hz']:.2f} | {r['tau_eff_ms']:.2f} | {r['v_threshold_eff_mV']:.2f} | {r['drive_eff_mV']:.2f} |\n"

    md_content += """
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
"""

    with open(report_dir / "RADBIO_NEURO_integrated_summary.md", "w", encoding="utf-8") as f:
        f.write(md_content)

    # 3. Build HTML content (with Premium CSS styling & Glassmorphism)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RADBIO_NEURO Integrated Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0b0f19;
            --card-bg: rgba(22, 28, 45, 0.6);
            --border-color: rgba(255, 255, 255, 0.08);
            --primary: #3b82f6;
            --accent: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
        }}
        
        body {{
            background: linear-gradient(135deg, #090d16 0%, #151c30 100%);
            color: var(--text-main);
            font-family: 'Outfit', sans-serif;
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }}
        
        header {{
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            padding: 2.5rem 5%;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        h1 {{
            font-size: 2.2rem;
            font-weight: 800;
            margin: 0 0 0.5rem 0;
            background: linear-gradient(90deg, #60a5fa, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .disclaimer-banner {{
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid var(--danger);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 2rem;
            color: #fca5a5;
            font-weight: 600;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 3rem auto;
            padding: 0 1.5rem;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2.5rem;
            margin-bottom: 3rem;
        }}
        
        @media (max-width: 900px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .card {{
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            transition: transform 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
        }}
        
        h2 {{
            color: var(--primary);
            font-size: 1.5rem;
            margin-top: 0;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        h3 {{
            color: var(--accent);
            font-size: 1.2rem;
        }}
        
        table.dataframe {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
        }}
        
        table.dataframe th, table.dataframe td {{
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }}
        
        table.dataframe th {{
            background: rgba(59, 130, 246, 0.1);
            color: var(--text-main);
            font-weight: 600;
        }}
        
        table.dataframe tr:hover {{
            background: rgba(255,255,255,0.03);
        }}
        
        .img-box {{
            background: rgba(0,0,0,0.2);
            border-radius: 12px;
            padding: 0.5rem;
            border: 1px solid var(--border-color);
            margin: 1.5rem 0;
            text-align: center;
        }}
        
        .img-box img {{
            max-width: 100%;
            border-radius: 8px;
        }}
        
        .warning-box {{
            background: rgba(245, 158, 11, 0.1);
            border-left: 4px solid var(--warning);
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
            color: #fde047;
        }}
    </style>
</head>
<body>
    <header>
        <h1>RADBIO_NEURO Modelling Report</h1>
        <p style="color: var(--text-muted); margin: 0;">Automated pipeline run results & diagnostic verification summaries</p>
    </header>
    
    <div class="container">
        <div class="disclaimer-banner">
            ⚠️ WARNING: Research prototype only. Not for medical, operational, or astronaut health decision-making. No clinical diagnostic claims are validated.
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>1. Environment & Physics Layer <span style="font-size:0.8rem; color:var(--text-muted)">RADBIO_NEURO_001</span></h2>
                <p>The SPENVIS effective-dose Monte Carlo results contain non-numeric NaN values. To prevent erroneous biological projections, the pipeline automatically falls back to <strong>SHIELDOSE-2 tissue absorbed dose</strong> rates.</p>
                <div class="warning-box">
                    <strong>Physics Audit Status:</strong> Monte Carlo Sv data is marked UNUSABLE. Fallback absorbed dose is currently active.
                </div>
                <h3>Absorbed Dose Summary Table</h3>
                {dose_rate_html}
            </div>
            
            <div class="card">
                <h2>2. Radiation Dose vs Shielding Depth</h2>
                <div class="img-box">
                    <img src="../figures/dose_vs_shielding_total_Gy_log.png" alt="Dose vs Shielding Depth">
                </div>
                <div class="img-box">
                    <img src="../figures/biology_ready_dose_rate_vs_shielding_mGy_day.png" alt="Dose Rate vs Shielding">
                </div>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>3. Biological Calibration Scaffold <span style="font-size:0.8rem; color:var(--text-muted)">RADBIO_NEURO_002</span></h2>
                <p>The model simulates daily ROS burden index (dimensionless indicator of ROS level, not a bounded 0-1 normalized value), mitochondrial integrity, and ATP levels. It splits acute redox effects from slow bioenergetic decay, fit to literature chronic low-dose benchmarks.</p>
                <h3>Endpoint Cellular Predictions (Day 180)</h3>
                {bio_endpoints_html}
                <div class="warning-box">
                    <strong>Calibration Domain Notice:</strong> Orbits crossing the radiation belts (VAB) generate dose-rates (>100 mGy/day) far exceeding the chronic validation bounds (~1 mGy/day). These projections are labeled extrapolations.
                </div>
            </div>
            
            <div class="card">
                <h2>4. Biological Response Figures</h2>
                <div class="img-box">
                    <img src="../figures/mito_integrity_vs_shielding.png" alt="Mito Integrity vs Shielding">
                </div>
                <div class="img-box">
                    <img src="../figures/timecourse_ros_10mm.png" alt="ROS Timecourse at 10mm">
                </div>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h2>5. Functional Neural Simulation <span style="font-size:0.8rem; color:var(--text-muted)">RADBIO_NEURO_003</span></h2>
                <p>Cellular ATP and ROS endpoints are mapped to network parameters in a stochastic Leaky Integrate-and-Fire population of 80 neurons. Bioenergetic drive is suppressed by ATP loss, while membrane properties adapt dynamically.</p>
                <h3>Endpoint Population Firing Results</h3>
                {neural_endpoints_html}
            </div>
            
            <div class="card">
                <h2>6. Neural Simulation Firing Results</h2>
                <div class="img-box">
                    <img src="../figures/endpoint_firing_rate_vs_shielding.png" alt="Endpoint Firing Rate vs Shielding">
                </div>
                <div class="img-box">
                    <img src="../figures/raster_VAB_RBSP_like_10mm.png" alt="Raster VAB at 10mm">
                </div>
            </div>
        </div>
        
        <div class="card" style="margin-top: 3rem;">
            <h2>7. Scientific Limitations & Actionable Next Steps</h2>
            <ul>
                <li><strong>No clinical diagnosis or medical validity:</strong> This prototype is a research-prototype model, not a medical, clinical, astronaut-health, or mission-operation prediction. Do not use for health diagnostics.</li>
                <li><strong>Monte Carlo Sievert:</strong> Effective-dose Monte Carlo produced NaN values and was audited but not used for biology input. Models must be rerun with fixed parameters to obtain actual high-LET radiation quality equivalent factors. SHIELDOSE-2 tissue absorbed dose is the active physics input.</li>
                <li><strong>Calibration limitations:</strong> Chronic space radiation biology studies are sparse; model fitting is anchored to only two mouse endpoints. Thin-shielded Van Allen cases are extrapolation outside the primary chronic low-dose validation domain.</li>
                <li><strong>Validation extension:</strong> Collect and digitize more mouse and cell experimental papers to anchor model constants in multiple tissues.</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

    with open(report_dir / "RADBIO_NEURO_integrated_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Generated integrated HTML report at {report_dir / 'RADBIO_NEURO_integrated_report.html'}")
    print(f"Generated integrated summary MD report at {report_dir / 'RADBIO_NEURO_integrated_summary.md'}")
