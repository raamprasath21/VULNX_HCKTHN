import argparse
from flask import Flask, jsonify, request


def create_app(mode="vulnerable"):
    app = Flask(__name__)
    app.config["MODE"] = mode

    def auth_token():
        auth_header = request.headers.get("Authorization", "")
        return auth_header.replace("Bearer ", "").strip()

    def payload_for(name):
        return {
            "record_count": 4,
            "records": [
                {"id": 101, "name": "Ava Thompson", "status": name},
                {"id": 102, "name": "Noah Singh", "status": name},
            ],
        }

    @app.route("/attendance", methods=["GET"])
    def attendance():
        token = auth_token()
        if token in {"attendance", "broad", "admin"}:
            return jsonify({"status": "ok", "message": f"Attendance verified for token {token}", "allowed": True}), 200
        return jsonify({"status": "error", "message": "Invalid or missing token"}), 401

    @app.route("/learner/search", methods=["GET"])
    def learner_search():
        token = auth_token()
        source = request.headers.get("X-Source", "approved")

        if token not in {"attendance", "broad", "admin"}:
            return jsonify({"status": "error", "message": "Authentication required"}), 401

        if mode == "hardened":
            if token == "attendance":
                return jsonify({"status": "forbidden", "message": "Attendance-only token cannot query learner data"}), 403
            if source != "approved" and token in {"attendance", "broad"}:
                return jsonify({"status": "forbidden", "message": "Unapproved source"}), 403
            return jsonify(payload_for("approved")), 200

        if source == "external":
            return jsonify(payload_for("external")), 200

        return jsonify(payload_for("broad-access")), 200

    @app.route("/learner/export", methods=["GET"])
    def learner_export():
        token = auth_token()
        if token not in {"attendance", "broad", "admin"}:
            return jsonify({"status": "error", "message": "Authentication required"}), 401

        if mode == "hardened":
            if token == "attendance":
                return jsonify({"status": "forbidden", "message": "Export requires dedicated approval"}), 403
            return jsonify({"status": "ok", "export": "approved file"}), 200

        return jsonify({"status": "ok", "export": "unrestricted learner export"}), 200

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the VulnX mock API simulation")
    parser.add_argument("--mode", choices=["vulnerable", "hardened"], default="vulnerable")
    args = parser.parse_args()

    app = create_app(mode=args.mode)
    app.run(host="127.0.0.1", port=8765, debug=False)
