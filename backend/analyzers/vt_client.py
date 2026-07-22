import os
import base64
import requests

VT_BASE = "https://www.virustotal.com/api/v3"


def _headers():
    key = os.getenv("VT_API_KEY", "")
    return {"x-apikey": key}


def get_url_reputation(url: str):
    try:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        r = requests.get(f"{VT_BASE}/urls/{url_id}", headers=_headers(), timeout=15)
        if r.status_code == 404:
            # Not seen before — submit it
            sub = requests.post(f"{VT_BASE}/urls", headers=_headers(), data={"url": url}, timeout=15)
            return {"url": url, "status": "submitted_new", "raw": sub.json() if sub.ok else None}
        data = r.json()
        stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        return {
            "url": url,
            "status": "found",
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0),
            "undetected": stats.get("undetected", 0),
        }
    except Exception as e:
        return {"url": url, "status": "error", "error": str(e)}


def get_domain_reputation(domain: str):
    try:
        r = requests.get(f"{VT_BASE}/domains/{domain}", headers=_headers(), timeout=15)
        if not r.ok:
            return {"domain": domain, "status": "error", "code": r.status_code}
        data = r.json().get("data", {}).get("attributes", {})
        stats = data.get("last_analysis_stats", {})
        return {
            "domain": domain,
            "status": "found",
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0),
            "reputation_score": data.get("reputation", 0),
            "creation_date": data.get("creation_date"),
        }
    except Exception as e:
        return {"domain": domain, "status": "error", "error": str(e)}


def get_file_reputation(sha256: str, filename: str = ""):
    try:
        r = requests.get(f"{VT_BASE}/files/{sha256}", headers=_headers(), timeout=15)
        if r.status_code == 404:
            return {"filename": filename, "sha256": sha256, "status": "not_found_in_vt"}
        data = r.json().get("data", {}).get("attributes", {})
        stats = data.get("last_analysis_stats", {})
        return {
            "filename": filename,
            "sha256": sha256,
            "status": "found",
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "type_description": data.get("type_description"),
            "meaningful_name": data.get("meaningful_name"),
        }
    except Exception as e:
        return {"filename": filename, "sha256": sha256, "status": "error", "error": str(e)}
