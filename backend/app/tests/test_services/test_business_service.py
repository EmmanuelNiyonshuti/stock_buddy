import pytest
from werkzeug.exceptions import NotFound, Forbidden, BadRequest
from app.services.business_services import (
                                            create_business,
                                            get_all_businesses,
                                            update_business_details,
                                            delete_business
                                            )
from app.models.user import User
from app.models.business import Business

def test_create_business(db_session, test_user):
    business_data = {
        "name": "NewCorp",
        "phone_number": "078901213",
        "email": "contact@newcorp.com"
    }
    new_business = create_business(db_session, test_user["id"], business_data)
    assert new_business is not None
    assert new_business.name == "NewCorp"
    assert new_business.phone_number == "078901213"
    assert new_business.email == "contact@newcorp.com"
    assert new_business.description is None

def test_get_all_businesses(db_session, test_user, setup_test_data):
    user, business = setup_test_data["user"], setup_test_data["business"]
    businesses = get_all_businesses(db_session, user.id, page=1, per_page=10)
    assert len(businesses["items"]) > 0

def test_get_all_businesses_not_found(db_session, test_user):
    user = test_user
    with pytest.raises(NotFound):
        businesses = get_all_businesses(db_session, user["id"], page=1, per_page=10)
        assert len(businesses["items"]) > 0

def test_update_business_details(db_session, setup_test_data):
    user = setup_test_data["user"]
    business_data = {
        "name": "NewCorp",
        "phone_number": "078901213",
        "email": "contact@newcorp.com"
    }
    business = create_business(db_session, user.id, business_data)
    assert business is not None
    updated_details = {
        "name": "Updated TechCorp",
        "phone_number": "078901213",
        "email": "new_contact@techcorp.com"
    }

    updated_business = update_business_details(db_session, user.id, business.id, updated_details)

    assert updated_business.name == "Updated TechCorp"
    assert updated_business.phone_number == "078901213"
    assert updated_business.email == "new_contact@techcorp.com"

def test_update_business_invalid_field(db_session, setup_test_data):
    user, business = setup_test_data["user"], setup_test_data["business"]

    invalid_details = {
        "name": "Invalid Business",
        "invalid_field": "Some value"
    }

    with pytest.raises(BadRequest, match="Invalid field"):
        update_business_details(db_session, user.id, business.id, invalid_details)

def test_update_business_not_owner(db_session, setup_test_data):
    user, business = setup_test_data["user"], setup_test_data["business"]
    other_user = User(username="other_user", email="other@example.com", password="password")
    db_session.add(other_user)
    db_session.commit()

    updated_details = {"name": "Unauthorized Change"}

    with pytest.raises(Forbidden, match="Forbidden: You are not the owner"):
        update_business_details(db_session, other_user.id, business.id, updated_details)

def test_delete_business(db_session, setup_test_data):
    owner, business = setup_test_data["user"], setup_test_data["business"]
    delete_business(db_session, owner.id, business.id)
    deleted_businesss = db_session.query(Business).filter_by(id=business.id).first()
    assert deleted_businesss is None

def test_delete_business_not_owner(db_session, test_user, setup_test_data):
    user = test_user
    business = setup_test_data["business"]
    with pytest.raises(Forbidden):
        delete_business(db_session, user["id"], business.id)
