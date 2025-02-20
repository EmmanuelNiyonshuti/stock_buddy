from app import db
from app.models.product import Product
from app.models.inventory import Inventory
from app.utils.required_data import require_json, require_data

def add_product(product_details):
    require_json()
    require_data(product_details, ["name", "price", "sku"], ["description"])
    new_product = Product(**product_details)
    db.session.add(new_product)
    db.session.flush()
    new_inventory = Inventory(
        product_id=new_product.id,
        stock_level=0,
        low_stock_alert=product_details.get("low_stock_alert", 5)
    )
    db.session.add(new_inventory)
    db.session.commit()
    return new_product

def get_all_products():
    products = Product.all()
    return products

def update_product(product_id, data):
    require_json()
    product = Product.get(product_id)
    for k, v in data.items():
        setattr(product, k, v)
    db.session.commit()
    return product

