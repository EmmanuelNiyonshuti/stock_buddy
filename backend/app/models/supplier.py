"""
Supplier model
"""
from app.models import BaseModel
from app import db

class Supplier(BaseModel, db.Model):
    name = db.Column(db.String(120), nullable=False)
    contact_info = db.Column(db.String(200), nullable=False)
