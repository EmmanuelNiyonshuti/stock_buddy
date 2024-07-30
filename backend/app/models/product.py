"""
Product model
"""
from app.models import BaseModel
from app import db
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declared_attr

class Product(BaseModel, db.Model):
    """
    defines attributes and properties related to Product model.
    """
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(2048))
    size = db.Column(db.String(60), nullable=True)
    weight = db.Column(db.Float, nullable=True)
    color = db.Column(db.String(100), nullable=True)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    unit_cost = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True)
    expiry_date = db.Column(db.Date, nullable=True)
    is_perishable = db.Column(db.Boolean, default=False)


    # business_id = db.Column(db.String(60), db.ForeignKey("business.id"), nullable=False)
    stock_id = db.Column(db.String(60), db.ForeignKey("stocks.id"), nullable=False)
    supplier_id = db.Column(db.String(60), db.ForeignKey('suppliers.id'), nullable=False)
    category_id = db.Column(db.String(60), db.ForeignKey('categories.id'), nullable=False)


    @validates("unit_cost")
    def validate_nonnegative(self, key, value):
        if value < 0:
            raise ValueError(f"{key} cannot be negative")
        return value

