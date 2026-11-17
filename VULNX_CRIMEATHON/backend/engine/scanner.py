import requests

from backend.ai.explainer import explain_finding
from backend.analyzers.api_analyzer import check_api_authorization
from backend.analyzers.auth_analyzer import check_authentication
from backend.analyzers.export_analyzer import check_export_restrictions
from backend.analyzers.network_analyzer import check_source_restrictions
from backend.analyzers.web_config_analyzer import check_local_website_config

DEFAULT_BASE_URL = "http://127.0.0.1:8765"


def fetch_json(base_url, endpoint, token=None, source=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if source:
        headers["X-Source"] = source
    try:
        response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
        payload = {}
        try:
            payload = response.json()
        except ValueError:
            payload = {"raw": response.text}
        return {
            "status_code": response.status_code,
            "payload": payload,
        }
    except requests.exceptions.RequestException as exc:
        return {
            "status_code": 0,
            "payload": {"error": str(exc)},
        }


def run_assessment(mode="vulnerable", base_url=DEFAULT_BASE_URL):
    assessment = {
        "mode": mode,
        "target": base_url,
        "tests": {
            "attendance_access": fetch_json(base_url, "/attendance", token="attendance"),
            "attendance_search": fetch_json(base_url, "/learner/search", token="attendance"),
            "attendance_export": fetch_json(base_url, "/learner/export", token="attendance"),
            "invalid_auth": fetch_json(base_url, "/learner/search", token="unknown"),
            "unapproved_source": fetch_json(base_url, "/learner/search", token="attendance", source="external"),
            "approved_source": fetch_json(base_url, "/learner/search", token="attendance", source="approved"),
            "broad_access": fetch_json(base_url, "/learner/search", token="broad"),
        },
    }
    findings = []
    for analyzer in (
        check_api_authorization,
        check_export_restrictions,
        check_source_restrictions,
        check_authentication,
        check_local_website_config,
    ):
        result = analyzer(assessment["tests"], mode)
        if result:
            findings.append({**result, "explanation": explain_finding(result)})
    assessment["findings"] = findings
    return assessment


def analyze_assessment(results, mode="vulnerable"):
    findings = []
    for analyzer in (
        check_api_authorization,
        check_export_restrictions,
        check_source_restrictions,
        check_authentication,
        check_local_website_config,
    ):
        result = analyzer(results, mode)
        if result:
            findings.append({**result, "explanation": explain_finding(result)})
    return {"mode": mode, "findings": findings}
