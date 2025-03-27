import pytest
from app.tests.test_helpers import assert_common_model_fields

def test_inventory_creation(client, setup_test_data):
    bsns, product, inventory = setup_test_data["business"], setup_test_data["product"], setup_test_data["inventory"]
    assert_common_model_fields(inventory)
    assert inventory.stock_level == 200
    assert inventory.low_stock_alert == 20
    assert inventory.product_id == product.id
    assert inventory.business_id == bsns.id
