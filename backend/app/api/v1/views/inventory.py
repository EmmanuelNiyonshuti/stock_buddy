from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.views import app_views
from app.utils.decorators import handle_exceptions
from app.services.inventory_services import (
                                             add_inventory,
                                             get_business_inventories
                                            )
from app.utils.create_resp import create_resp

@app_views.route("/businesses/<string:business_id>/inventories", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_business_inventory_view(business_id):
    user_id = get_jwt_identity()
    inventory_details = request.get_json()
    new_inventory = add_inventory(user_id, business_id, inventory_details)
    return create_resp(new_inventory.to_dict(), 201)

@app_views.route("/businesses/<string:business_id>/inventories", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_business_inventories_view(business_id):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    inventories = get_business_inventories(page, per_page, business_id)
    return create_resp(inventories)
