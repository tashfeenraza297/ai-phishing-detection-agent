# project_root.py
import sys
from pathlib import Path

# D:\Portfolio_Projects\Phishing_Agent\ai_phishing_agent  <-- your project root
PROJECT_ROOT = Path(__file__).parent.resolve()

# Add root to Python path if not already there
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Optional: expose for imports
__all__ = ["PROJECT_ROOT"]