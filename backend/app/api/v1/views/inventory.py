from flask_jwt_extended import jwt_required
from app.api.v1.views import app_views
from app.utils.decorators import handle_exceptions
from app.services.inventory_services import get_inventory
from app.utils.create_resp import create_resp

@app_views.route("/products/<string:product_id>/inventory", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_inventory_status(product_id):
    product_inventory = get_inventory(product_id)
    return create_resp(product_inventory.to_dict())
