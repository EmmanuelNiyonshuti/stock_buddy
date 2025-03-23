from flask import request, abort
from app import db
from app.models.transaction import Transaction
from app.models.inventory import Inventory
from app.models.product import Product
from app.utils.required_data import require_data, require_json
from app.utils.pagination import paginate_query

def create_transaction(product_id, transaction_details):
    product = Product.get(product_id)
    require_json()
    require_data(transaction_details, ["transaction_type", "quantity", "total_price"])

    inventory = Inventory.query.filter_by(product_id=product_id).first()
    if not inventory:
        abort(400, description="No inventory found for this product. Please add inventory before recording transactions.")
    
    transaction_type = transaction_details["transaction_type"]
    quantity = transaction_details["quantity"]
    if transaction_type == "Sale" and quantity > inventory.stock_level:
        abort(400, description=f"Not enough stock available for this Sale. Available stock for {product.name}: {inventory.stock_level}")
    transaction_details["total_price"] = product.price * quantity
    inventory.update_stock_level(quantity, transaction_type)
    new_transaction = Transaction(
        **transaction_details,
        product_id=product_id
    )
    db.session.add(new_transaction)
    db.session.commit()

    return new_transaction

def get_product_transactions(page, per_page, product_id):
    product = Product.get(product_id)
    query = Transaction.query.filter_by(product_id=product_id)
    return paginate_query(query, page, per_page)

def get_product_transaction(product_id, transaction_id):
    product = Product.get(product_id)
    transaction = Transaction.query.filter_by(product_id=product_id, id=transaction_id).first()
    if not transaction:
        abort(404, description="No transaction found for product {product_id}")
    return transaction

