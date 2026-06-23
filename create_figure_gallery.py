import os
from datetime import datetime

PROJECT_ROOT = r"D:\Downloads\Radiation modelling"
FIG_DIR = os.path.join(PROJECT_ROOT, "06_INTEGRATED_PIPELINE", "figures")
REP_DIR = os.path.join(PROJECT_ROOT, "06_INTEGRATED_PIPELINE", "reports")

os.makedirs(REP_DIR, exist_ok=True)

def get_category(filename):
    fn = filename.lower()
    if "validation" in fn or "target" in fn or "flag" in fn:
        return "validation / flags"
    elif "raster" in fn or "voltage" in fn or "firing" in fn or "drive" in fn:
        return "neural / raster / voltage"
    elif "ros" in fn or "mito" in fn or "excitability" in fn or "ltp" in fn:
        return "biology / ROS / mitochondria"
    elif "dose" in fn or "shielding" in fn:
        return "dose / shielding"
    return "other"

def get_description(filename):
    fn = filename.lower()
    if "dose_vs_shielding" in fn:
        return "Total absorbed tissue dose (Gy) over 180 days across all shielding depths."
    elif "dose_rate" in fn or "forcing" in fn:
        return "Biology-ready absorbed tissue dose-rate forcing (mGy/day) across shielding depths."
    elif "model_vs_validation" in fn:
        return "Model predictions compared against experimental/literature validation anchors."
    elif "mito_integrity_vs_shielding" in fn:
        return "Endpoint mitochondrial integrity proxy (Day 180) vs shielding thickness."
    elif "excitability_vs_shielding" in fn:
        return "Endpoint neural excitability ratio (Day 180) vs shielding thickness."
    elif "ltp_proxy_vs_shielding" in fn:
        return "Endpoint long-term potentiation (LTP) ratio (Day 180) vs shielding thickness."
    elif "timecourse_ros" in fn:
        return "ROS daily accumulation timecourse over 180 days at 10 mm Al."
    elif "timecourse_mito" in fn:
        return "Mitochondrial integrity daily damage/repair timecourse at 10 mm Al."
    elif "timecourse_excitability" in fn:
        return "Excitability ratio daily changes timecourse at 10 mm Al."
    elif "firing_rate_vs_shielding" in fn:
        return "Endpoint mean neural network population firing rate (Hz) vs shielding thickness."
    elif "timecourse_firing" in fn:
        return "Neural network population firing rate (Hz) sampled timecourse at 10 mm Al."
    elif "effective_drive" in fn:
        return "Bioenergetic voltage drive entering integrate-and-fire model vs shielding thickness."
    elif "raster_healthy" in fn:
        return "Spike raster plot for unexposed healthy control neural network."
    elif "raster_leo" in fn:
        return "Spike raster plot for LEO ISS-like scenario at 10 mm Al shielding."
    elif "raster_vab" in fn:
        return "Spike raster plot for extreme Van Allen Belt scenario at 10 mm Al shielding."
    elif "voltage_healthy" in fn:
        return "Membrane potential voltage traces for healthy control neural population."
    elif "voltage_leo" in fn:
        return "Membrane potential voltage traces for LEO scenario at 10 mm Al."
    elif "voltage_vab" in fn:
        return "Membrane potential voltage traces for Van Allen Belt scenario at 10 mm Al."
    return "Visual result figure from the radiation modelling pipeline."

def main():
    if not os.path.exists(FIG_DIR):
        print(f"Figures directory not found: {FIG_DIR}")
        return

    png_files = sorted([f for f in os.listdir(FIG_DIR) if f.lower().endswith(".png")])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. HTML Gallery
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RADBIO_NEURO Figure Gallery</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #f3f4f6;
            --card-bg: #ffffff;
            --text: #111827;
            --text-muted: #6b7280;
            --primary: #3b82f6;
            --border: #e5e7eb;
            --badge-dose: #3b82f6;
            --badge-bio: #10b981;
            --badge-neural: #8b5cf6;
            --badge-val: #f59e0b;
        }}
        body {{
            background-color: var(--bg);
            color: var(--text);
            font-family: 'Outfit', sans-serif;
            margin: 0;
            padding: 0;
        }}
        header {{
            background: #ffffff;
            border-bottom: 1px solid var(--border);
            padding: 2rem 5%;
            margin-bottom: 2rem;
        }}
        h1 {{
            margin: 0;
            font-weight: 800;
            font-size: 2rem;
            color: #1f2937;
        }}
        .meta {{
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 0.5rem;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem 3rem 1.5rem;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
        }}
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
        }}
        .card-content {{
            padding: 1.25rem;
        }}
        .card-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin: 0 0 0.5rem 0;
            word-break: break-all;
        }}
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.6rem;
            font-size: 0.75rem;
            font-weight: 600;
            border-radius: 9999px;
            color: #ffffff;
            margin-bottom: 0.75rem;
        }}
        .badge-dose {{ background-color: var(--badge-dose); }}
        .badge-bio {{ background-color: var(--badge-bio); }}
        .badge-neural {{ background-color: var(--badge-neural); }}
        .badge-val {{ background-color: var(--badge-val); }}
        .img-container {{
            width: 100%;
            background: #f9fafb;
            border-bottom: 1px solid var(--border);
            text-align: center;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }}
        .desc {{
            font-size: 0.875rem;
            color: var(--text-muted);
            margin: 0.5rem 0 0 0;
            line-height: 1.4;
        }}
    </style>
