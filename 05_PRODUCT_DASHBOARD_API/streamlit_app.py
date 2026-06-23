import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Set premium layout configuration
st.set_page_config(
    page_title="RADBIO_NEURO Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme styling adjustments via markdown injection
st.markdown("""
<style>
    .reportview-container {
        background: #0b0f19;
    }
    .main .block-container {
        padding-top: 1.5rem;
    }
    .metric-card {
        background: rgba(22, 28, 45, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .warning-banner {
        background-color: rgba(239, 68, 68, 0.15);
        color: #fca5a5;
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        text-align: center;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# STRENGTHENED WARNING BANNER
st.markdown(
    """<div class="warning-banner">
        ⚠️ <strong>RESEARCH PROTOTYPE DISCLAIMER</strong>: ROS, mitochondrial, and neural outputs are calibrated research-prototype metrics, not medical, clinical, astronaut-health, or mission-operation predictions. <br>
        • Effective-dose Monte Carlo files produced NaN and are not used for biology input.<br>
        • SHIELDOSE-2 tissue absorbed dose is the active physics forcing input.<br>
        • Thin-shielded Van Allen Belt (VAB) cases represent extreme extrapolation outside the primary chronic low-dose validation range.
    </div>""",
    unsafe_allow_html=True
)

# Resolve paths
BASE_DIR = Path(__file__).resolve().parent.parent
INT_OUT_DIR = BASE_DIR / "06_INTEGRATED_PIPELINE" / "outputs"
INT_FIG_DIR = BASE_DIR / "06_INTEGRATED_PIPELINE" / "figures"
INT_REP_DIR = BASE_DIR / "06_INTEGRATED_PIPELINE" / "reports"

@st.cache_data
def load_data():
    try:
        forcing = pd.read_csv(INT_OUT_DIR / "biology_ready_dose_forcing_table.csv")
        bio_pred = pd.read_csv(INT_OUT_DIR / "biology_calibrated_endpoint_predictions.csv")
        bio_daily = pd.read_csv(INT_OUT_DIR / "biology_calibrated_daily_timecourses_all_scenarios.csv")
        neural_endpoints = pd.read_csv(INT_OUT_DIR / "neural_endpoint_simulation_summary.csv")
        neural_daily = pd.read_csv(INT_OUT_DIR / "neural_timecourse_10mm_summary.csv")
        control = pd.read_csv(INT_OUT_DIR / "healthy_control_neural_summary.csv")
        status = pd.read_csv(INT_OUT_DIR / "pipeline_status_flags.csv")
        interp_flags = pd.read_csv(INT_OUT_DIR / "scenario_interpretation_flags.csv")
        return forcing, bio_pred, bio_daily, neural_endpoints, neural_daily, control, status, interp_flags
    except Exception as e:
        st.error(f"Error loading pipeline outputs: {e}. Please run the pipeline first.")
        return None, None, None, None, None, None, None, None

forcing, bio_pred, bio_daily, neural_endpoints, neural_daily, control, status, interp_flags = load_data()

# SIDEBAR OPTIONS
st.sidebar.title("🧬 Parameter Controls")
if forcing is not None and interp_flags is not None:
    # Scenario selection
    scenario_options = sorted(list(forcing['scenario'].unique()))
    scenario = st.sidebar.selectbox("Select Scenario", scenario_options)
    
    # Shielding depth selection
    shield_options = sorted(list(forcing['shield_mm_Al'].unique()))
    shield_val = st.sidebar.selectbox("Select Shielding Depth (mm Al)", shield_options)

    # Filter data based on selections
    forcing_row = forcing[(forcing['scenario'] == scenario) & (forcing['shield_mm_Al'] == shield_val)].iloc[0]
    bio_row = bio_pred[(bio_pred['scenario'] == scenario) & (bio_pred['shield_mm_Al'] == shield_val)].iloc[0]
    interp_row = interp_flags[(interp_flags['scenario'] == scenario) & (interp_flags['shield_mm_Al'] == shield_val)].iloc[0]
    
    # Handle matching neural row (endpoint may not exist for all sub-shieldings, fall back to nearest)
    neural_sub = neural_endpoints[(neural_endpoints['scenario'] == scenario) & (neural_endpoints['shield_mm_Al'] == shield_val)]
    if not neural_sub.empty:
        neural_row = neural_sub.iloc[0]
    else:
        # Fall back to closest shield in neural endpoints
        closest_idx = (neural_endpoints['shield_mm_Al'] - shield_val).abs().argmin()
        neural_row = neural_endpoints.iloc[closest_idx]
        st.sidebar.warning(f"Exact neural simulation not available for {shield_val} mm Al. Showing nearest ({neural_row['shield_mm_Al']} mm Al).")

    # Display scenario/shielding-specific warnings at the top of the main screen
    st.subheader("🛡️ Real-Time Scientific Interpretation Flag")
    domain_flag = interp_row['calibration_domain_flag']
    interp_class = interp_row['interpretation_class']
    user_msg = interp_row['recommended_user_message']
    
    if "outside" in domain_flag or "extrapolation" in interp_class:
        st.warning(f"⚠️ **Domain Extrapolation ({interp_class})**: {user_msg}")
    else:
        st.success(f"✔️ **Validated Domain ({interp_class})**: {user_msg}")

# EXPLANATION PANEL
with st.expander("📚 Model Architecture & Key Explanations (Physics, Biology, Neural, Limitations)", expanded=False):
    st.markdown("""
    * **Physics Input Layer**: Uses **SHIELDOSE-2 tissue absorbed dose** rates. The raw SPENVIS effective-dose Monte Carlo outputs contained `NaN` values and were audited as unusable. The pipeline automatically falls back to tissue absorbed dose.
    * **Biology Model Layer**: Simulates daily ROS burden index, mitochondrial integrity index, and ATP proxy.
      * *Note on ROS*: ROS burden index is a dimensionless index representing cellular ROS levels, not a bounded 0–1 normalized value. It can grow logarithmically under extreme radiation forcing.
    * **Neural Simulation Layer**: Models a conductance-equivalent Leaky Integrate-and-Fire (LIF) network. Suppressed ATP levels scale down membrane driving current, elevate threshold levels, and reduce integration times. Under extreme belt stress, complete ATP depletion results in a **zero firing state** (blank raster), which indicates simulated metabolic shutdown rather than missing data.
    * **Extrapolation Caveat**: Chronic biological validation data is rare and focuses on low-dose rates (0.1–10 mGy/day). Thin-shielded VAB cases (>100 mGy/day) represent extreme extrapolation stress tests.
    """)

# TABS
tabs = st.tabs([
    "Project Overview", 
    "SPENVIS Physics Layer", 
    "Dose vs Shielding", 
    "Biology Calibration Layer", 
    "Neural Simulation Layer", 
    "Scientific Flags", 
    "Export Report"
])

# TAB 1: Project Overview
with tabs[0]:
    st.header("Project Overview")
    st.write(
        """
        This dashboard presents an interactive interface for the **Radiation-to-Biology-to-Neural-Risk Modelling Pipeline**.
        It simulates the downstream physiological risks of space radiation on neuro-excitability and bioenergetics.
        """
    )
    st.image(str(INT_FIG_DIR / "model_vs_validation_targets.png") if INT_FIG_DIR.exists() else [])
    
    st.markdown(
        """
        1. **Physics Layer**: Extracts mission ionizing dose (SHIELDOSE-2) and converts it to daily dose rates.
        2. **Biology Calibration**: Simulates daily ROS burden, mitochondrial damage, and ATP proxies, calibrated against literature targets.
        3. **Neural Simulation**: Computes leaky integrate-and-fire network firing rates under redox and bioenergetic stress.
        """
    )

# TAB 2: SPENVIS Physics Layer
with tabs[1]:
    st.header("SPENVIS Physics Layer")
    if forcing is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Selected Config Metrics")
            st.metric("Total Mission Dose (Gy)", f"{forcing_row['total_dose_Gy']:.4f}")
            st.metric("Daily Dose Rate (mGy/day)", f"{forcing_row['total_dose_rate_mGy_day']:.4f}")
            st.metric("Forcing Regime", forcing_row['forcing_regime_label'])
        with col2:
            st.subheader("Dose-Rate Decomposition")
            comp = {
                "Electrons": forcing_row['electron_dose_rate_mGy_day'],
                "Bremsstrahlung": forcing_row['brems_dose_rate_mGy_day'],
                "Trapped Protons": forcing_row['trapped_proton_dose_rate_mGy_day']
            }
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(comp.keys(), comp.values(), color=['#3b82f6', '#10b981', '#f59e0b'])
            ax.set_ylabel("mGy / day")
            ax.set_title("Forcing Dose-Rate Contributions")
            st.pyplot(fig)
            plt.close(fig)

# TAB 3: Dose vs Shielding
with tabs[2]:
    st.header("Dose vs Shielding")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Mission Absorbed Dose over Shielding")
        st.image(str(INT_FIG_DIR / "dose_vs_shielding_total_Gy_log.png"))
    with col2:
        st.subheader("Daily Dose-Rate Forcing over Shielding")
        st.image(str(INT_FIG_DIR / "biology_ready_dose_rate_vs_shielding_mGy_day.png"))

# TAB 4: Biology Calibration Layer
with tabs[3]:
    st.header("Biology Calibration Layer")
    if bio_daily is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Endpoint Biology Summary")
            st.metric("ROS Burden Index (Dimensionless)", f"{bio_row['ros_norm_day_end']:.4f}")
            st.metric("Mitochondrial Integrity Index (M_end)", f"{bio_row['mito_integrity_day_end']:.4f}")
            st.metric("ATP Proxy (ATP_end)", f"{bio_row['atp_proxy_day_end']:.4f}")
            st.metric("Excitability Ratio", f"{bio_row['excitability_ratio_day_end']:.4f}")
            st.caption("Note: ROS Burden Index is a dimensionless value, not a bounded 0-1 normalized index.")
            
        with col2:
            st.subheader("Daily Biological Timecourse (180 days)")
            daily_sub = bio_daily[(bio_daily['scenario'] == scenario) & (bio_daily['shield_mm_Al'] == shield_val)]
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(daily_sub['day'], daily_sub['ros_norm'], label="ROS Burden Index (Dimensionless)", color='#ef4444')
            ax.plot(daily_sub['day'], daily_sub['mito_integrity'], label="Mitochondria Integrity Index", color='#10b981')
            ax.plot(daily_sub['day'], daily_sub['atp_proxy'], label="ATP Proxy", color='#f59e0b', linestyle='--')
            ax.set_xlabel("Day")
            ax.set_ylabel("Metric Value / Index")
            ax.set_title(f"Cellular Dynamics for {scenario} at {shield_val} mm Al")
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)

# TAB 5: Neural Simulation Layer
with tabs[4]:
    st.header("Neural Simulation Layer")
    if neural_endpoints is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Network Firing Summary")
            st.metric("Population Firing Rate (Hz)", f"{neural_row['mean_firing_rate_hz']:.2f}")
            st.metric("Effective Drive (mV)", f"{neural_row['drive_eff_mV']:.2f}")
            st.metric("Effective Membrane Tau (ms)", f"{neural_row['tau_eff_ms']:.2f}")
            st.metric("Effective Threshold (mV)", f"{neural_row['v_threshold_eff_mV']:.2f}")
            
            # Control reference
            if control is not None:
                st.metric("Healthy Control Firing Rate (Hz)", f"{control.iloc[0]['mean_firing_rate_hz']:.2f}")
        with col2:
            st.subheader("Neural Network Firing Rate vs Shielding")
            st.image(str(INT_FIG_DIR / "endpoint_firing_rate_vs_shielding.png"))

        st.subheader("Raster plot and Membrane Voltages at 10 mm Al")
        col3, col4 = st.columns(2)
        with col3:
            st.image(str(INT_FIG_DIR / f"raster_{scenario}_10mm.png") if (INT_FIG_DIR / f"raster_{scenario}_10mm.png").exists() else [])
            st.caption("Note: Under severe stress (VAB scenario at low shielding), a blank raster indicates zero population firing (LIF shutdown), not missing data.")
        with col4:
            st.image(str(INT_FIG_DIR / f"voltage_{scenario}_10mm.png") if (INT_FIG_DIR / f"voltage_{scenario}_10mm.png").exists() else [])

# TAB 6: Scientific Flags
with tabs[5]:
    st.header("Scientific Flags & Warnings")
    if bio_row is not None:
        # Check domain warning flag
        flag = bio_row['calibration_domain_flag']
        if "outside" in flag:
            st.warning(f"⚠️ warning: Case is outside biological calibration domain! (Status: {flag})")
            st.write(
                f"The selected dose-rate ({forcing_row['total_dose_rate_mGy_day']:.2f} mGy/day) exceeds the validation limits "
                "of chronic low-dose-rate space environments (0.1 to 10.0 mGy/day)."
            )
        else:
            st.success(f"✔️ Case is within validated biological calibration domain. (Status: {flag})")
            
        # Display pipeline status flags
        if status is not None:
            st.subheader("System Execution Status Flags")
            st.table(status)

# TAB 7: Export Report
with tabs[6]:
    st.header("Export Pipeline Reports")
    st.write("Retrieve the HTML report and Markdown summaries created by the integrated pipeline.")
    
    html_file = INT_REP_DIR / "RADBIO_NEURO_integrated_report.html"
    md_file = INT_REP_DIR / "RADBIO_NEURO_integrated_summary.md"
    
    if html_file.exists():
        with open(html_file, "rb") as f:
            st.download_button(
                label="Download HTML Integrated Report",
                data=f.read(),
                file_name="RADBIO_NEURO_integrated_report.html",
                mime="text/html"
            )
    else:
        st.info("HTML report file not found. Run the pipeline first.")
        
    if md_file.exists():
        with open(md_file, "rb") as f:
            st.download_button(
                label="Download Markdown Summary Report",
                data=f.read(),
                file_name="RADBIO_NEURO_integrated_summary.md",
                mime="text/markdown"
            )
