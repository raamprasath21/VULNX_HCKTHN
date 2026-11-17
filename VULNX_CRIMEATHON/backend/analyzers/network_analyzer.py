from backend.engine.risk_engine import make_finding


def check_source_restrictions(results, mode):
    unapproved = results.get("unapproved_source", {})
    if mode == "vulnerable" and unapproved.get("status_code") == 200:
        return make_finding(
            "Source validation weakness",
            "medium",
            "high",
            "The service accepted an unapproved simulated source instead of blocking it.",
            "Validate the source origin against the allowlist and reject unexpected sources before serving data.",
            evidence=[
                "X-Source: external was accepted",
                "response status: 200",
                "expected hardened behavior: deny unapproved source",
            ],
            category="network",
        )
    return None
