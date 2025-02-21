from flask import request
from app.api.v1.views import app_views
from app.services.transaction_services import (add_transaction,
                                               get_all_transactions,
                                               get_transaction
                                              )
from app.utils.decorators import handle_exceptions
from app.utils.create_resp import create_resp

@app_views.route("/products/<string:product_id>/transactions", methods=["POST"], strict_slashes=False)
@handle_exceptions
def add_transaction_view(product_id):
    transaction_details = request.get_json()
    transaction = add_transaction(product_id, transaction_details)
    return create_resp(transaction.to_dict(), 201)

@app_views.route("/products/<string:product_id>/transactions", methods=["GET"], strict_slashes=False)
@handle_exceptions
def get_product_transactions(product_id):
    transactions = get_all_transactions(product_id)
    return create_resp(transactions)

@app_views.route("/products/<string:product_id>/transactions/<string:transaction_id>", methods=["GET"], strict_slashes=False)
@handle_exceptions
def get_product_transaction(product_id, transaction_id):
    transaction = get_transaction(product_id, transaction_id)
    return create_resp(transaction.to_dict())
