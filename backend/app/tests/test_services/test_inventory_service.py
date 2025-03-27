import pytest
from werkzeug.exceptions import Forbidden, NotFound
from app.services.inventory_services import (
                                            add_inventory, get_business_inventories
                                            )
from app.models.inventory import Inventory
from app.models.user import user_business_association

def test_add_inventory(db_session, setup_test_data):
    """Test adding inventory when user is properly associated with the business."""
    user, business, product = (
        setup_test_data["user"],
        setup_test_data["business"],
        setup_test_data["product"],
    )
    inventory_data = {
        "stock_level": 100,
        "low_stock_alert": 10,
        "product_id": product.id,
    }
    new_inventory = add_inventory(db_session, user.id, business.id, inventory_data)
    assert new_inventory is not None
    assert new_inventory.business_id == business.id
    assert new_inventory.stock_level == 100
    assert new_inventory.low_stock_alert == 10

def test_add_inventory_without_association(db_session, test_user, setup_test_data):
    """Test adding inventory when user is NOT associated with any business."""
    user = test_user

    inventory_data = {
        "stock_level": 50,
        "low_stock_alert": 5,
        "product_id": setup_test_data["product"].id,
    }

    with pytest.raises(Forbidden, match="No associated business"):
        add_inventory(db_session, user["id"], setup_test_data["business"].id, inventory_data)

def test_get_business_inventories(db_session, setup_test_data):
    """Test retrieving paginated inventories for a business."""
    user, business, product = (
        setup_test_data["user"],
        setup_test_data["business"],
        setup_test_data["product"],
    )
    inventory1 = Inventory(stock_level=100, low_stock_alert=10, product_id=product.id, business_id=business.id)
    inventory2 = Inventory(stock_level=200, low_stock_alert=20, product_id=product.id, business_id=business.id)
    db_session.add_all([inventory1, inventory2])
    db_session.commit()

    result = get_business_inventories(page=1, per_page=10, business_id=business.id)
    assert len(result["items"]) == 3

