from flask import request
from app import db
from app.models.product import Product
from app.models.user import user_business_association
from app.models.inventory import Inventory
from app.utils.required_data import require_json, require_data
from app.utils.pagination import paginate_query
from flask_jwt_extended import get_jwt_identity

def add_product(product_details):
    user_id = get_jwt_identity()
    associated_bsns = db.session.query(user_business_association).filter_by(user_id=user_id).all()
    if not associated_bsns:
        abort(403, "no associated business. please you must be the owner of the business or associated with one to add products")
    require_json()
    require_data(product_details, ["name", "price", "sku"], ["description"])
    new_product = Product(**product_details)
    db.session.add(new_product)
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
