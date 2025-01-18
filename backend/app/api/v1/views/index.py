"""
check the status of the api.
"""
from flask import jsonify, request
from app.models import User
from app.api.v1.views import app_views
@app_views.route("/status", methods=["GET", "POST"], strict_slashes=False)
def stat():
    """
    returns the status of the api.
    """
    return jsonify({
        "status": "OK"
    }), 200
