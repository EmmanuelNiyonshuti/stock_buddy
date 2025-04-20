"""
check the status of the api.
"""
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from app.models import User
from app.api.v1.views import app_views_bp
from flasgger import swag_from

@app_views_bp.route("/status", methods=["GET"], strict_slashes=False)
@swag_from({
    "tags": ["API Status"],
    "summary": "Check API status",
    "description": "This endpoint checks whether the API is running properly.",
    "responses": {
        200: {
            "description": "API is running successfully.",
            "examples": {
                "application/json": {
                    "status": "OK"
                }
            }
        }
    }
})
def status():
    return jsonify({
        "status": "OK"
    }), 200
