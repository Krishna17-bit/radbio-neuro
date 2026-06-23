# Run Order Guide

This guide details the sequence for running pipeline scripts, executing tests, and launching the user products.

---

## Prerequisites
Ensure Python is installed and required dependencies are installed. You can install all dependencies by running:
```powershell
pip install -r 03_RADBIO_NEURO_002_BIOLOGY_CALIBRATION/requirements.txt
pip install -r 05_PRODUCT_DASHBOARD_API/requirements.txt
```
*(FastAPI and Streamlit require additional packages listed in the product requirements).*

---

## Execution Sequence

### Step 1: Run the End-to-End Integrated Pipeline
This runs the physics parsing, biological calibration, neural network LIF simulation, and generates the Markdown/HTML reports.
- **Using the batch file**:
  ```powershell
  .\run_full_pipeline.bat
  ```
- **Using the command line**:
  ```powershell
  python run_full_pipeline.py
  ```
- **Outputs generated**:
  - CSV summaries under `06_INTEGRATED_PIPELINE/outputs/`
  - Plot figures under `06_INTEGRATED_PIPELINE/figures/`
  - Automated HTML and MD reports under `06_INTEGRATED_PIPELINE/reports/`

### Step 2: Run Sanity Checks and Tests
This verifies the pipeline outputs, data boundaries, and checks that no NaN values exist in necessary results.
- **Using the batch file**:
  ```powershell
  .\run_tests.bat
  ```
- **Using the command line**:
  ```powershell
  pytest tests/
  ```

### Step 3: Launch the Streamlit Dashboard UI
Provides an interactive visualization of orbit comparisons, dose rate dependencies, daily biology dynamics, and neural population spikes.
- **Using the batch file**:
  ```powershell
  .\run_dashboard.bat
  ```
- **Using the command line**:
  ```powershell
  cd 05_PRODUCT_DASHBOARD_API
  streamlit run streamlit_app.py
  ```

### Step 4: Run the FastAPI REST Server
Exposes GET endpoints mapping scenario summaries and raw data for integration with external dashboards or products.
- **Using the batch file**:
  ```powershell
  .\run_api.bat
  ```
- **Using the command line**:
  ```powershell
  cd 05_PRODUCT_DASHBOARD_API
  python api.py
  ```
