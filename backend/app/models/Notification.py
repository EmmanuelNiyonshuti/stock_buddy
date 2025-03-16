"""
Notification model
"""
from typing import Literal
from app.models import BaseModel
from app import db
from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Notification(BaseModel):
    """ """
    recipient: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[Literal["SMS", "Email", "In-App"]] = mapped_column(Enum("SMS", "Email", "In-App"), nullable=False)
    status: Mapped[Literal["Pending", "Sent", "Failed"]] = mapped_column(Enum("Pending", "Sent", "Failed"), default="Pending")

    user_id: Mapped[str] = mapped_column(String(60), ForeignKey("users.id"), nullable=False)
