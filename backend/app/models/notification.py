"""
Notification model for managing business notifications.

This module defines the Notification model, which represents notifications sent to users regarding business-related events. 
It includes:
- `recipient`: The recipient of the notification (e.g., business owner)
- `message`: The content or body of the notification
- `channel`: The channel through which the notification is sent (SMS, Email, or In-App)
- `status`: The current status of the notification (Pending, Sent, or Failed)
- `business_id`: ID of the business associated with the notification
- `inventory_id`: ID of the inventory associated with the notification (if applicable)
- Relationships:
  - `business`: Links to the `Business` model, associating the notification with a specific business
  - `inventory`: Links to the `Inventory` model, associating the notification with a specific inventory item
"""
from typing import Literal
from app.models import BaseModel
from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Notification(BaseModel):
    message: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[Literal["SMS", "Email", "In-App"]] = mapped_column(Enum("SMS", "Email", "In-App"), nullable=False)
    status: Mapped[Literal["Pending", "Sent", "Failed"]] = mapped_column(Enum("Pending", "Sent", "Failed"), default="Pending")

    business_id: Mapped[str] = mapped_column(String(60), ForeignKey("business.id"), nullable=False)
    inventory_id: Mapped[str] = mapped_column(String(60), ForeignKey("inventories.id"), nullable=True)

    business = relationship(
      "Business",
      back_populates="notifications"
    )
    inventory = relationship(
      "Inventory",
      back_populates="notification"
    )
