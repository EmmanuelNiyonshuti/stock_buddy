from werkzeug.exceptions import BadRequest, Forbidden
from app.models.user import user_business_association
from app.models.transaction import Transaction
from app.models.inventory import Inventory
from app.models.product import Product
from app.utils.required_data import require_data, require_json
from app.utils.pagination import paginate_query

def create_transaction(db_session, user_id, product_id, transaction_details):
    inventory = Inventory.query.filter_by(product_id=product_id).first()
    if not inventory:
        raise BadRequest("No inventory found for this product. Please add inventory before recording transactions.")
    associated_business = db_session.query(user_business_association).filter_by(
                                                                                user_id=user_id, business_id=inventory.business_id
                                                                                ).first()
    if not associated_business:
        raise Forbidden("Forbidden: You are not associated with this business to add a transaction")
    transaction_type = transaction_details["transaction_type"]
    quantity = transaction_details["quantity"]
    if transaction_type == "Sale" and quantity > inventory.stock_level:
        raise BadRequest(f"Not enough stock available for this Sale. Available stock for {product.name}: {inventory.stock_level}")
    product = Product.get(product_id)
    transaction_details["total_price"] = product.price * quantity
    inventory.update_stock_level(db_session, quantity, transaction_type)
    new_transaction = Transaction(
        **transaction_details,
        product_id=product_id
    )
    db_session.add(new_transaction)
    db_session.commit()
    return new_transaction

def get_product_transactions(db_session, user_id, product_id, page, per_page):
    product = Product.get(product_id)
    associated_business = db_session.query(user_business_association).filter_by(user_id=user_id).first()
    if not associated_business:
        raise Forbidden("Forbidden: You are not associated with this business")
    query = Transaction.query.filter_by(product_id=product_id)
    return paginate_query(query, page, per_page)

def get_product_transaction(product_id, transaction_id):
    product = Product.get(product_id)
    transaction = Transaction.query.filter_by(product_id=product_id, id=transaction_id).first()
    if not transaction:
        raise NotFound("No transaction found for product {product_id}")
    return transaction
