from app.models import db
from app.models import BaseModel
from sqlalchemy.orm import validates

class Stock(BaseModel):
    quantity = db.Column(db.Integer, nullable=False, default=0)
    business_id = db.Column(db.String(60), db.ForeignKey("business.id"), nullable=False,)
    location_id = db.Column(db.String(60), db.ForeignKey("locations.id"), nullable=False)

    @validates("quantity")
    def validate_quantity(self, key, quantity):
        if quantity < 0:
            raise ValueError(f"{key} cannot be negative")
        return quantity

    def record_movement(self, quantity_change, movement_type, reason):
        if movement_type not in ["in", "out"]:
            raise ValueError("Movement type must be 'in' or 'out'")
        new_quantity = self.quantity + quantity_change if movement_type == "in" else self.quantity - quantity_change
        if new_quantity < 0:
            raise ValueError("Quantity can not be negative")
        movement = StockMovement(
            product_id = self.product_id,
            quantity_change = quantity_change,
            movement_type = movement_type,
            reason = reason,
            stock_id = self.id
        )
        self.quantity = new_quantity
        db.session.add(movement)
        db.session.add(self)
        db.session.commit()

    def get_stock_value(self):
        return self.quantity * self.products.unit_cost

    @classmethod
    def get_low_stock_levels(cls, threshold):
        return cls.query.filter(cls.quantity < threshold).all()


class Location(BaseModel, db.Model):
    name = db.Column(db.String(100), nullable=False)
    business_id = db.Column(db.String(60), db.ForeignKey("business.id"), nullable=False)
