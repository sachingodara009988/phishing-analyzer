import re
import hashlib
from email import policy
from email.parser import BytesParser
from urllib.parse import urlparse


def parse_email(raw_bytes: bytes):
    """Parse raw email bytes (or reconstructed from pasted text) into a message object."""
    return BytesParser(policy=policy.default).parsebytes(raw_bytes)


def parse_pasted_headers(header_text: str):
    """
    Build a minimal fake-email object from pasted headers only (no body).
    We wrap it so header lookups work the same as a full .eml.
    """
    raw = header_text.strip().encode() + b"\n\n"  # blank line = end of headers
    return BytesParser(policy=policy.default).parsebytes(raw)


def get_auth_result(msg, mechanism: str):
    """Extract spf/dkim/dmarc result from Authentication-Results header."""
    auth_header = msg.get("Authentication-Results", "") or ""
    auth_header = auth_header.lower()
    pattern = rf"{mechanism}=(\w+)"
    match = re.search(pattern, auth_header)
    if match:
        return match.group(1)  # pass / fail / none / softfail / neutral
    return "not_found"


def domain_of(address: str):
    if not address:
        return None
    match = re.search(r'@([\w.-]+)', address)
    return match.group(1).lower() if match else None


def analyze_headers(msg):
    """
    Returns a structured list of checks, each with pass/fail/warning status,
    so the frontend can render a clean checklist.
    """
    checks = []

    from_addr = msg.get("From")
    return_path = msg.get("Return-Path")
    reply_to = msg.get("Reply-To")

    spf = get_auth_result(msg, "spf")
    dkim = get_auth_result(msg, "dkim")
    dmarc = get_auth_result(msg, "dmarc")

    checks.append({
        "name": "SPF Authentication",
        "status": "pass" if spf == "pass" else ("warning" if spf == "not_found" else "fail"),
        "detail": f"SPF result: {spf}"
    })
    checks.append({
        "name": "DKIM Authentication",
        "status": "pass" if dkim == "pass" else ("warning" if dkim == "not_found" else "fail"),
        "detail": f"DKIM result: {dkim}"
    })
    checks.append({
        "name": "DMARC Authentication",
        "status": "pass" if dmarc == "pass" else ("warning" if dmarc == "not_found" else "fail"),
        "detail": f"DMARC result: {dmarc}"
    })

    from_domain = domain_of(from_addr)
    return_path_domain = domain_of(return_path)
    mismatch = bool(from_domain and return_path_domain and from_domain != return_path_domain)
    checks.append({
        "name": "From vs Return-Path Match",
        "status": "fail" if mismatch else "pass",
        "detail": f"From domain: {from_domain or 'n/a'} | Return-Path domain: {return_path_domain or 'n/a'}"
    })

    reply_to_domain = domain_of(reply_to)
    reply_mismatch = bool(reply_to_domain and from_domain and reply_to_domain != from_domain)
    checks.append({
        "name": "Reply-To Consistency",
        "status": "warning" if reply_mismatch else "pass",
        "detail": (f"Reply-To domain ({reply_to_domain}) differs from From domain ({from_domain})"
                   if reply_mismatch else "Reply-To matches sender domain or not set")
    })

    received_chain = msg.get_all("Received") or []
    checks.append({
        "name": "Received Chain Present",
        "status": "pass" if received_chain else "warning",
        "detail": f"{len(received_chain)} hop(s) found" if received_chain else "No Received headers found (may be pasted headers only)"
    })

    message_id = msg.get("Message-ID", "")
    mid_domain = None
    mid_match = re.search(r'@([\w.-]+)>?$', message_id or "")
    if mid_match:
        mid_domain = mid_match.group(1).lower()
    mid_mismatch = bool(mid_domain and from_domain and mid_domain != from_domain)
    checks.append({
        "name": "Message-ID Domain Match",
        "status": "warning" if mid_mismatch else "pass",
        "detail": (f"Message-ID domain ({mid_domain}) differs from From domain ({from_domain})"
                   if mid_mismatch else "Message-ID domain consistent or not checkable")
    })

    return {
        "checks": checks,
        "raw": {
            "from": from_addr,
            "return_path": return_path,
            "reply_to": reply_to,
            "subject": msg.get("Subject"),
            "message_id": message_id,
            "received_chain": received_chain,
            "from_domain": from_domain,
        }
    }


def extract_urls_and_attachments(msg):
    urls = set()
    attachments = []

    for part in msg.walk():
        disposition = part.get_content_disposition()
        if disposition == "attachment":
            payload = part.get_payload(decode=True)
            if payload:
                attachments.append({
                    "filename": part.get_filename() or "unknown",
                    "content": payload,
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "size": len(payload)
                })
        ctype = part.get_content_type()
        if ctype in ("text/plain", "text/html"):
            payload = part.get_payload(decode=True)
            if payload:
                text = payload.decode(errors="ignore")
                found = re.findall(r'https?://[^\s"\'<>\)\]]+', text)
                for u in found:
                    urls.add(u.rstrip('.,;'))

    return list(urls), attachments


def get_body_text(msg):
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            payload = part.get_payload(decode=True)
            if payload:
                return payload.decode(errors="ignore")
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            payload = part.get_payload(decode=True)
            if payload:
                return re.sub('<[^<]+?>', ' ', payload.decode(errors="ignore"))
    return ""
