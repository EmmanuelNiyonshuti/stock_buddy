from flask import request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import Forbidden, NotFound
from app.api.v1.views import app_views_bp
from app.models.product import Product
from app import db
from app.utils.required_data import require_json, require_data
from app.utils.decorators import handle_exceptions
from app.services.inventory_services import (
                                             add_inventory,
                                             get_business_inventories
                                            )
from app.utils.create_resp import create_resp
from flasgger import swag_from

@app_views_bp.route("/businesses/<string:business_id>/inventories", methods=["POST"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Inventory"],
    "summary": "Add inventory to a business",
    "description": "Allows a user to add inventory for a specific business. Requires authentication.",
    "parameters": [
        {
            "name": "business_id",
            "in": "path",
            "required": True,
            "type": "string",
            "description": "The unique ID of the business"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "example": "product123"},
                    "stock_level": {"type": "integer", "example": 100},
                    "low_stock_alert": {"type": "integer", "example": 10}
                },
                "required": ["product_id", "stock_level", "low_stock_alert"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Inventory added successfully",
            "examples": {
                "application/json": {
                    "id": "inventory123",
                    "business_id": "business123",
                    "product_id": "product123",
                    "stock_level": 100,
                    "low_stock_alert": 10
                }
            }
        },
        403: {"description": "User not authorized to add inventory"},
        400: {"description": "Invalid request data"}
    }
})
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

@app_views_bp.route("/businesses/<string:business_id>/inventories", methods=["GET"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Inventory"],
    "summary": "Get all inventories for a business",
    "description": "Retrieves a paginated list of all inventories for a specific business.",
    "parameters": [
        {
            "name": "business_id",
            "in": "path",
            "required": True,
            "type": "string",
            "description": "The unique ID of the business"
        },
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "default": 1,
            "description": "Page number for pagination"
        },
        {
            "name": "per_page",
            "in": "query",
            "type": "integer",
            "default": 10,
            "description": "Number of inventory records per page"
        }
    ],
    "responses": {
        200: {
            "description": "List of inventories",
            "examples": {
                "application/json": {
                    "inventories": [
                        {
                            "id": "inventory123",
                            "business_id": "business123",
                            "product_id": "product123",
                            "stock_level": 100,
                            "low_stock_alert": 10
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "per_page": 10
                }
            }
        },
        404: {"description": "No inventories found"},
        403: {"description": "User not authorized to view inventories"}
    }
})
def get_business_inventories_view(business_id):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    try:
        inventories = get_business_inventories(page, per_page, business_id)
        return create_resp(inventories)
    except NotFound as e:
        abort(404, description=str(e))