</head>
<body>
    <header>
        <h1>RADBIO_NEURO Figure Gallery</h1>
        <div class="meta">
            <strong>Project Folder:</strong> {PROJECT_ROOT}<br>
            <strong>Total Figures:</strong> {len(png_files)} | 
            <strong>Generated:</strong> {timestamp}
        </div>
    </header>
    <div class="container">
        <div style="background: rgba(59, 130, 246, 0.1); border-left: 4px solid var(--primary); padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; line-height: 1.6;">
            <h2 style="margin-top: 0; font-size: 1.25rem; color: var(--primary); font-weight: 600;">📊 Gallery Scientific Interpretation Overview</h2>
            <ul style="margin: 0.5rem 0 0 0; padding-left: 1.25rem; font-size: 0.95rem; color: #374151;">
                <li style="margin-bottom: 0.5rem;"><strong>LEO ISS-like Orbit</strong>: Shows a clear, shielding-dependent dose reduction. At deeper shielding depths (e.g. 10 mm Al), modeled cell ROS burden remains low, partial preservation of mitochondrial integrity is achieved, and active population firing rates are preserved.</li>
                <li style="margin-bottom: 0.5rem;"><strong>Van Allen Belt Crossing (VAB)</strong>: Involves extreme, high dose-rate forcing. Behind thin shielding (1 mm or 2 mm Al), complete cellular and network collapse occurs, with modeled ATP depletion shutting down firing.</li>
                <li style="margin-bottom: 0.5rem;"><strong>Blank VAB Raster Plots</strong>: A blank raster represents zero or near-zero population firing under severe extrapolated bioenergetic stress (metabolic shutdown), not missing or broken plot data.</li>
                <li style="margin-bottom: 0;"><strong>Effective-Dose MC NaN Fallback</strong>: SPENVIS effective-dose Monte Carlo raw files were audited but not used in the pipeline because outputs were non-numeric (NaN). The active physics forcing relies on SHIELDOSE-2 tissue absorbed dose.</li>
            </ul>
        </div>
        <div class="grid">
"""

    for filename in png_files:
        cat = get_category(filename)
        desc = get_description(filename)
        badge_class = "badge-dose"
        if "biology" in cat:
            badge_class = "badge-bio"
        elif "neural" in cat:
            badge_class = "badge-neural"
        elif "validation" in cat:
            badge_class = "badge-val"

        rel_path = f"../figures/{filename}"
        html_content += f"""
            <div class="card">
                <div class="img-container">
                    <img src="{rel_path}" alt="{filename}">
                </div>
                <div class="card-content">
                    <span class="badge {badge_class}">{cat}</span>
                    <h2 class="card-title">{filename}</h2>
                    <p class="desc">{desc}</p>
                </div>
            </div>
"""

    html_content += """
        </div>
    </div>
</body>
</html>
"""

    # Write HTML Gallery
    html_file = os.path.join(REP_DIR, "FIGURE_GALLERY.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Created HTML figure gallery: {html_file}")

    # 2. Markdown Index
    md_content = f"""# RADBIO_NEURO Figure Index

**Total Figures**: {len(png_files)}
**Generation Timestamp**: {timestamp}
**Project Folder**: `{PROJECT_ROOT}`

---

## Figures List

"""
    for filename in png_files:
        cat = get_category(filename)
        desc = get_description(filename)
        rel_path = f"../figures/{filename}"
        md_content += f"""### [{filename}]({rel_path})
- **Category**: `{cat}`
- **Description**: {desc}

"""

    md_file = os.path.join(REP_DIR, "FIGURE_INDEX.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Created Markdown figure index: {md_file}")

if __name__ == "__main__":
    main()
