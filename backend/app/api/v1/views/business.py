from flask import request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound
from app import db
from app.api.v1.views import app_views
from app.utils.required_data import require_json, require_data
from app.models.business import Business
from app.services.business_services import (
                                            create_business,
                                            get_all_businesses,
                                            update_business_details,
                                            delete_business
                                            )
from app.utils.create_resp import create_resp
from flasgger import swag_from

@app_views.route("/businesses", methods=["POST"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Businesses"],
    "summary": "Add a new business",
    "description": "Creates a new business for the authenticated user.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "John's Retail"},
                    "phone_number": {"type": "string", "example": "+250788123456"},
                    "email": {"type": "string", "example": "business@example.com"},
                    "description": {"type": "string", "example": "A retail store for electronics."}
                },
                "required": ["name", "phone_number"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Business created successfully",
            "examples": {
                "application/json": {
                    "id": "business_id",
                    "name": "John's Retail",
                    "phone_number": "+250788123456",
                    "email": "business@example.com",
                    "description": "A retail store for electronics."
                }
            }
        }
    }
})
def add_business_view():
    require_json()
    business_details = request.get_json()
    require_data(business_details, ["name", "phone_number"], ["email", "description"])
    user_id = get_jwt_identity()
    new_business = create_business(db.session, user_id, business_details)
    return create_resp(new_business.to_dict(), 201)

@app_views.route("/businesses", methods=["GET"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Businesses"],
    "summary": "Get all businesses",
    "description": "Retrieves all businesses created by the authenticated user.",
    "parameters": [
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
            "description": "Number of businesses per page"
        }
    ],
    "responses": {
        200: {
            "description": "List of businesses",
            "examples": {
                "application/json": {
                    "businesses": [
                        {
                            "id": "business_id",
                            "name": "John's Retail",
                            "phone_number": "+250788123456",
                            "email": "business@example.com",
                            "description": "A retail store for electronics."
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "per_page": 10
                }
            }
        },
        404: {"description": "No businesses found"}
    }
})
def all_businesses_view():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    try:
        user_businesses = get_all_businesses(db.session, user_id, page, per_page)
        return create_resp(user_businesses)
    except NotFound as e:
        abort(404, description=str(e))

@app_views.route("/businesses/<string:business_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Businesses"],
    "summary": "Get a specific business",
    "description": "Retrieves details of a specific business by its ID.",
    "parameters": [
        {
            "name": "business_id",
            "in": "path",
            "required": True,
            "type": "string",
            "description": "The unique ID of the business"
        }
    ],
    "responses": {
        200: {
            "description": "Business details",
            "examples": {
                "application/json": {
                    "id": "business_id",
                    "name": "John's Retail",
                    "phone_number": "+250788123456",
                    "email": "business@example.com",
                    "description": "A retail store for electronics."
                }
            }
        },
        404: {"description": "Business not found"}
    }
})
def get_business_view(business_id):
    business = Business.get(business_id)
    return create_resp(business.to_dict())

@app_views.route("/businesses/<string:business_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Businesses"],
    "summary": "Update a business",
    "description": "Updates the details of an existing business.",
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
                    "name": {"type": "string", "example": "New Business Name"},
                    "phone_number": {"type": "string", "example": "+250788987654"},
                    "email": {"type": "string", "example": "newemail@example.com"},
                    "description": {"type": "string", "example": "Updated business description"}
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "Business updated successfully",
            "examples": {
                "application/json": {
                    "id": "business_id",
                    "name": "New Business Name",
                    "phone_number": "+250788987654",
                    "email": "newemail@example.com",
                    "description": "Updated business description"
                }
            }
        },
        400: {"description": "Bad request"},
        403: {"description": "Forbidden"}
    }
})
def update_business_view(business_id):
    require_json()
    user_id = get_jwt_identity()
    business = Business.get(business_id)
    business_details = request.get_json()
    try:
        updated_details = update_business_details(db.session, user_id, business_id, business_details)
        return create_resp(updated_details.to_dict())
    except BadRequest as e:
        abort(400, description=str(e))
    except Forbidden as e:
        abort(403, description=str(e))

@app_views.route("/businesses/<string:business_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Businesses"],
    "summary": "Delete a business",
    "description": "Deletes an existing business. Only the owner can delete it.",
    "parameters": [
        {
            "name": "business_id",
            "in": "path",
            "required": True,
            "type": "string",
            "description": "The unique ID of the business"
        }
    ],
    "responses": {
        200: {"description": "Business deleted successfully"},
        403: {"description": "Not authorized to delete this business"},
        404: {"description": "Business not found"}
    }
})
def delete_business_view(business_id):
    business = Business.get(business_id)
    user_id = get_jwt_identity()
    try:
        msg = delete_business(db.session, user_id, business_id)
        return create_resp({"message": "Business deleted successfully"})
    except Forbidden as e:
        abort(403, description=str(e))
