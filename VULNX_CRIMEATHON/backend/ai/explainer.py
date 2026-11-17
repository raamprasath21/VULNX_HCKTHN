def explain_finding(finding):
    title = finding.get("title", "Security issue")
    severity = finding.get("severity", "medium").upper()
    description = finding.get("description", "The system did not enforce the expected security control.")
    recommendation = finding.get("recommendation", "Review the configuration and apply the least-privilege policy.")

    return {
        "title": title,
        "severity": severity,
        "explanation": (
            f"Detected issue: {title}. {description} "
            f"This matters because the implemented control does not match the expected security policy for the target environment."
        ),
        "recommendation": recommendation,
    }
