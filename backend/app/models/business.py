"""
Business model for managing business details.

This module defines the Business model, which represents a business entity. 
"""
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import BaseModel
from app.models.user import user_business_association

class Business(BaseModel):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    users = relationship(
        "User",
        secondary=user_business_association,
        back_populates="businesses"
        )

    notifications = relationship(
        "Notification",
        back_populates="business",
        cascade="all, delete-orphan"
    )
    inventory = relationship(
        "Inventory",
        back_populates="business",
        cascade="all, delete-orphan",
    )
