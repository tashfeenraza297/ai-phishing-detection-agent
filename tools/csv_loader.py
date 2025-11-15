# tools/csv_loader.py
import pandas as pd
from config import CONFIG
from pathlib import Path

def load_phishing_csv() -> pd.DataFrame:
    path: Path = CONFIG["paths"]["dataset"]
    
    if not path.exists():
        raise FileNotFoundError(
            f"CSV NOT FOUND!\n"
            f"Expected: {path}\n"
            f"Check: D:\\Portfolio_Projects\\Phishing_Agent\\archive\\Nazario.csv"
        )
    
    try:
        df = pd.read_csv(path)
        if df.empty:
            raise ValueError("CSV is empty!")
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV: {e}")