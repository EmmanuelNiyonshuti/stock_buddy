from app import db
from app.models import BaseModel
from sqlalchemy import Integer, String, Float, Numeric, ForeignKey, Enum
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column


class Transaction(BaseModel):
    transaction_type: Mapped[str] = mapped_column(String(255), Enum("Purchase", "Sale"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    product_id: Mapped[str] = mapped_column(String(60), ForeignKey("products.id"), nullable=False)

    def __repr__(self):
        return f"<transaction_type: {self.transaction_type}, quantity: {self.quantity}, total_price: {self.total_price}"
