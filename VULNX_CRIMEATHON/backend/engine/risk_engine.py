def severity_rank(severity):
    mapping = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    return mapping.get(str(severity).lower(), 0)


def make_finding(title, severity, confidence, description, recommendation, evidence=None, category="security"):
    return {
        "title": title,
        "severity": str(severity).lower(),
        "confidence": str(confidence).lower(),
        "description": description,
        "recommendation": recommendation,
        "category": category,
        "evidence": evidence or [],
    }


def compare_expected(actual, expected):
    if actual == expected:
        return True
    if isinstance(actual, str) and isinstance(expected, str):
        return actual.lower() == expected.lower()
    return bool(actual == expected)
