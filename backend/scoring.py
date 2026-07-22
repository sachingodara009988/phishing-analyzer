def compute_verdict(header_result, url_reports, file_reports, domain_report, whois_report, gemini_result):
    score = 0
    reasons = []

    for check in header_result.get("checks", []):
        if check["status"] == "fail":
            if "SPF" in check["name"] or "DKIM" in check["name"] or "DMARC" in check["name"]:
                score += 12
            else:
                score += 15
            reasons.append(f"Header check failed: {check['name']}")
        elif check["status"] == "warning":
            score += 5

    for u in url_reports:
        if u.get("status") == "found":
            if u.get("malicious", 0) > 0:
                score += 25
                reasons.append(f"Malicious URL detected: {u['url']}")
            elif u.get("suspicious", 0) > 0:
                score += 12
                reasons.append(f"Suspicious URL flagged: {u['url']}")

    for f in file_reports:
        if f.get("status") == "found" and f.get("malicious", 0) > 0:
            score += 30
            reasons.append(f"Malicious attachment detected: {f.get('filename')}")

    if domain_report and domain_report.get("status") == "found":
        if domain_report.get("malicious", 0) > 0:
            score += 20
            reasons.append("Sender domain has malicious detections on VirusTotal")

    if whois_report and whois_report.get("status") == "found" and whois_report.get("newly_registered"):
        score += 15
        reasons.append(f"Sender/link domain registered only {whois_report.get('age_days')} days ago")

    if gemini_result and gemini_result.get("status") == "success":
        if gemini_result.get("is_likely_phishing"):
            confidence_weight = {"low": 10, "medium": 18, "high": 25}.get(gemini_result.get("confidence", "low"), 10)
            score += confidence_weight
            reasons.append(f"AI analysis: {gemini_result.get('summary', 'flagged as likely phishing')}")
        if gemini_result.get("impersonated_brand"):
            score += 10
            reasons.append(f"AI detected possible impersonation of: {gemini_result['impersonated_brand']}")

    score = min(score, 100)

    if score >= 76:
        verdict = "Critical"
    elif score >= 51:
        verdict = "High"
    elif score >= 26:
        verdict = "Medium"
    else:
        verdict = "Low"

    return {
        "score": score,
        "verdict": verdict,
        "reasons": reasons
    }
