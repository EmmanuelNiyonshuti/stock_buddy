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

    transaction = relationship(
                        "Transaction",
                        backref="product",
                        cascade="all, delete-orphan",
                        lazy="dynamic"
                        )
    inventory = relationship(
                            "Inventory",
                            backref="product",
                            uselist=False,
                            cascade="all, delete-orphan"
                            )
    def __repr__(self):
        return f"<Product {self.name}, SKU: {self.sku}, Price: {self.price}"
