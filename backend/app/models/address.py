from app import db
from app.models import BaseModel

class Address(BaseModel, db.Model):
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
