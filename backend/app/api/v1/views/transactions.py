from flask import request
from flask_jwt_extended import jwt_required
from app.api.v1.views import app_views
from app.services.transaction_services import (create_transaction,
                                               get_product_transactions,
                                               get_product_transaction
                                              )
from app.utils.create_resp import create_resp

@app_views.route("/products/<string:product_id>/transactions", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_transaction_view(product_id):
    transaction_details = request.get_json()
    new_transaction = create_transaction(product_id, transaction_details)
    return create_resp(new_transaction.to_dict(), 201)

@app_views.route("/products/<string:product_id>/transactions", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_product_transactions(product_id):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    transactions = get_product_transactions(page, per_page, product_id)
    return create_resp(transactions)

@app_views.route("/products/<string:product_id>/transactions/<string:transaction_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_product_transaction(product_id, transaction_id):
    transaction = get_product_transaction(product_id, transaction_id)
    return create_resp(transaction.to_dict())
