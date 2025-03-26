"""
Authentication routes.
"""
from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from email_validator import validate_email, EmailNotValidError
from app import db
from app.api.v1.views import app_views
from app.utils.required_data import require_json, require_data
from app.services.auth_services import register_user, login_user
from app.utils.create_resp import create_resp
from app.utils.auth_helpers import create_auth_response, create_logout_response

@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_registration_view():
    require_json()
    user_details = request.get_json()
    require_data(user_details, ["username", "email", "password"])
    try:
        validate_email(user_details["email"])
    except EmailNotValidError:
        abort(400, description="Invalid email address")
    try:
        user_data = register_user(db.session, user_details)
        return create_auth_response(user_data, user_data, 201)
    except ValueError as e:
        abort(409, description=str(e))

@app_views.route("/auth/login", methods=["POST"], strict_slashes=False)
def user_login_view():
    require_json()
    login_details = request.get_json()
    require_data(login_details, ["email", "password"])
    try:
        user_data = login_user(user_details)
        return create_auth_response(user_data)
    except Unauthorized as e:
        abort(401, description=str(e))

@app_views.route("/auth/logout", methods=["POST"], strict_slashes=False)
def user_logout_view():
    return create_logout_response()

@app_views.route("/auth/refresh", methods=["POST"], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user_data = {"id": user_id}
    return create_auth_response(user_data, "Token refreshed successfully")
