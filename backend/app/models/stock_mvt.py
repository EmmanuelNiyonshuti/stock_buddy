from app import db
from app.models import BaseModel

class StockMovement(BaseModel, db.Model):
    movement_type = db.Column(db.String(20), nullable=False)
    quantity_change = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(100), nullable=False)

    stock_id = db.Column(db.String(60), db.ForeignKey("stocks.id"), nullable=False, )
    product_id = db.Column(db.String(60), db.ForeignKey("products.id"), nullable=False)
