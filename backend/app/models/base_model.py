"""
Base model for database entities.

This module defines a reusable base model that provides common attributes 
and utility methods for all database models. It includes:
- UUID-based primary key
- Automatic timestamps (created_at, updated_at)
- Table name generation
- JSON serialization
- Common query methods (get, all)
"""

from datetime import datetime, timezone
import uuid
from werkzeug.exceptions import NotFound
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app import db


class BaseModel(db.Model):
    __abstract__ = True

    id: Mapped[str] = mapped_column(String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __init__(self, **kwargs):
        """Allows setting attributes dynamically while keeping default values."""
        super().__init__(**kwargs)
        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_at = kwargs.get("created_at", datetime.now(timezone.utc))
        self.updated_at = kwargs.get("updated_at", datetime.now(timezone.utc))

    def to_dict(self):
        """Returns a JSON-serializable dictionary of the model."""
        return {
            column.name: (getattr(self, column.name).isoformat() if isinstance(getattr(self, column.name), datetime) else getattr(self, column.name))
            for column in self.__table__.columns
        }

    @declared_attr
    def __tablename__(cls):
        """Generates table names automatically."""
        if cls.__name__.endswith("y"):
            return cls.__name__.strip("y").lower() + "ies"
        elif cls.__name__.endswith("s"):
            return cls.__name__.lower()
        return cls.__name__.lower() + "s"

    @classmethod
    def get(cls, obj_id):
        """Retrieve a single object by ID."""
        obj = db.session.get(cls, obj_id)
        if obj is None:
            raise NotFound(description=f"{cls.__name__} with id {obj_id} not found.")
        return obj

    @classmethod
    def all(cls):
        """Retrieve all objects as dictionaries."""
        return [obj.to_dict() for obj in cls.query.all()]

    def __str__(self):
        return f"<{self.__class__.__name__}> id: {self.id} created_at: {self.created_at} updated_at: {self.updated_at}"
