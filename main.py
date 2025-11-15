# main.py
import project_root
import uvicorn, argparse, json, datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tools.rule_tool import RuleTool
from tools.virustotal_tool import VirusTotalTool
from tools.otx_tool import OTXTool
from llm_agent import generate_report
from config import CONFIG
from error_handler import log

app = FastAPI(title="AI Phishing Agent")

class ScanRequest(BaseModel):
    input: str
    type: str = "url"   # url | ip | email

def run_scan(data: str, typ: str) -> dict:
    # 1. Rule
    rule = RuleTool.analyze(data)

    # 2. Threat Intel (only if rule suspicious)
    intel = []
    if rule["suspected"]:
        if typ == "url":
            intel.append(VirusTotalTool.scan_url(data))
            intel.append(OTXTool.check_indicator(data, "url"))
        elif typ == "ip":
            intel.append(OTXTool.check_indicator(data, "IPv4"))
    else:
        intel.append({"source": "Skipped", "details": "Rule clean"})

    # 3. LLM
    llm = generate_report(rule, intel, data)

    # 4. Final
    report = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "input": {"type": typ, "value": data},
        "rule": rule,
        "intel": intel,
        "llm": llm,
        "risk_score": llm["risk_score"],
        "classification": llm["classification"],
        "alert": "DANGER – BLOCK!" if llm["risk_score"] > CONFIG["risk_threshold"] else "Safe"
    }
    # Save
    out_path = CONFIG["paths"]["reports"] / f"{int(datetime.datetime.now().timestamp())}.json"
    out_path.write_text(json.dumps(report, indent=2))
    return report

@app.post("/scan")
def scan(req: ScanRequest):
    return run_scan(req.input, req.type)

# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--type", default="url")
    parser.add_argument("--serve", action="store_true")
    args = parser.parse_args()

    if args.serve:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        print(json.dumps(run_scan(args.input, args.type), indent=2))