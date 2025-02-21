from flask import request, abort
from app import db
from app.models.transaction import Transaction
from app.models.inventory import Inventory
from app.models.product import Product
from app.utils.required_data import require_data, require_json
from app.utils.pagination import paginate_query

def add_transaction(product_id, transaction_details):
    product = Product.get(product_id)
    if not product:
        abort(404, description=f"product with id {product_id} does not exist")
    require_json()
    require_data(transaction_details, ["transaction_type", "quantity", "total_price"])
    inventory = Inventory.query.filter_by(product_id=product_id).first()
    if not inventory:
        abort(404, description=f"stock for product with id {product_id} not found")
    new_transaction = Transaction(
                                  product_id=product_id,
                                  **transaction_details
                                  )
    db.session.add(new_transaction)
    db.session.commit()
    inventory.update_stock_level(new_transaction.quantity, new_transaction.transaction_type)

    return new_transaction

def get_all_transactions(product_id):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    query = Transaction.query.filter_by(product_id=product_id)
    return paginate_query(query, page, per_page)

def get_transaction(product_id, transaction_id):
    transaction = Transaction.query.filter_by(product_id=product_id, id=transaction_id).first()
    if not transaction:
        abort(404, description="Transaction not found")
    return transaction

