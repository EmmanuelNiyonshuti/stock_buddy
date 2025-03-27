import pytest
from app.tests.test_helpers import assert_common_model_fields

def test_notification_creation(client, setup_test_data):
    bsns, inventory, notification = setup_test_data["business"], setup_test_data["inventory"], setup_test_data["notification"]
    assert_common_model_fields(notification)
    assert notification.message == "Stock is running low!"
    assert notification.channel == "Email"
    assert notification.status == "Pending"
    assert notification.business_id == bsns.id
    assert notification.inventory_id == inventory.id