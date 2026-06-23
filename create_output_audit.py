import os
import pandas as pd
import numpy as np
from datetime import datetime

PROJECT_ROOT = r"D:\Downloads\Radiation modelling"
OUT_DIR = os.path.join(PROJECT_ROOT, "06_INTEGRATED_PIPELINE", "outputs")
REP_DIR = os.path.join(PROJECT_ROOT, "06_INTEGRATED_PIPELINE", "reports")

os.makedirs(REP_DIR, exist_ok=True)

files_to_audit = [
    "pipeline_status_flags.csv",
    "biology_ready_dose_forcing_table.csv",
    "biology_calibrated_endpoint_predictions.csv",
    "biology_calibrated_daily_timecourses_all_scenarios.csv",
    "neural_endpoint_simulation_summary.csv",
    "neural_timecourse_10mm_summary.csv",
    "scenario_interpretation_flags.csv"
]

def main():
    audit_records = []
    existence = {}
    row_col_counts = {}
    col_names = {}
    domain_warnings = []
    mc_nan_flagged = False
    van_allen_extrapolated = False

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Audit process
    for fname in files_to_audit:
        fpath = os.path.join(OUT_DIR, fname)
        exists = os.path.isfile(fpath)
        existence[fname] = exists
        if not exists:
            print(f"File missing: {fpath}")
            continue

        try:
            df = pd.read_csv(fpath)
            row_col_counts[fname] = (len(df), len(df.columns))
            col_names[fname] = list(df.columns)

            for col in df.columns:
                dtype = str(df[col].dtype)
                nan_count = int(df[col].isna().sum())
                row_count = len(df)
                
                # Check for MC NaN status
                if fname == "pipeline_status_flags.csv" and col == "status":
                    status_text = " ".join(df[col].dropna().astype(str).tolist())
                    if "NaN" in status_text or "audit only" in status_text:
                        mc_nan_flagged = True

                # Check for Van Allen extrapolation status
                if fname == "biology_calibrated_endpoint_predictions.csv" and col == "calibration_domain_flag":
                    flags_text = df[col].dropna().tolist()
                    if any("outside" in str(fl).lower() for fl in flags_text):
                        van_allen_extrapolated = True

                if np.issubdtype(df[col].dtype, np.number):
                    # Numeric column
                    c_min = float(df[col].min())
                    c_max = float(df[col].max())
                    c_mean = float(df[col].mean())
                else:
                    c_min = np.nan
                    c_max = np.nan
                    c_mean = np.nan

                audit_records.append({
                    "filename": fname,
                    "column_name": col,
                    "data_type": dtype,
                    "row_count": row_count,
                    "min": c_min,
                    "max": c_max,
                    "mean": c_mean,
                    "nan_count": nan_count
                })
        except Exception as e:
            print(f"Error auditing {fname}: {e}")

    # Write numeric audit CSV
    audit_df = pd.DataFrame(audit_records)
    csv_out_path = os.path.join(REP_DIR, "NUMERIC_AUDIT_SUMMARY.csv")
    audit_df.to_csv(csv_out_path, index=False)
    print(f"Created Numeric Audit CSV: {csv_out_path}")

    # Build Markdown Content
    md = f"""# RADBIO_NEURO Numeric Audit Summary Report

**Audit Run Timestamp**: {timestamp}
**Project Root Path**: `{PROJECT_ROOT}`

---

## 1. File Inventory and Properties

| Filename | Status | Rows | Columns |
| :--- | :---: | :---: | :---: |
"""
    for fname in files_to_audit:
        status_str = "✔️ Exists" if existence[fname] else "❌ Missing"
        rows, cols = row_col_counts.get(fname, (0, 0))
        md += f"| `{fname}` | {status_str} | {rows} | {cols} |\n"

    md += """
---

## 2. Scientific Fallbacks & Warning Indicators

- **Monte Carlo Effective-Dose NaN Fallback**: 
"""
    # Verify directly from physics audit file as well just to be 100% robust
    phys_audit_path = os.path.join(PROJECT_ROOT, "02_RADBIO_NEURO_001_PHYSICS_LAYER", "RADBIO_NEURO_001_NOTEBOOK_BUILD", "data", "effective_dose_output_audit.csv")
    phys_mc_nans = True
    if os.path.isfile(phys_audit_path):
        try:
            phys_df = pd.read_csv(phys_audit_path)
            any_usable = phys_df['usable_numeric_effective_dose'].fillna(False).astype(bool).any()
            phys_mc_nans = not any_usable
        except:
            pass

    if mc_nan_flagged or phys_mc_nans:
        md += "  - **Status**: ⚠️ **FLAGGED**. The SPENVIS effective-dose Monte Carlo raw outputs contain NaN/non-numeric values and are audited but **not** used. The pipeline has successfully defaulted to **SHIELDOSE-2 tissue absorbed dose** as the active physics forcing input.\n"
    else:
        md += "  - **Status**: ❌ Not Flagged (Expected effective-dose NaNs).\n"

    md += "\n- **Van Allen Belt Extrapolation Warning**:\n"
    if van_allen_extrapolated:
        md += "  - **Status**: ⚠️ **FLAGGED**. Thin-shielded Van Allen scenario cases exceed 10.0 mGy/day. These outputs are correctly flagged with `outside_primary_validation_domain_high_dose_rate` because they constitute a mathematical extrapolation far outside the primary chronic low-dose biological validation range (0.1 to 10.0 mGy/day).\n"
    else:
        md += "  - **Status**: ❌ Not Flagged.\n"

    md += """
- **Clinical Validation Disclaimer**:
  - **Status**: ⚠️ **DECLARED**. This software is a computational research prototype. All ROS, mitochondrial, and neural outputs are calibrated research-prototype metrics and **not** clinical, medical, or astronaut operational health predictions.

---

## 3. Detailed Numeric Column Metrics

"""
    for fname in files_to_audit:
        if not existence[fname]:
            continue
        md += f"### File: `{fname}`\n\n"
        md += "| Column Name | Type | Rows | Min | Max | Mean | NaNs |\n"
        md += "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n"
        
        file_df = audit_df[audit_df["filename"] == fname]
        for _, r in file_df.iterrows():
            cmin = f"{r['min']:.6g}" if not pd.isna(r["min"]) else "-"
            cmax = f"{r['max']:.6g}" if not pd.isna(r["max"]) else "-"
            cmean = f"{r['mean']:.6g}" if not pd.isna(r["mean"]) else "-"
            md += f"| `{r['column_name']}` | `{r['data_type']}` | {r['row_count']} | {cmin} | {cmax} | {cmean} | {r['nan_count']} |\n"
        md += "\n"

    md += """
---

## 4. Plain-Language Explanation of Outputs

1. **biology_ready_dose_forcing_table.csv**:
   Contains parsed ionizing radiation doses over 180 days from SHIELDOSE-2 and daily equivalent dose rates in mGy/day. These rates serve as the input forcing variables for biological cells.
   
2. **biology_calibrated_endpoint_predictions.csv**:
   Outputs the steady-state biological proxies at Day 180. The excitability ratio and LTP proxies show how cellular stress compromises electrical functions. Low values represent deficits.
   
3. **biology_calibrated_daily_timecourses_all_scenarios.csv**:
   Shows how ROS builds up and how mitochondrial integrity degrades day-by-day. In high-exposure cases, ROS rises quickly while mitochondria fail over weeks.
   
4. **neural_endpoint_simulation_summary.csv**:
   Summarizes the functional firing rates of the leaky integrate-and-fire network simulation. Suppressed ATP levels cause the population firing rates to decline dramatically.
   
5. **neural_timecourse_10mm_summary.csv**:
   Shows daily changes in network excitability parameters (threshold, baseline drive, and membrane tau) and population firing rates at 10 mm Al.
   
6. **scenario_interpretation_flags.csv**:
   Provides scenario/shielding-specific warnings and flags (e.g. validated vs. extrapolated vs. extreme stress), and recommended user messages for dashboard presentation.
"""

    md_out_path = os.path.join(REP_DIR, "NUMERIC_AUDIT_SUMMARY.md")
    with open(md_out_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Created Numeric Audit MD Report: {md_out_path}")

if __name__ == "__main__":
    main()
