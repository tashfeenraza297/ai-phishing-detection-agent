# tools/otx_tool.py
import requests
from config import CONFIG
from error_handler import safe_tool

class OTXTool:
    @staticmethod
    @safe_tool
    def check_indicator(indicator: str, ind_type: str = "url") -> dict:
        key = CONFIG["apis"]["otx"]
        if not key: return {"error": "OTX key missing"}
        url = f"https://otx.alienvault.com/api/v1/indicators/{ind_type}/{indicator}/general"
        r = requests.get(url, headers={"X-OTX-API-KEY": key})
        if r.status_code == 200:
            data = r.json()
            pulses = len(data.get("pulse_info", {}).get("pulses", []))
            return {
                "source": "AlienVault OTX",
                "pulses": pulses,
                "threat_level": "High" if pulses > 0 else "Low"
            }
        return {"error": f"OTX {r.status_code}"}