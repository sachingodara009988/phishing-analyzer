import os
import json
import requests

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def analyze_with_gemini(subject: str, body: str, from_domain: str, urls: list):
    key = os.getenv("GEMINI_API_KEY", "")
    if not key:
        return {"status": "skipped", "reason": "no_api_key"}

    prompt = f"""You are a phishing analyst. Analyze this email and respond with ONLY valid JSON, no markdown fences, no extra text.

JSON schema:
{{
  "is_likely_phishing": boolean,
  "confidence": "low" | "medium" | "high",
  "impersonated_brand": string or null,
  "social_engineering_tactics": [array of short strings, e.g. "urgency", "authority impersonation", "threat of account suspension"],
  "tone_red_flags": [array of short strings, e.g. "generic greeting", "poor grammar", "mismatched sender name"],
  "summary": "one or two sentence plain-English verdict"
}}

Email subject: {subject or "N/A"}
Sender domain: {from_domain or "N/A"}
Links found in email: {urls[:10]}
Email body (truncated):
{(body or "")[:4000]}
"""

    try:
        r = requests.post(
            f"{GEMINI_URL}?key={key}",
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=25
        )
        if not r.ok:
            return {"status": "error", "code": r.status_code, "body": r.text[:300]}

        data = r.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        text = text.strip().strip("```json").strip("```").strip()
        parsed = json.loads(text)
        parsed["status"] = "success"
        return parsed
    except Exception as e:
        return {"status": "error", "error": str(e)}
