from datetime import datetime, timezone
import whois as pywhois


def get_domain_age(domain: str):
    try:
        w = pywhois.whois(domain)
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        if not creation:
            return {"domain": domain, "status": "unknown"}

        if creation.tzinfo is None:
            creation = creation.replace(tzinfo=timezone.utc)
        age_days = (datetime.now(timezone.utc) - creation).days

        return {
            "domain": domain,
            "status": "found",
            "creation_date": str(creation),
            "age_days": age_days,
            "newly_registered": age_days < 30
        }
    except Exception as e:
        return {"domain": domain, "status": "error", "error": str(e)}
