"""
Inventory model for managing stock levels.

This module defines the Inventory model, which tracks stock levels for products. 
It includes:
- `stock_level`: Current stock count
- `low_stock_alert`: Threshold for low stock notifications
- `product_id`: Foreign key linking to the associated product
- Methods for updating stock levels based on transactions
"""
from app.models import BaseModel
from app import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.services.notification_service import send_sms

class Inventory(BaseModel):
    stock_level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    low_stock_alert: Mapped[int] = mapped_column(Integer, nullable=False)

    product_id: Mapped[str] = mapped_column(String(60), ForeignKey('products.id'), nullable=False)
    user_id: Mapped[str] = mapped_column(String(60), ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Inventory Product id = {self.product_id}, stock level = {self.stock_level}>"

    def update_stock_level(self, quantity: int, transaction_type: str) -> None:
        if transaction_type == "Purchase":
            self.stock_level += quantity
        elif transaction_type == "Sale":
            self.stock_level -= quantity
        if self.stock_level < self.low_stock_alert:
            send_sms_task.delay(user.phone_number, "⚠️ Low Stock Alert! Restock early.")
        db.session.commit()
