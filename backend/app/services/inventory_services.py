"""
Inventory services.
"""
from flask import abort
from flask_jwt_extended import get_jwt_identity
from app.models.product import Product
from app.models.business import Business
from app.models.inventory import Inventory
from app.models.user import user_business_association
from app import db
from app.utils.required_data import require_json, require_data
from app.utils.pagination import paginate_query

def add_inventory(user_id, business_id, inventory_details):
    business = Business.get(business_id)
    associated_bsns = db.session.query(user_business_association).filter_by(user_id=user_id).all()
    if not associated_bsns:
        abort(403, "No associated business. You must be the owner of the business or associated with one to add an inventory")
    require_json()
    require_data(inventory_details, [ "product_id", "stock_level", "low_stock_alert"])
    product = Product.get(inventory_details["product_id"])
    new_inventory = Inventory(
                              **inventory_details,
                              business_id=business_id
                              )
    db.session.add(new_inventory)
    db.session.commit()
    return new_inventory

def get_business_inventories(page, per_page, business_id):
    business = Business.query.filter_by(id=business_id).first()
    if not business:
        abort(404, description=f"Business with id {business_id} not found.")
    business_inventories = Inventory.query.filter_by(business_id=business_id)
    paginated_business_inventories = paginate_query(business_inventories, page, per_page)
    if not paginated_business_inventories["items"]:
        abort(404, description="No inventory associated with this business.")
    return paginated_business_inventories
