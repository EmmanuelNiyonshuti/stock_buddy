from flask import request
from app import db
from app.models.product import Product
from app.models.inventory import Inventory
from app.utils.required_data import require_json, require_data
from app.utils.pagination import paginate_query
from flask_jwt_extended import get_jwt_identity

def add_product(product_details):
    require_json()
    require_data(product_details, ["name", "price", "sku"], ["description"])
    new_product = Product(**product_details)
    db.session.add(new_product)
    db.session.flush()
    user_id = get_jwt_identity()
    business = Business.query.filter_by(owner_id=user_id).first()
    if not business:
        abort(403, description="User does not have an associated business")
    new_inventory = Inventory(
        business_id=business.id,
        product_id=new_product.id,
        stock_level=0,
        low_stock_alert=product_details.get("low_stock_alert", 5)
    )
    db.session.add(new_inventory)
    db.session.commit()
    return new_product

def get_all_products():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    query = Product.query
    return paginate_query(query, page, per_page)


def update_product(product_id, data):
    require_json()
    product = Product.get(product_id)
    for k, v in data.items():
        setattr(product, k, v)
    db.session.commit()
    return product
