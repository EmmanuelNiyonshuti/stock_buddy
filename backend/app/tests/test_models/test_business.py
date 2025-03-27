import pytest
from datetime import datetime
from app import db
from app.models.business import Business
from app.tests.test_helpers import assert_common_model_fields

def test_create_business(client, setup_test_data):
    bsns = setup_test_data["business"]
    assert_common_model_fields(bsns)
    assert bsns.name == "TechCorp"
    assert bsns.email == "contact@techcorp.com"
    assert bsns.phone_number == "078901212"
    assert bsns.description == None

def test_business_email_unique(client, setup_test_data):
    bsn1 = setup_test_data["business"]
    bsns2 = Business(name="Biz2", email="contact@techcorp.com")

    db.session.add(bsns2)
    with pytest.raises(Exception):
        db.session.commit()
