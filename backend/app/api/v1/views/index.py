from flask import jsonify
from app.api.v1.views import app_views


@app_views.route("/status", methods=["GET"])
def stat():
    return jsonify({
        "status": "OK"
    }), 200