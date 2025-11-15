# tools/rule_tool.py
import re
from error_handler import safe_tool

class RuleTool:
    KEYWORDS = ['login', 'verify', 'update', 'bank', 'password', 'security', 'account']
    
    # FIXED: Only trigger typo if domain is NOT in known good list
    KNOWN_GOOD_DOMAINS = ['google.com', 'microsoft.com', 'apple.com', 'amazon.com', 'github.com']
    
    TYPOS = re.compile(
        r'(paypa[1l]|g[o0]{2}gle|am[4a]z[0o]n|micros[o0]ft|'
        r'apple-support|icloud-verification)\.(com|net|org)',
        re.IGNORECASE
    )

    @staticmethod
    @safe_tool
    def analyze(text: str) -> dict:
        reasons = []
        lower = text.lower()

        # Keyword check
        if any(kw in lower for kw in RuleTool.KEYWORDS):
            reasons.append("Suspicious keyword")

        # Domain typo check
        domain_match = re.search(r'https?://([^\s/]+)', text)
        if domain_match:
            domain = domain_match.group(1).lower()
            if domain not in RuleTool.KNOWN_GOOD_DOMAINS:
                if RuleTool.TYPOS.search(domain):
                    reasons.append("Domain typo-squatting")

        return {
            "suspected": bool(reasons),
            "reasons": reasons
        }