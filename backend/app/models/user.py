"""
User model for managing user details and authentication.

This module defines the User model, which represents the users of the system (e.g., business owners, employees, and admins). 
"""
from app import db, bcrypt
from sqlalchemy import Column, Enum, String, Table, ForeignKey
from sqlalchemy.orm import validates, Mapped, mapped_column, relationship
from typing import Literal
from app.models import BaseModel

user_business_association = Table(
    'user_business_association',
    db.Model.metadata,
    Column('user_id', String(60), ForeignKey('users.id'), primary_key=True),
    Column('business_id', String(60), ForeignKey('business.id'), primary_key=True),
    Column('role', Enum("Owner", "Employee", "Admin"), nullable=False)
)

class User(BaseModel):
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)

    businesses = relationship(
      "Business",
      secondary=user_business_association,
      back_populates='users'
    )

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__"""
        dictionary = self.__dict__.copy()
        if "_sa_instance_state" in dictionary:
             del dictionary["_sa_instance_state"]
        return dictionary

