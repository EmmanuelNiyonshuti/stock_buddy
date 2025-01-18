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
from sqlalchemy.orm import validates, Mapped, mapped_column
from app.models import BaseModel

@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user by user ID.
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
    EMPLOYEE = "employee"

class User(BaseModel, UserMixin):
    username: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(60), nullable=False)
    # is_verified: Mapped[int] = mapped_column(db.Boolean, default=False)
    # is_active: Mapped[int] = mapped_column(db.Boolean, default=True)
    # role: Mapped[str] = mapped_column(db.Enum(UserRole), nullable=False, default=UserRole.OWNER)

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__"""
        dictionary = self.__dict__.copy()
        if "_sa_instance_state" in dictionary:
             del dictionary["_sa_instance_state"]
        return dictionary

    def is_admin(self):
        return self.role == UserRole.ADMIN
    def is_owner(self):
        return self.role == UserRole.OWNER
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
