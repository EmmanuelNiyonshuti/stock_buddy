"""
Category specific products model.
"""
from app import db
from app.models import BaseModel

class Category(BaseModel, db.Model):
    """
    Implements Product categorie's table.
    """
    name = db.Column(db.String(128), nullable=False)
    brand = db.Column(db.String(128), nullable=False)
    # warranty = db.Column(db.Date, nullable=True)
