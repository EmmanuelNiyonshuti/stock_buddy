"""
Inventory services.
"""
from werkzeug.exceptions import NotFound, Forbidden
from app.models.product import Product
from app.models.business import Business
from app.models.inventory import Inventory
from app.models.user import user_business_association
from app.utils.pagination import paginate_query

def add_inventory(db_session, user_id, business_id, inventory_details):
    associated_bsns = db_session.query(user_business_association).filter_by(user_id=user_id).all()
    if not associated_bsns:
        raise Forbidden("No associated business. You must be the owner of the business or associated with one to add an inventory")
    new_inventory = Inventory(
                              **inventory_details,
                              business_id=business_id
                              )
    db_session.add(new_inventory)
    db_session.commit()
    return new_inventory

def get_business_inventories(page, per_page, business_id):
    business = Business.query.filter_by(id=business_id)
    if not business:
        raise NotFound(f"Business with id {business_id} not found.")
    business_inventories = Inventory.query.filter_by(business_id=business_id)
    if business_inventories.count() == 0:
        raise NotFound("No inventory associated with this business.")

    paginated_business_inventories = paginate_query(business_inventories, page, per_page)

    if not paginated_business_inventories["items"]:
        raise NotFound("No inventory associated with this business.")

    return paginated_business_inventories

