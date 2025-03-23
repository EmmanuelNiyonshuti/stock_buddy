"""
Inventory model for managing stock levels.

This module defines the Inventory model, which tracks stock levels for products. 
"""
from app.models import BaseModel
from app import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Inventory(BaseModel):
    stock_level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    low_stock_alert: Mapped[int] = mapped_column(Integer, nullable=False)

    business_id: Mapped[str] = mapped_column(String(60), ForeignKey("business.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(String(60), ForeignKey('products.id'), nullable=False)

    business = relationship(
        "Business",
        back_populates="inventory"
    )

    product = relationship(
                          "Product",
                          back_populates="inventory"
                          )
    notification = relationship(
      "Notification",
      back_populates="inventory"
    )

    def __repr__(self):
        return f"<Inventory Product id = {self.product_id}, stock level = {self.stock_level}>"

    def update_stock_level(self, quantity: int, transaction_type: str) -> None:
        if transaction_type == "Purchase":
            self.stock_level += quantity
        elif transaction_type == "Sale":
            self.stock_level -= quantity
        if self.stock_level < self.low_stock_alert:
            from app.tasks import send_sms_task
            send_sms_task.delay(self.business.phone_number, "⚠️ Low Stock Alert! Restock early.")
        db.session.commit()
