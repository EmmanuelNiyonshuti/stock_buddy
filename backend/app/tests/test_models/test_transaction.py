import pytest
from app.tests.test_helpers import assert_common_model_fields

def test_transaction_creation(client, setup_test_data):
    product, transaction = setup_test_data["product"], setup_test_data["transaction"]
    assert_common_model_fields(transaction)
    assert transaction.product_id == product.id
    assert transaction.transaction_type == "Purchase"
    assert transaction.quantity == 50
    assert transaction.total_price == 1025
    
