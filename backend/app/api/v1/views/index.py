"""
check the status of the api.
"""
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.models import User
from app.api.v1.views import app_views
@app_views.route("/status", methods=["GET", "POST"], strict_slashes=False)
def stat():
    """
    returns the status of the api.

    ---
    responses:
        200:
            description: A successful response.
            examples:
            {
                "status": "OK"
            }
    """
    return jsonify({
        "status": "OK"
    }), 200
