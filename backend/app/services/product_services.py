from flask_jwt_extended import get_jwt_identity
from werkzeug.exceptions import Forbidden
from app.models.product import Product
from app.models.business import Business
from app.models.user import user_business_association
from app.models.inventory import Inventory
from app.utils.pagination import paginate_query

def add_product(db_session, user_id, product_details):
    associated_bsns = db_session.query(user_business_association).filter_by(user_id=user_id).all()
    if not associated_bsns:
        raise Unauthorized("no associated business. please you must be the owner of the business or associated with one to add products")
    new_product = Product(**product_details)
    db_session.add(new_product)
    db_session.commit()
    return new_product

def get_all_products(db_session, user_id, business_id, page, per_page):
    business = Business.get(business_id)
    association = db_session.query(user_business_association).filter_by(
        user_id=user_id, business_id=business_id
    ).first()

    if not association:
        raise Forbidden("You are not authorized to view this business's products.")
    query = Product.query.join(Inventory).filter(Inventory.business_id == business_id)
    return paginate_query(query, page, per_page)

def update_product(db_session, user_id, business_id, product_id, product_details):
    business = Business.get(business_id)
    association = db_session.query(user_business_association).filter_by(
        user_id=user_id, business_id=business_id, role="Owner"
    ).first()
    if not association:
        raise Forbidden("You are not authorized to update this business's products.")
    product = Product.query.filter_by(id=product_id).join(Inventory).filter(Inventory.business_id == business_id).first()
    for k, v in product_details.items():
        setattr(product, k, v)
    db_session.commit()
    return product
