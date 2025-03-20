"""
Authentication routes.
"""
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.api.v1.views import app_views
from app.services.auth_services import register_user, login_user
from app.utils.create_resp import create_resp
from app.utils.auth_helpers import create_auth_response, create_logout_response

@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_registration_view():
    user_details = request.get_json()
    user_data = register_user(user_details)
    return create_auth_response(user_data, "user registered successfully", 201)

@app_views.route("/auth/login", methods=["POST"], strict_slashes=False)
def user_login_view():
    user_details = request.get_json()
    user_data = login_user(user_details)
    return create_auth_response(user_data, "Logged in successfully")

@app_views.route("/auth/logout", methods=["POST"], strict_slashes=False)
def user_logout_view():
    return create_logout_response()

@app_views.route("/auth/refresh", methods=["POST"], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user_data = {"id": user_id}
    return create_auth_response(user_data, "Token refreshed successfully")
