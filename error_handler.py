# error_handler.py
import logging
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.FileHandler("data/agent.log"), logging.StreamHandler()]
)
log = logging.getLogger("PhishingAgent")

def safe_tool(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.error(f"{func.__name__} failed: {e}")
            return {"error": str(e), "source": func.__name__}
    return wrapper