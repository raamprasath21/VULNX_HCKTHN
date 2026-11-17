from flask import Blueprint, jsonify

reports_bp = Blueprint("reports", __name__, url_prefix="/api")


@reports_bp.route("/reports", methods=["GET"])
def reports():
    return jsonify({
        "summary": {
            "total_assessments": 1,
            "vulnerabilities": 3,
            "severity": {"high": 2, "medium": 1},
        }
    })
