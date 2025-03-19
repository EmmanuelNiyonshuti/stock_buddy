"""
Business model for managing business details.

This module defines the Business model, which represents a business entity. 
It includes:
- `name`: The name of the business
- `phone_number`: Business's unique phone number
- `email`: Optional email address of the business
- `description`: Optional detailed description of the business
- `owner_id`: ID of the user who owns the business, linking to the `User` model
- Relationships:
  - `notification`: Links to notifications related to the business (e.g., stock-outs)
  - `inventories`: Links to inventory records associated with the business
"""
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import BaseModel

class Business(BaseModel):
    """ """
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    owner_id: Mapped[str] = mapped_column(String(60), ForeignKey("users.id"), nullable=False)

    notification = relationship(
        "Notification",
        backref="business",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    inventory = relationship(
        "Inventory",
        backref="business",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
