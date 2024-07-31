"""
User Model
"""
import jwt
from flask import current_app
from app import db, bcrypt, login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from enum import Enum
from sqlalchemy.ext.declarative import declared_attr
import re
from sqlalchemy.orm import validates
from app.models import BaseModel

@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user by their user ID.
    :param user_id: The ID of the user to load.
    :return: The user object or None if not found.
    """
    return User.query.get(user_id)

class UserRole(Enum):
    """
    Enum for defining user roles.
    """
    ADMIN = "admin"
    OWNER = "owner"
    MANAGER = "manager"
    EMPLOYEE = "employee"

class User(BaseModel, UserMixin):
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.OWNER)

    def to_dict(self):
        d = super().to_dict()
        d["role"] = self.role.value if self.role else None
        d["username"] = self.username
        d.pop("password", None)
        d["first_name"] = self.first_name
        d["last_name"] = self.last_name
        d["is_verified"] = self.is_verified
        d["is_active"] = self.is_active
        return d

    @validates("email")
    def validate_email(self, key, email):
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email


    @validates("first_name", "last_name")
    def validate_name(self, key, name):
        if not re.match("^[a-zA-Z][a-zA-Z_ ]{2,}$", name):
            raise ValueError(f"{key} must be in letters, underscores or spaces")
        return name

    @declared_attr
    def full_name(self):
        """
        Returns the user's full name by combining first and last name.
        """
        return f"{self.first_name} {self.last_name}"


    def is_admin(self):
        return self.role == UserRole.ADMIN
    def is_owner(self):
        return self.role == UserRole.OWNER
    def is_manager(self):
        return self.role == UserRole.MANAGER
    def is_employee(self):
        return self.role == UserRole.EMPLOYEE
    def has_role(self, role):
        return self.role == role

    def get_reset_token(self):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.id}, salt=current_app.config["SECURITY_PASSWORD_SALT"])

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expires_sec)
        except:
            return None
        return User.query.get(user_id)
