# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# === PROJECT ROOT ===
BASE_DIR = Path(__file__).parent.resolve()

# === DATASET (ABSOLUTE PATH) ===
DATASET_PATH = Path(r"D:\Portfolio_Projects\Phishing_Agent\archive\Nazario.csv")

# === REPORTS DIR ===
REPORTS_DIR = BASE_DIR / "data" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# === MAIN CONFIG ===
CONFIG = {
    "llm": {
        "provider": os.getenv("LLM_PROVIDER", "gemini"),
        "model": os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        "api_key": os.getenv("GEMINI_API_KEY")
    },
    "apis": {
        "virustotal": os.getenv("VT_API_KEY"),
        "otx": os.getenv("OTX_API_KEY")
    },
    "paths": {
        "dataset": DATASET_PATH,
        "reports": REPORTS_DIR,
        "logs": BASE_DIR / "data" / "agent.log"
    },
    "risk_threshold": 70,
    "batch_mode": True
}

# === QUICK VALIDATION ===
if not DATASET_PATH.exists():
    print(f"[WARNING] Dataset missing: {DATASET_PATH}")