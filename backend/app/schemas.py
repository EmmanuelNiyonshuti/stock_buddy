from app import ma
from app.models import (User, UserRole,
                Business, Stock, Location, Category,
                Supplier, Product, StockMovement)

class SupplierSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Supplier
        include_relationships = True
        load_instance = True

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_relationships = True
        load_instance = True

class StockMovementSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StockMovement
        include_relationships = True
        load_instance = True
    # created_at = ma.DateTime(format="%Y-%m-%d %H:%M:%S")

class Location(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        include_relationships = True
        load_instance = True

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_relationships = True
        include_fk = True
        load_instance = True
    category = ma.Nested(CategorySchema, many=True, exclude=("products",))
    supplier = ma.Nested(Supplier, many=True, exclude=("products",))


class StockSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stock
        include_fk = True
        include_relationships = True
        load_instance = True
    # location = ma.Nested(LocationSchema)
    products = ma.Nested(ProductSchema, many=True, exclude=("stock",))
    movements = ma.Nested(StockMovement, many=True, exclude=("stock",))


class BusinessSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Business
        include_relationships = True
        include_fk = True
        load_instance = True
    stocks = ma.Nested(StockSchema, many=True, exclude=("business", ))
    location = ma.Nested(StockSchema, exclude=("business",))

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        exclude = ("password",)
    role = ma.Enum(UserRole)


#single user schema
user_schema = UserSchema()
#multiple user schema
users_schema = UserSchema(many=True)

business_schema = BusinessSchema()
businesses_schema = BusinessSchema(many=True)

stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

supplier_schema = SupplierSchema()
suppliers_schema = SupplierSchema(many=True)

category_schema = CategorySchema()


