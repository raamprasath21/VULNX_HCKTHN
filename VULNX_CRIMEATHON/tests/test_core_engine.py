from backend.engine.scanner import analyze_assessment


VULNERABLE_RESULTS = {
    "attendance_search": {"status_code": 200},
    "attendance_export": {"status_code": 200},
    "unapproved_source": {"status_code": 200},
    "invalid_auth": {"status_code": 200},
}

HARDENED_RESULTS = {
    "attendance_search": {"status_code": 403},
    "attendance_export": {"status_code": 403},
    "unapproved_source": {"status_code": 403},
    "invalid_auth": {"status_code": 401},
}


def test_vulnerable_mode_reports_issues():
    outcome = analyze_assessment(VULNERABLE_RESULTS, mode="vulnerable")
    assert any(item["title"] == "Excessive API permissions" for item in outcome["findings"])
    assert any(item["title"] == "Unrestricted learner export" for item in outcome["findings"])
    assert any(item["title"] == "Source validation weakness" for item in outcome["findings"])


def test_hardened_mode_has_no_findings():
    outcome = analyze_assessment(HARDENED_RESULTS, mode="hardened")
    assert outcome["findings"] == []
