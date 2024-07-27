"""
Base class to which all models inherit the same functionality.
"""
from app import db
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @declared_attr
    def __tablename__(cls):
        if cls.__name__.endswith("y"):
            return cls.__name__.strip("y").lower() + "ies"
        elif cls.__name__.endswith("s"):
            return cls.__name__.lower()
        return cls.__name__.lower() + "s"

    def to_dict(self):
        dictionary = self.__dict__.copy()
        dictionary.pop("_sa_instance_state", None)
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        return dictionary
    
    @classmethod
    def get(cls, obj_id):
        """
        retrieves a single object.
        """
        obj = db.session.get(cls, obj_id)
        return obj if obj else None

    @classmethod
    def all(cls):
        """
        Retrieves all objs.
        """
        objs = cls.query.all()
        return [obj.to_dict() for obj in objs] if objs else None

    def __str__(self):
        return f"<{self.__class__.__name__}> id: {self.id} created_at: {self.created_at} updated_at: {self.updated_at}"
