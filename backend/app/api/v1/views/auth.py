"""
Authentication routes.
"""
from flask import request, abort
from werkzeug.exceptions import Unauthorized
from flask_jwt_extended import get_jwt_identity, jwt_required
from email_validator import validate_email, EmailNotValidError
from app import db
from app.api.v1.views import app_views_bp
from app.utils.required_data import require_json, require_data
from app.services.auth_services import register_user, login_user
from app.utils.create_resp import create_resp
from app.utils.auth_helpers import create_auth_response, create_logout_response
from flasgger import swag_from

@app_views_bp.route("/users", methods=["POST"], strict_slashes=False)
@swag_from({
    "tags": ["Authentication"],
    "summary": "User Registration",
    "description": "Registers a new user and returns an authentication token.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "example": "john_doe"},
                    "email": {"type": "string", "example": "john@example.com"},
                    "password": {"type": "string", "example": "securepassword"}
                },
                "required": ["username", "email", "password"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "User registered successfully",
            "examples": {
                "application/json": {
                    "message": "User registered successfully",
                    "access_token": "your-jwt-token"
                }
            }
        },
        400: {"description": "Invalid email address"},
        409: {"description": "User already exists"}
    }
})
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

@app_views_bp.route("/auth/login", methods=["POST"], strict_slashes=False)
@swag_from({
    "tags": ["Authentication"],
    "summary": "User Login",
    "description": "Authenticates a user and returns an access token.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "example": "john@example.com"},
                    "password": {"type": "string", "example": "securepassword"}
                },
                "required": ["email", "password"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "User logged in successfully",
            "examples": {
                "application/json": {
                    "message": "Login successful",
                    "access_token": "your-jwt-token"
                }
            }
        },
        401: {"description": "Invalid email or password"}
    }
})
def user_login_view():
    require_json()
    login_details = request.get_json()
    require_data(login_details, ["email", "password"])
    try:
        user_data = login_user(login_details)
        return create_auth_response(user_data)
    except Unauthorized as e:
        abort(401, description=str(e))

@app_views_bp.route("/auth/logout", methods=["POST"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Authentication"],
    "summary": "User Logout",
    "description": "Logs out the user by invalidating the JWT token.",
    "responses": {
        200: {
            "description": "User logged out successfully",
            "examples": {
                "application/json": {
                    "message": "Logout successful"
                }
            }
        }
    }
})
def user_logout_view():
    return create_logout_response()

@app_views_bp.route("/auth/refresh", methods=["POST"], strict_slashes=False)
@jwt_required(refresh=True)
@swag_from({
    "tags": ["Authentication"],
    "summary": "Refresh Access Token",
    "description": "Refreshes an expired access token.",
    "responses": {
        200: {
            "description": "New token issued",
            "examples": {
                "application/json": {
                    "message": "Token refreshed successfully",
                    "access_token": "your-new-jwt-token"
                }
            }
        }
    }
})
def refresh():
    user_id = get_jwt_identity()
    user_data = {"id": user_id}
    return create_auth_response(user_data, "Token refreshed successfully")
