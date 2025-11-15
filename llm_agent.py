# llm_agent.py
import json, google.generativeai as genai
from config import CONFIG
from error_handler import log

genai.configure(api_key=CONFIG["llm"]["api_key"])
model = genai.GenerativeModel(CONFIG["llm"]["model"])

def generate_report(rule_res: dict, intel_res: list, raw: str) -> dict:
    context = f"""
    Input: {raw}
    Rule Result: {json.dumps(rule_res)}
    Threat Intel: {json.dumps(intel_res)}
    """
    prompt = f"""
    You are a senior cybersecurity analyst.
    Based on the data above, output **only** valid JSON with:
    - risk_score (0-100)
    - classification (Phishing / Malicious / Suspicious / Safe)
    - reason (2 sentences max)
    - action (user advice)
    {context}
    """
    try:
        resp = model.generate_content(prompt)
        return json.loads(resp.text.strip("```json\n"))
    except Exception as e:
        log.error(f"LLM failed: {e}")
        return {"risk_score": 50, "classification": "Unknown", "reason": "LLM error", "action": "Manual review"}