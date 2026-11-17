from flask import Flask, jsonify
from flask_cors import CORS

from backend.routes.assessment import assessment_bp
from backend.routes.findings import findings_bp
from backend.routes.reports import reports_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(assessment_bp)
    app.register_blueprint(findings_bp)
    app.register_blueprint(reports_bp)

    @app.route("/")
    def root():
        return jsonify({
            "name": "VulnX",
            "status": "ready",
            "mode": "crimeathon"
        })

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=True)
