from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.api.v1.views import app_views_bp
from app.models.product import Product
from app import db
from app.utils.create_resp import create_resp
from app.services.product_services import (add_product,
                                           get_all_products,
                                           update_product)
from flasgger import swag_from

@app_views_bp.route("/products", methods=["POST"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Products"],
    "summary": "Add a new product",
    "description": "Creates a new product for the authenticated user.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Laptop"},
                    "price": {"type": "number", "example": 999.99},
                    "sku": {"type": "string", "example": "LPT-12345"},
                    "description": {"type": "string", "example": "High-performance laptop"}
                },
                "required": ["name", "price", "sku"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Product created successfully",
            "examples": {
                "application/json": {
                    "id": "product123",
                    "name": "Laptop",
                    "price": 999.99,
                    "sku": "LPT-12345",
                    "description": "High-performance laptop"
                }
            }
        },
        401: {"description": "Unauthorized request"}
    }
})
def add_product_view():
    require_json()
    require_data(product_details, ["name", "price", "sku"], ["description"])
    user_id = get_jwt_identity()
    product_details = request.get_json()
    try:
        new_product = add_product(db.session, user_id, product_details)
        return create_resp(new_product.to_dict(), 201)
    except Unauthorized as e:
        abort(401, description=str(e))

@app_views_bp.route("/products", methods=["GET"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Products"],
    "summary": "Retrieve all products for a business",
    "description": "Fetches a paginated list of products associated with a specific business.",
    "parameters": [
        {
            "name": "business_id",
            "in": "query",
            "required": True,
            "type": "string",
            "description": "The ID of the business whose products are being retrieved"
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
            "description": "Number of products per page"
        }
    ],
    "responses": {
        200: {
            "description": "List of products",
            "examples": {
                "application/json": {
                    "products": [
                        {
                            "id": "product123",
                            "name": "Laptop",
                            "price": 999.99,
                            "sku": "LPT-12345",
                            "description": "High-performance laptop"
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "per_page": 10
                }
            }
        },
        400: {"description": "Missing business_id"},
        401: {"description": "Unauthorized access"}
    }
})
def get_all_products_view():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    business_id = request.args.get("business_id", type=str)
    if not business_id:
        abort(400, description="business_id is required")
    products = get_all_products(db.session, user_id, business_id, page, per_page)
    return create_resp(products)

@app_views_bp.route("/products/<string:product_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Products"],
    "summary": "Get a specific product",
    "description": "Retrieves details of a single product by its ID.",
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "type": "string",
            "description": "The unique ID of the product"
        }
    ],
    "responses": {
        200: {
            "description": "Product details",
            "examples": {
                "application/json": {
                    "id": "product123",
                    "name": "Laptop",
                    "price": 999.99,
                    "sku": "LPT-12345",
                    "description": "High-performance laptop"
                }
            }
        },
        404: {"description": "Product not found"}
    }
})
def get_product_view(product_id):
    product = Product.get(product_id)
    return create_resp(product.to_dict())

@app_views_bp.route("/products/<string:product_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Products"],
    "summary": "Update a product",
    "description": "Updates the details of an existing product.",
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "type": "string",
            "description": "The unique ID of the product"
        },
        {
            "name": "business_id",
            "in": "query",
            "required": True,
            "type": "string",
            "description": "The ID of the business that owns the product"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Updated Laptop"},
                    "price": {"type": "number", "example": 899.99},
                    "sku": {"type": "string", "example": "LPT-12345"},
                    "description": {"type": "string", "example": "Updated high-performance laptop"}
                }
            }
        }
    ],
    "responses": {
        200: {"description": "Product updated successfully"},
        400: {"description": "Missing business_id"},
        404: {"description": "Product not found"}
    }
})
def update_product_view(product_id):
    require_json()
    data = request.get_json()
    business_id = request.args.get("business_id", type=str)
    if not business_id:
        abort(400, description="business_id is required")
    user_id = get_jwt_identity()
    updated_product = update_product(db.session, user_id, business_id, product_id, data)
    return create_resp(updated_product.to_dict())

@app_views_bp.route("/products/<string:product_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Products"],
    "summary": "Delete a product",
    "description": "Removes a product from the database.",
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "type": "string",
            "description": "The unique ID of the product"
        }
    ],
    "responses": {
        200: {"description": "Product deleted successfully"},
        404: {"description": "Product not found"}
    }
})
def delete_product_view(product_id):
    product = Product.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return create_resp({})
