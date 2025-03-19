"""
Transaction model for recording product purchases and sales.

This module defines the Transaction model, which tracks individual sales and purchases of products. 
It includes:
- `transaction_type`: Indicates whether the transaction is a "Purchase" or "Sale"
- `quantity`: The number of units involved in the transaction
- `total_price`: The total cost of the transaction
- `product_id`: Foreign key linking the transaction to a specific product
"""
from typing import Literal
from sqlalchemy import Integer, String, Float, Numeric, ForeignKey, Enum
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from app import db
from app.models import BaseModel

class Transaction(BaseModel):
    transaction_type: Mapped[Literal["Purchase", "Sale"]] = mapped_column(Enum("Purchase", "Sale", name="transaction_type_enum"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    product_id: Mapped[str] = mapped_column(String(60), ForeignKey("products.id"), nullable=False)

    def __repr__(self):
        return f"<transaction_type: {self.transaction_type}, quantity: {self.quantity}, total_price: {self.total_price}"
