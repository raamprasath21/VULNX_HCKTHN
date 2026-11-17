from backend.engine.risk_engine import make_finding


def check_local_website_config(results, mode):
    target = results.get("target")
    if target and target.get("https") is False:
        return make_finding(
            "Local site security configuration",
            "medium",
            "medium",
            "The local review target is not enforcing HTTPS or is missing protective response headers.",
            "Enable HTTPS, set HSTS, and harden cookies and security headers for the local assessment target.",
            evidence=[
                "HTTPS check: disabled",
                "cookie check: missing protections",
            ],
            category="web",
        )
    return None
