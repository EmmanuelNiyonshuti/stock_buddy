"""
User model for managing user details and authentication.

This module defines the User model, which represents the users of the system (e.g., business owners, employees, and admins). 
It includes:
- `username`: The unique username of the user
- `email`: The unique email of the user (used for login)
- `password`: The hashed password for user authentication
- `role`: The role of the user (Owner, Employee, or Admin)
- Relationships:
  - `business`: Links to the `Business` model, where the user is the owner of a business
"""
from app import db, bcrypt, login_manager
from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import validates, Mapped, mapped_column, relationship
from typing import Literal
from app.models import BaseModel

@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user by user ID.
    :param user_id: The ID of the user to load.
    :return: The user object or None if not found.
    """
    return User.query.get(user_id)

class User(BaseModel, UserMixin):
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    role: Mapped[Literal["Owner", "Employee", "Admin"]] = mapped_column(String(60), nullable=False)

    business = relationship("Business", backref="owner", cascade="all, delete-orphan")

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__"""
        dictionary = self.__dict__.copy()
        if "_sa_instance_state" in dictionary:
             del dictionary["_sa_instance_state"]
        return dictionary

