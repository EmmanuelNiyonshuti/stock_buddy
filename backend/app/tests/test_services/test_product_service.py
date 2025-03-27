import pytest
from werkzeug.exceptions import Forbidden
from app.services.product_services import (
                                            add_product,
                                            get_all_products,
                                            update_product
                                            )

def test_add_product(db_session, setup_test_data):
    user = setup_test_data["user"]
    product_details = {
        "name": "Sample product2",
        "description": "This is a sample product2 for testing",
        "sku": "SP-002",
        "price": 25
    }
    new_product = add_product(db_session, user.id, product_details)
    assert new_product is not None
    assert new_product.name == "Sample product2"
    assert new_product.description == "This is a sample product2 for testing"
    assert new_product.sku == "SP-002"
    assert new_product.price == 25

def test_get_all_product(db_session, setup_test_data):
    user, business = setup_test_data["user"], setup_test_data["business"]
    products = get_all_products(db_session, user.id, business.id, page=1, per_page=10)
    assert len(products["items"]) > 0

def test_get_all_product_random_user(db_session, setup_test_data, test_user):
    rand_user = test_user
    business = setup_test_data["business"]
    with pytest.raises(Forbidden):
        products = get_all_products(db_session, rand_user["id"], business.id, page=1, per_page=10)

def test_update_product(db_session, setup_test_data):
    user, business, product = setup_test_data["user"], setup_test_data["business"], setup_test_data["product"]
    product_details = {
        "name": "Updated Sample product2",
        "description": "Updated description",
        "sku": "Updated sku",
        "price": 23
    }
    updated_product = update_product(db_session, user.id, business.id, product.id, product_details)
    assert updated_product.name ==  "Updated Sample product2"
    assert updated_product.description ==  "Updated description"
    assert updated_product.sku ==  "Updated sku"
    assert updated_product.price ==  23


def test_update_product_not_owner(db_session, test_user, setup_test_data):
    rand_user = test_user
    business, product = setup_test_data["business"], setup_test_data["product"]
    product_details = {
        "name": "Updated Sample product2",
        "description": "Updated description",
        "sku": "Updated sku",
        "price": 23
    }
    with pytest.raises(Forbidden):
        updated_product = update_product(db_session, rand_user["id"], business.id, product.id, product_details)
