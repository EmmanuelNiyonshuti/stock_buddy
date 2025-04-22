import pytest
from werkzeug.exceptions import Forbidden
from app.services.transaction_services import (
                                                create_transaction,
                                                get_product_transactions,
                                                get_product_transaction
                                              )

def test_create_transaction(db_session, setup_test_data):
    user, product = setup_test_data["user"], setup_test_data["product"]
    transaction_details = {
        "transaction_type":"Sale",
        "quantity":20,
        "total_price":410
    }
    new_transaction = create_transaction(db_session, user.id, product.id, transaction_details)
    assert new_transaction.transaction_type == "Sale"
    assert new_transaction.quantity == 20
    assert new_transaction.total_price == 410

def test_create_transaction_random_user(db_session, test_user, setup_test_data):
    user = test_user
    product = setup_test_data["product"]
    transaction_details = {
        "transaction_type":"Sale",
        "quantity":20,
        "total_price":410
    }
    with pytest.raises(Forbidden):
        new_transaction = create_transaction(db_session, user["id"], product.id, transaction_details)

def test_get_product_transactions(db_session, setup_test_data):
    product, user = setup_test_data["product"], setup_test_data["user"]
    transactions = get_product_transactions(db_session, user.id, product.id, page=1, per_page=10)
    assert len(transactions["items"]) > 0

