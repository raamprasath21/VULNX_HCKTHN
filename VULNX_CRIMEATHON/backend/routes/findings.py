from flask import Blueprint, jsonify

findings_bp = Blueprint("findings", __name__, url_prefix="/api")


@findings_bp.route("/findings", methods=["GET"])
def findings():
    response = {
        "findings": [
            {
                "title": "Excessive API permissions",
                "severity": "high",
                "confidence": "high",
                "description": "The integration has permission beyond its intended attendance scope.",
            }
        ]
    }
    return jsonify(response)
