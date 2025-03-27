import pytest
from app.tests.test_helpers import assert_common_model_fields

def test_product_creation(client, setup_test_data):
    product = setup_test_data["product"]
    assert_common_model_fields(product)
    assert product.name == "Sample product"
    assert product.sku == "SP-001"
    assert product.description == "This is a sample product for testing"
    assert product.price == 20.5