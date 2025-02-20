"""
Setup SQLAlchemy relationships for models in the application.

This module imports all models and establishes relationships between them using SQLAlchemy's
relationship function and backref attribute.
"""

from app import db
from .base_model import BaseModel
from .user import User

