from backend.engine.risk_engine import make_finding


def check_export_restrictions(results, mode):
    attendance_export = results.get("attendance_export", {})
    if mode == "vulnerable" and attendance_export.get("status_code") == 200:
        return make_finding(
            "Unrestricted learner export",
            "high",
            "high",
            "The integration can export learner data without a separate approval workflow.",
            "Require a dedicated export approval check and enforce explicit per-request authorization for bulk exports.",
            evidence=[
                "attendance token reached /learner/export unexpectedly",
                "response status: 200",
                "expected hardened behavior: export denied for attendance-only token",
            ],
            category="export",
        )
    return None
