from flask_jwt_extended import get_jwt_identity
from werkzeug.exceptions import Forbidden
from app.models.product import Product
from app.models.user import user_business_association
from app.models.inventory import Inventory
from app.utils.pagination import paginate_query

def add_product(db_session, user_id, product_details):
    associated_bsns = db.session.query(user_business_association).filter_by(user_id=user_id).all()
    if not associated_bsns:
        raise Unauthorized("no associated business. please you must be the owner of the business or associated with one to add products")
    new_product = Product(**product_details)
    db_session.add(new_product)
    db_session.commit()
    return new_product

def get_all_products():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    query = Product.query
    return paginate_query(query, page, per_page)

def update_product(db_session, product_id, data):
    product = Product.get(product_id)
    for k, v in data.items():
        setattr(product, k, v)
    db_session.commit()
    return product
