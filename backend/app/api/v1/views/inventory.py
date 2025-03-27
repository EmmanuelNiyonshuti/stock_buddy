from flask import request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import Forbidden
from app.api.v1.views import app_views
from app.models.product import Product
from app import db
from app.utils.required_data import require_json, require_data
from app.utils.decorators import handle_exceptions
from app.services.inventory_services import (
                                             add_inventory,
                                             get_business_inventories
                                            )
from app.utils.create_resp import create_resp

@app_views.route("/businesses/<string:business_id>/inventories", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_business_inventory_view(business_id):
    require_json()
    inventory_details = request.get_json()
    require_data(inventory_details, [ "product_id", "stock_level", "low_stock_alert"])
    user_id = get_jwt_identity()
    product = Product.get(inventory_details["product_id"])
    try:
        new_inventory = add_inventory(db.session, user_id, business_id, inventory_details)
        return create_resp(new_inventory.to_dict(), 201)
    except Forbidden as e:
        abort(403, description=str(e))

@app_views.route("/businesses/<string:business_id>/inventories", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_business_inventories_view(business_id):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    try:
        inventories = get_business_inventories(page, per_page, business_id)
        return create_resp(inventories)
    except NotFound as e:
        abort(404, description=str(e))
