from fastapi import FastAPI, HTTPException
import pandas as pd
from pathlib import Path

app = FastAPI(title="RADBIO_NEURO REST API", version="1.0.0")

# Resolve paths
BASE_DIR = Path(__file__).resolve().parent.parent
INT_OUT_DIR = BASE_DIR / "06_INTEGRATED_PIPELINE" / "outputs"

def load_table(name: str) -> pd.DataFrame:
    path = INT_OUT_DIR / name
    if not path.is_file():
        raise HTTPException(status_code=503, detail=f"Data table {name} not found. Please run pipeline first.")
    return pd.read_csv(path)

@app.get("/health")
def get_health():
    return {"status": "healthy"}

@app.get("/scenarios")
def get_scenarios():
    forcing = load_table("biology_ready_dose_forcing_table.csv")
    scenarios = sorted(forcing["scenario"].unique().tolist())
    return {"scenarios": scenarios}

@app.get("/shielding-options")
def get_shielding_options():
    forcing = load_table("biology_ready_dose_forcing_table.csv")
    options = sorted(forcing["shield_mm_Al"].unique().tolist())
    return {"shielding_options_mm_Al": options}

@app.get("/summary")
def get_summary():
    forcing = load_table("biology_ready_dose_forcing_table.csv")
    biology = load_table("biology_calibrated_endpoint_predictions.csv")
    neural = load_table("neural_endpoint_simulation_summary.csv")
    
    # Merge on scenario and shield
    merged = pd.merge(forcing, biology, on=["scenario", "shield_mm_Al"])
    merged = pd.merge(merged, neural, on=["scenario", "shield_mm_Al"], suffixes=('_bio', '_neuro'))
    
    return merged.to_dict(orient="records")

@app.get("/physics/{scenario}")
def get_physics(scenario: str):
    forcing = load_table("biology_ready_dose_forcing_table.csv")
    sub = forcing[forcing["scenario"] == scenario]
    if sub.empty:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario}' not found.")
    return sub.to_dict(orient="records")

@app.get("/biology/{scenario}")
def get_biology(scenario: str):
    biology = load_table("biology_calibrated_endpoint_predictions.csv")
    sub = biology[biology["scenario"] == scenario]
    if sub.empty:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario}' not found.")
    return sub.to_dict(orient="records")

@app.get("/neural/{scenario}")
def get_neural(scenario: str):
    neural = load_table("neural_endpoint_simulation_summary.csv")
    sub = neural[neural["scenario"] == scenario]
    if sub.empty:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario}' not found.")
    return sub.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
