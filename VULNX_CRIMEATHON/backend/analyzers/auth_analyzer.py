from backend.engine.risk_engine import make_finding


def check_authentication(results, mode):
    invalid_auth = results.get("invalid_auth", {})
    status_code = invalid_auth.get("status_code")
    if mode == "vulnerable" and status_code not in (None, 0, 401):
        return make_finding(
            "Authentication bypass",
            "critical",
            "medium",
            "Invalid credentials were accepted instead of being rejected.",
            "Reject unknown credentials immediately and enforce token validation before access is granted.",
            evidence=[
                "invalid token resulted in a non-401 response",
                "response status: {}".format(status_code),
            ],
            category="auth",
        )
    return None
