from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.views import app_views
from app.services.transaction_services import (create_transaction,
                                               get_product_transactions,
                                               get_product_transaction
                                              )
from app.utils.create_resp import create_resp
from flasgger import swag_from

@app_views.route("/products/<string:product_id>/transactions", methods=["POST"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Transactions"],
    "summary": "Create a new transaction for a product",
    "description": "Records a new stock transaction (e.g., sale or purchase) for a product.",
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "type": "string",
            "description": "The unique ID of the product"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "transaction_type": {
                        "type": "string",
                        "enum": ["sale", "purchase"],
                        "example": "sale",
                        "description": "Type of transaction (sale or purchase)"
                    },
                    "quantity": {
                        "type": "integer",
                        "example": 5,
                        "description": "Quantity of the product involved in the transaction"
                    },
                    "total_price": {
                        "type": "number",
                        "example": 499.95,
                        "description": "Total price of the transaction"
                    }
                },
                "required": ["transaction_type", "quantity", "total_price"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Transaction created successfully",
            "examples": {
                "application/json": {
                    "id": "txn123",
                    "product_id": "product123",
                    "transaction_type": "sale",
                    "quantity": 5,
                    "total_price": 499.95,
                    "timestamp": "2025-03-27T10:00:00Z"
                }
            }
        },
        400: {"description": "Bad request - missing or invalid fields"},
        401: {"description": "Unauthorized request"}
    }
})
def create_transaction_view(product_id):
    require_json()
    transaction_details = request.get_json()
    require_data(transaction_details, ["transaction_type", "quantity", "total_price"])
    user_id = get_jwt_identity()
    try:
        new_transaction = create_transaction(db.session, user_id, product_id, transaction_details)
        return create_resp(new_transaction.to_dict(), 201)
    except BadRequest as e:
        abort(400, description=str(e))

@app_views.route("/products/<string:product_id>/transactions", methods=["GET"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Transactions"],
    "summary": "Retrieve all transactions for a product",
    "description": "Fetches a paginated list of transactions related to a specific product.",
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "type": "string",
            "description": "The unique ID of the product"
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
            "description": "Number of transactions per page"
        }
    ],
    "responses": {
        200: {
            "description": "List of transactions",
            "examples": {
                "application/json": {
                    "transactions": [
                        {
                            "id": "txn123",
                            "transaction_type": "sale",
                            "quantity": 5,
                            "total_price": 499.95,
                            "timestamp": "2025-03-27T10:00:00Z"
                        },
                        {
                            "id": "txn124",
                            "transaction_type": "purchase",
                            "quantity": 10,
                            "total_price": 999.90,
                            "timestamp": "2025-03-26T09:30:00Z"
                        }
                    ],
                    "total": 2,
                    "page": 1,
                    "per_page": 10
                }
            }
        },
        401: {"description": "Unauthorized access"}
    }
})
def get_product_transactions_view(product_id):
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    transactions = get_product_transactions(db.session, user_id, page, per_page, product_id)
    return create_resp(transactions)

@app_views.route("/products/<string:product_id>/transactions/<string:transaction_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
@swag_from({
    "tags": ["Transactions"],
    "summary": "Get a specific transaction for a product",
    "description": "Retrieves details of a single transaction by its ID.",
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "required": True,
            "type": "string",
            "description": "The unique ID of the product"
        },
        {
            "name": "transaction_id",
            "in": "path",
            "required": True,
            "type": "string",
            "description": "The unique ID of the transaction"
        }
    ],
    "responses": {
        200: {
            "description": "Transaction details",
            "examples": {
                "application/json": {
                    "id": "txn123",
                    "product_id": "product123",
                    "transaction_type": "sale",
                    "quantity": 5,
                    "total_price": 499.95,
                    "timestamp": "2025-03-27T10:00:00Z"
                }
            }
        },
        404: {"description": "Transaction not found"}
    }
})
def get_product_transaction_view(product_id, transaction_id):
    try:
        transaction = get_product_transaction(product_id, transaction_id)
        return create_resp(transaction.to_dict())
    except NotFound as e:
        abort(404, description=str(e))
