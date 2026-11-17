from backend.engine.risk_engine import make_finding


def check_api_authorization(results, mode):
    attendance_search = results.get("attendance_search", {})
    if mode == "vulnerable" and attendance_search.get("status_code") == 200:
        return make_finding(
            "Excessive API permissions",
            "high",
            "high",
            "The RollCall integration can access learner records despite being limited to attendance-related operations.",
            "Restrict the integration to attendance-only access and require separate approval for learner search and exports.",
            evidence=[
                "attendance token reached /learner/search unexpectedly",
                "response status: 200",
                "expected hardened behavior: access denied",
            ],
            category="api",
        )
    return None
