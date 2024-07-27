from flask import request, jsonify, session, abort, jsonify
from email_validator import validate_email, EmailNotValidError
from app.api.v1.views import app_views
from app.models import User
from app import db, bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

@app_views.route("/users", methods=["POST"])
def create_user():
    """ """
    if not request.is_json:
        abort(400)
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
        return jsonify({"error": "The username is taken choose another one"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "the email was taken use another one"}), 400

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
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create a user", "details": str(e)}), 500
    return jsonify({"msg": "created successfully"}), 201

@app_views.route("users/auth", methods=["POST"])
def auth():
    if not request.is_json:
        abort(400)
    data = request.get_json()
    for field in ["email", "password"]:
        if field not in data:
            return jsonify({"error": f"Missing {field}"}), 400
    user = User.query.filter_by(email=data["email"]).first()
    if not user and bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"error": "check email and password"}), 400
    access_token = create_access_token(identity=user.id)
    return jsonify({
        "access_token": access_token,
        "id": user.id
    }), 200

@app_views.route("/users/<uuid:user_id>")
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    curr_user_id = get_jwt_identity()
    if str(curr_user_id) != str(user_id):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(user.to_dict()), 200

@app_views.route("/users/<uuid:user_id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_user(user_id):
    curr_user_id = get_jwt_identity()
    if str(curr_user_id) != str(user_id):
        return jsonify({"error": "unauthorized"}), 401
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    