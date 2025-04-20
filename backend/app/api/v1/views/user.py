from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.api.v1.views import app_views_bp
from app.services.user_services import (
                                        user_profile,
                                        update_account,
                                        delete_account
                                        )
from app.utils.create_resp import create_resp
from flasgger import swag_from

@app_views_bp.route("/users/profile", methods=["GET"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Account"],
    "summary": "Account Details",
    "description": "Retrieves user's account details.",
    "responses": {
        200: {
            "examples": {
                "application/json": {
                    "id": "user_id",
                    "username": "user_username",
                    "email": "user_email",
                    "created_at": "user_created_at"
                    }
                }
            },
        401: {
            "error": "Unauthorized",
            "message": "Missing cookie \"access_cookie\""
            }
        }
    })
def user_profile_view():
    user_id = get_jwt_identity()
    user_details = user_profile(user_id)
    return create_resp(user_details)

@app_views_bp.route("/users/update", methods=["PUT", "PATCH"])
@jwt_required()
@swag_from({
    "tags": ["Account"],
    "summary": "Update user's account",
    "description": "Update user's account details"
})
def update_account():
    user_id = get_jwt_identity()
    updated_user = update_account(user_id)
    return create_resp(updated_user)

@app_views_bp.route("/users/delete", methods=["DELETE"])
@jwt_required()
@swag_from({
    "tags": ["Account"],
    "summary": "Delete Account",
    "description": "Delete User's Account"
})
def delete_account():
    user_id = get_jwt_identity()
    delete_account(user_id)
    return create_resp()
