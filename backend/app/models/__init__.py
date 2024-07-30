"""
Setup SQLAlchemy relationships for models in the application.

This module imports all models and establishes relationships between them using SQLAlchemy's
relationship function and backref attribute.

Relationships:
- Category.products: One-to-many relationship where each Category can have multiple Products.
- Supplier.products: One-to-many relationship where each Supplier can supply multiple Products.
- Stock.products: One-to-many relationship where each stock can have multiple products.
- Stock.locations: Many-to-one relationship where each Stock entry is associated with a specific Location.
"""
from app import db
from .base_model import BaseModel
from .user import User, UserRole
from .business import Business
from .product import Product
from .product_category import Category
from .supplier import Supplier
from .stock import Stock, Location
from .stock_mvt import StockMovement


#user relationships
User.business = db.relationship("Business", back_populates="owner", cascade="all, delete-orphan")


#business relationships
Business.owner = db.relationship("User", back_populates="business")
# Business.products = db.relationship("Product", back_populates="business")
Business.stocks = db.relationship("Stock", back_populates="business", cascade="all, delete-orphan")
Business.location = db.relationship("Location", back_populates="business")

# product relationships
# Product.business = db.relationship("Business", back_populates="products")
Product.stock = db.relationship("Stock", back_populates="products")
Product.supplier = db.relationship("Supplier", back_populates="products")
Product.category = db.relationship("Category", back_populates="products")

#supplier relationship with product
Supplier.products = db.relationship("Product", back_populates="supplier")

#category relationships
Category.products = db.relationship("Product", back_populates="category")

#stock relationships
Stock.business = db.relationship("Business", back_populates="stocks")
Stock.products = db.relationship("Product", back_populates="stock", cascade="all, delete-orphan")
Stock.movements = db.relationship("StockMovement", back_populates="stock", cascade="all, delete-orphan")
Stock.location = db.relationship("Location", back_populates="stocks")


#stock movement
StockMovement.stock = db.relationship("Stock", back_populates="movements")
StockMovement.product = db.relationship("Product")


#location
Location.stocks = db.relationship("Stock", back_populates="location")
Location.business = db.relationship("Business", back_populates="location")
