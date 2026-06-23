import pandas as pd
from pathlib import Path
import subprocess
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
INT_OUT_DIR = BASE_DIR / "06_INTEGRATED_PIPELINE" / "outputs"

def test_neural_firing_rates():
    neural_path = INT_OUT_DIR / "neural_endpoint_simulation_summary.csv"
    assert neural_path.is_file()
    
    df = pd.read_csv(neural_path)
    assert 'mean_firing_rate_hz' in df.columns
    assert 'drive_eff_mV' in df.columns
    assert (df['mean_firing_rate_hz'] >= 0.0).all()

def test_dashboard_syntax():
    # Run python -m py_compile to check syntax of streamlit app and api
    dash_path = BASE_DIR / "05_PRODUCT_DASHBOARD_API" / "streamlit_app.py"
    api_path = BASE_DIR / "05_PRODUCT_DASHBOARD_API" / "api.py"
    
    res1 = subprocess.run([sys.executable, "-m", "py_compile", str(dash_path)], capture_output=True)
    assert res1.returncode == 0, f"Streamlit app syntax error: {res1.stderr.decode()}"
    
    res2 = subprocess.run([sys.executable, "-m", "py_compile", str(api_path)], capture_output=True)
    assert res2.returncode == 0, f"API app syntax error: {res2.stderr.decode()}"
