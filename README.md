# AI Phishing Detection Agent 🛡️

An AI-powered agent for detecting phishing URLs, IPs, and emails. It uses rule-based patterns, external APIs (VirusTotal, AlienVault OTX), and Gemini 1.5 Flash LLM for reasoning and risk scoring.

**Note:** This is an ongoing project. I'm currently enhancing it with advanced features like fine-tuned LLM models, Chrome extension integration, real-time Gmail monitoring, and deployment to cloud platforms (e.g., Render). Contributions and feedback welcome!

## Features
- **Modular Architecture:** 3-layer system (Rule-based, Threat Intel, LLM Analysis).
- **Inputs Supported:** URLs, IPs, full email content.
- **Batch Scanning:** Process CSV datasets (e.g., Nazario Phishing Corpus with 1565 emails).
- **UI:** Interactive Streamlit app for single/batch scans.
- **API:** FastAPI backend for programmatic access.
- **Reports:** JSON outputs with risk score (0-100), classification (Phishing/Safe), and recommendations.
- **External Tools:** VirusTotal & OTX APIs (free tiers).
- **Testing:** 299 URLs scanned in batch mode with 24.7% detection rate.

## Demo
![Batch Scan Demo](demo.gif)  <!-- Upload a GIF/screenshot of Streamlit running batch scan -->

## Tech Stack
- **Language:** Python 3.10+
- **AI/LLM:** Google Gemini 1.5 Flash
- **APIs:** VirusTotal, AlienVault OTX
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Libs:** requests, pandas, google-generativeai, python-dotenv
- **Dataset:** Nazario Phishing Corpus (not included; download from source)

## Setup & Run
1. Clone repo: `git clone https://github.com/yourusername/ai-phishing-detection-agent.git`
2. Install deps: `pip install -r requirements.txt`
3. Create `.env` (see .env.example):