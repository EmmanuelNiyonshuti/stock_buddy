"""
Authentication services.
"""
from app import bcrypt
from werkzeug.exceptions import Unauthorized
from app.models.user import User

def register_user(db_session, user_details):
    existing_user = User.query.filter_by(email=user_details["email"]).first()
    if existing_user:
        raise ValueError(f"{user_details["email"]} is already taken. please use another email.")
    pwd_hash = bcrypt.generate_password_hash(user_details["password"]).decode("utf-8")
    new_user = User(
        username=user_details["username"],
        email=user_details["email"],
        password=pwd_hash
        )
    db_session.add(new_user)
    db_session.commit()
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }

def login_user(login_details):
    user = User.query.filter_by(email=login_details["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password, login_details["password"]):
        raise Unauthorized("Invalid email or password")
    return {
        "id": user.id
        }
