from flask import Blueprint, jsonify, request

from backend.engine.scanner import run_assessment

assessment_bp = Blueprint("assessment", __name__, url_prefix="/api")


@assessment_bp.route("/assessment", methods=["POST", "GET"])
def assessment():
    payload = request.get_json(silent=True) or {}
    mode = payload.get("mode", "vulnerable")
    result = run_assessment(mode=mode)
    return jsonify(result)
