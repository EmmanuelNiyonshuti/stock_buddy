from flask import request
from app.api.v1.views import app_views
from app.services.transaction_services import add_transaction
from app.utils.decorators import handle_exceptions
from app.utils.create_resp import create_resp

@app_views.route("/products/<product_id>/transactions", methods=["POST"], strict_slashes=False)
@handle_exceptions
def add_transaction_view(product_id):
    transaction_details = request.get_json()
    transaction = add_transaction(product_id, transaction_details)
    return create_resp(transaction.to_dict(), 201)
