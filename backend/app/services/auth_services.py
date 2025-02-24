from flask import abort
from flask_jwt_extended import (create_access_token,
                                create_refresh_token
                                )
from email_validator import validate_email, EmailNotValidError
from app.utils.required_data import require_json, require_data
from app import db, bcrypt
from app.models.user import User

def register_user(user_details):
    require_json()
    require_data(user_details, ["username", "email", "password"])
    try:
        validate_email(user_details["email"])
    except EmailNotValidError:
        abort(400, description="Invalid email address")
    if User.query.filter_by(email=user_details["email"]).first():
        abort(409, description=f"{user_details["email"]} was taken please use another email.")
    pwd_hash = bcrypt.generate_password_hash(user_details["password"]).decode("utf-8")
    new_user = User(
        username=user_details["username"],
        email=user_details["email"],
        password=pwd_hash
        )
    db.session.add(new_user)
    db.session.commit()
    return new_user


def login_user(login_details):
    require_json()
    require_data(login_details, ["email", "password"])
    user = User.query.filter_by(email=login_details["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password, login_details["password"]):
        abort(401, description="Invalid email or password")
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def logout_user():
    pass