import os
from pathlib import Path
import pandas as pd

def ensure_dir(path: Path) -> Path:
    """Ensure directory exists and return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path

def load_csv(path: Path, **kwargs) -> pd.DataFrame:
    """Load a CSV file, raising a clear error if it doesn't exist."""
    if not path.exists():
        raise FileNotFoundError(f"Required CSV not found: {path}")
    return pd.read_csv(path, **kwargs)

def save_csv(df: pd.DataFrame, path: Path, index: bool = False, **kwargs):
    """Save a DataFrame to a CSV, creating directories if needed."""
    ensure_dir(path.parent)
    df.to_csv(path, index=index, **kwargs)
