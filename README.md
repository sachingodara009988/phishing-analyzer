# Phishing Mail Analyzer

Upload an .eml file, paste headers, or paste raw email source to get:
- Header authentication checklist (SPF/DKIM/DMARC, From/Return-Path mismatch, etc.) - pass/fail/warning per check
- URL reputation via VirusTotal + live sandbox via urlscan.io
- Attachment reputation via VirusTotal (hash lookup)
- Sender domain reputation (VirusTotal) + domain age (WHOIS)
- AI content analysis via Gemini (impersonation, social engineering tactics, tone red flags)
- Aggregated risk score and verdict (Low / Medium / High / Critical)

## Local development

### 1. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # then fill in your real API keys
uvicorn main:app --reload --port 8000
```
Backend runs at http://localhost:8000 - Swagger docs at http://localhost:8000/docs

### 2. Frontend (separate terminal)
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at http://localhost:5173 and proxies /api calls to the backend.

## API Keys needed
- VirusTotal: https://www.virustotal.com/ -> profile -> API Key (free tier: 500/day, 4/min)
- urlscan.io: https://urlscan.io/ -> Settings -> API (free tier available)
- Gemini: https://aistudio.google.com/ -> Get API Key (free tier available)

Put them in backend/.env locally, and as Environment Variables in Render for deployment.

## Deploying to Render (single service)

React build output goes directly into backend/static/, so ONE Render web
service can serve both the API and the frontend.

1. On Render: New -> Web Service -> connect your GitHub repo
   - Root Directory: backend
   - Build Command:
     pip install -r requirements.txt && cd ../frontend && npm install && npm run build
   - Start Command:
     uvicorn main:app --host 0.0.0.0 --port $PORT
   - Environment Variables: VT_API_KEY, URLSCAN_API_KEY, GEMINI_API_KEY

2. Deploy. Your site + API will be live at the same Render URL.

## Notes
- Free-tier VirusTotal is rate-limited (4 req/min) - backend caps URL lookups to 8 per email and urlscan live scans to 3 per email.
- Render's free tier spins down on inactivity; first request after idle takes ~30-50s to wake up.
- WHOIS lookups can fail/timeout depending on TLD - handled gracefully, won't crash analysis.
