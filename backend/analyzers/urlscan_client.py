import os
import time
import requests

BASE = "https://urlscan.io/api/v1"


def scan_url(url: str, wait_seconds: int = 8):
    """
    Submits a URL to urlscan.io and polls briefly for the result.
    If not ready within wait_seconds, returns the pending scan link instead.
    """
    key = os.getenv("URLSCAN_API_KEY", "")
    if not key:
        return {"url": url, "status": "skipped", "reason": "no_api_key"}

    headers = {"API-Key": key, "Content-Type": "application/json"}
    try:
        submit = requests.post(f"{BASE}/scan/", headers=headers,
                                json={"url": url, "visibility": "unlisted"}, timeout=15)
        if not submit.ok:
            return {"url": url, "status": "error", "code": submit.status_code, "body": submit.text[:200]}

        result = submit.json()
        result_url = result.get("api")
        scan_page = result.get("result")

        for _ in range(wait_seconds):
            time.sleep(1)
            check = requests.get(result_url, timeout=10)
            if check.status_code == 200:
                data = check.json()
                verdicts = data.get("verdicts", {}).get("overall", {})
                return {
                    "url": url,
                    "status": "complete",
                    "malicious": verdicts.get("malicious", False),
                    "score": verdicts.get("score", 0),
                    "screenshot": data.get("task", {}).get("screenshotURL"),
                    "report_url": scan_page,
                }

        return {"url": url, "status": "pending", "report_url": scan_page}
    except Exception as e:
        return {"url": url, "status": "error", "error": str(e)}
