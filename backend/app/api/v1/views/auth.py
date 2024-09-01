from flask import request, jsonify, session, abort, make_response
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_jwt_identity,
                                jwt_required,
                                set_access_cookies,
                                set_refresh_cookies,
                                unset_jwt_cookies,
                                get_csrf_token)
from email_validator import validate_email, EmailNotValidError
from app.api.v1.views import app_views
from app.models import User
from app.schemas import user_schema, users_schema
from app import db, bcrypt

@app_views.route("/auth/register", methods=["POST"])
def register():
    """ """
    if not request.is_json:
        abort(400, description="Invalid JSON")
    data = request.get_json()
    req_data = ["username", "email", "password", "first_name","last_name"]
    for field in req_data:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400
    try:
        validate_email(data["email"])
    except EmailNotValidError:
        return jsonify({"error": "Invalid email address"}), 400
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "The username is taken choose another one"}), 409
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "the email was taken use another one"}), 409
    
    hash_pwd = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    try:
        user = User(
                username=data["username"],
                email=data["email"],
                password=hash_pwd,
                first_name=data["first_name"],
                last_name=data["last_name"],
                role = data.get("role"),
                )
        db.session.add(user)
        db.session.commit()
        return user_schema.jsonify(user), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create a user", "details": str(e)}), 500

@app_views.route("/auth/login", methods=["POST"])
def login():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    for field in ["email", "password"]:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400
    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"error": "user does not exist"}), 404
    if not bcrypt.check_password_hash(user.password, data["password"]):
        abort(400, description="Invalid password")
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    resp = make_response(jsonify({"login": True}))
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    resp.set_cookie("csrf_access_token", get_csrf_token(access_token))
    resp.set_cookie("csrf_refresh_token", get_csrf_token(refresh_token))
    return resp, 200

@app_views.route("/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    resp = jsonify({"msg": "logout successfully"})
    unset_jwt_cookies(resp)
    return resp, 200

@app_views.route("/auth/refresh")
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    resp = make_response(jsonify({"access_token": access_token}))
    set_access_cookies(resp, access_token)
    return resp, 200
