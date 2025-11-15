# tools/virustotal_tool.py
import requests, time, json
from config import CONFIG
from error_handler import safe_tool, log

class VirusTotalTool:
    BASE = "https://www.virustotal.com/api/v3"

    @staticmethod
    @safe_tool
    def scan_url(url: str) -> dict:
        api_key = CONFIG["apis"]["virustotal"]
        if not api_key: return {"error": "VT key missing"}

        # submit
        submit = requests.post(
            f"{VirusTotalTool.BASE}/urls",
            headers={"x-apikey": api_key},
            data={"url": url}
        )
        if submit.status_code != 200:
            return {"error": f"VT submit {submit.status_code}"}
        scan_id = submit.json()["data"]["id"]

        # poll
        for _ in range(3):
            time.sleep(4)
            r = requests.get(
                f"{VirusTotalTool.BASE}/analyses/{scan_id}",
                headers={"x-apikey": api_key}
            )
            if r.status_code == 200:
                stats = r.json()["data"]["attributes"]["stats"]
                malicious = stats.get("malicious", 0)
                total = sum(stats.values())
                return {
                    "source": "VirusTotal",
                    "malicious": malicious,
                    "total": total,
                    "threat_level": "High" if malicious > 0 else "Low"
                }
        return {"error": "VT timeout"}