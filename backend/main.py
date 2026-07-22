import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from analyzers.header_parser import (
    parse_email, parse_pasted_headers, analyze_headers,
    extract_urls_and_attachments, get_body_text
)
from analyzers.vt_client import get_url_reputation, get_file_reputation, get_domain_reputation
from analyzers.urlscan_client import scan_url
from analyzers.whois_client import get_domain_age
from analyzers.gemini_client import analyze_with_gemini
from scoring import compute_verdict

load_dotenv()

app = FastAPI(title="Phishing Mail Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_full_analysis(msg):
    header_result = analyze_headers(msg)
    urls, attachments = extract_urls_and_attachments(msg)
    body = get_body_text(msg)

    # URL reputation — cap to avoid burning free-tier rate limits
    url_reports = [get_url_reputation(u) for u in urls[:8]]

    # urlscan for top 3 URLs only (slower, live scan)
    urlscan_reports = [scan_url(u) for u in urls[:3]]

    # Attachments
    file_reports = [
        get_file_reputation(a["sha256"], a["filename"]) for a in attachments
    ]

    # Domain reputation + WHOIS age for sender domain
    from_domain = header_result["raw"].get("from_domain")
    domain_report = get_domain_reputation(from_domain) if from_domain else None
    whois_report = get_domain_age(from_domain) if from_domain else None

    # AI content analysis
    gemini_result = analyze_with_gemini(
        subject=header_result["raw"].get("subject"),
        body=body,
        from_domain=from_domain,
        urls=urls
    )

    verdict = compute_verdict(header_result, url_reports, file_reports, domain_report, whois_report, gemini_result)

    return {
        "verdict": verdict,
        "headers": header_result,
        "urls": url_reports,
        "urlscan": urlscan_reports,
        "attachments": file_reports,
        "domain_reputation": domain_report,
        "domain_age": whois_report,
        "ai_analysis": gemini_result,
        "extracted": {
            "url_count": len(urls),
            "attachment_count": len(attachments),
            "urls_found": urls,
        }
    }


@app.post("/api/analyze/file")
async def analyze_file(file: UploadFile):
    raw = await file.read()
    msg = parse_email(raw)
    return run_full_analysis(msg)


@app.post("/api/analyze/headers")
async def analyze_headers_only(header_text: str = Form(...)):
    msg = parse_pasted_headers(header_text)
    return run_full_analysis(msg)


@app.post("/api/analyze/raw")
async def analyze_raw_text(raw_email: str = Form(...)):
    msg = parse_email(raw_email.encode())
    return run_full_analysis(msg)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


# Serve React build (single-service deploy)
FRONTEND_BUILD = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(FRONTEND_BUILD):
    app.mount("/", StaticFiles(directory=FRONTEND_BUILD, html=True), name="static")
