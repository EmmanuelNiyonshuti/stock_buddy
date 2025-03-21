"""
Product model for managing product details.

This module defines the Product model, which represents items available for sale. 
It includes:
- `name`: Product name
- `description`: Optional product details
- `price`: Cost of the product (stored as Decimal with 2 decimal places)
- `sku`: Unique Stock Keeping Unit identifier
- Relationships:
  - `transaction`: Links to transactions involving the product
  - `inventory`: Links to the inventory record for the product
"""
from app import db
from app.models import BaseModel
from sqlalchemy import Integer, String, Float, Numeric, Text
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Product(BaseModel):
  name: Mapped[str] = mapped_column(String(255), nullable=False)
  description: Mapped[str] = mapped_column(Text, nullable=True)
  price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
  sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

  transactions = relationship(
                      "Transaction",
                      back_populates="product",
                      cascade="all, delete-orphan",
                      )
  inventory = relationship(
                          "Inventory",
                          back_populates="product",
                          uselist=False,
                          cascade="all, delete-orphan"
                          )
  def __repr__(self):
      return f"<Product {self.name}, SKU: {self.sku}, Price: {self.price}"
