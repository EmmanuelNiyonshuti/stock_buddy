"""
Authentication routes.
"""
from flask import request, jsonify, session, abort, make_response
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_jwt_identity,
                                jwt_required)
from email_validator import validate_email, EmailNotValidError
from app.api.v1.views import app_views
from app.models import User
from app import db, bcrypt

@app_views.route("/auth/register", methods=["POST"], strict_slashes=False)
def register_user():
    if not request.is_json:
        abort(400, description="Invalid JSON")
    user_details = request.get_json()
    required_fields = ["username", "email", "password"]
    if not all(field in user_details for field in required_fields):
        missing_fields = [field for field in user_details if field not in required_fields]
        return jsonify({"error": f"Missing required fields: {", ".join(missing_fields)}"}), 400
    try:
        validate_email(user_details["email"])
    except EmailNotValidError:
        return jsonify({"error": "Invalid email address"}), 400
    if User.query.filter_by(email=user_details["email"]).first():
        return jsonify({"error": "The email was taken use another email"}), 409
    if User.query.filter_by(username=user_details["username"]).first():
        return jsonify({"error": "The username was taken, user another username"}), 409

    pwd_hash = bcrypt.generate_password_hash(user_details["password"]).decode("utf-8")
    try:
        new_user = User(
                username=user_details["username"],
                email=user_details["email"],
                password=pwd_hash
                )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create a user", "details": str(e)}), 500

@app_views.route("/auth/login", methods=["POST"], strict_slashes=False)
def login_user():
    if not request.is_json:
        abort(400, description="Invalid JSON")
    user_details = request.get_json()
    for field in ["email", "password"]:
        if field not in user_details:
            return jsonify({"error": f"Missing {field}"}), 400
    user = User.query.filter_by(email=user_details["email"]).first()
    if not user:
        return jsonify({"error": "Not found"}), 404
    if not bcrypt.check_password_hash(user.password, user_details["password"]):
        abort(400, description="Invalid password")
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(
        access_token = access_token,
        refresh_token = refresh_token
        )

@app_views.route("/auth/refresh", methods=["GET"], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify(access_token = access_token)

@app_views.route("/auth/get_me", methods=["GET"], strict_slashes=False)
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at,
    }), 200
