import pytest
from datetime import datetime
from app import db
from app.models.user import User, user_business_association
from app.models.business import Business
from app.tests.test_helpers import assert_common_model_fields

def test_create_user(client, setup_test_data):
    user = setup_test_data["user"]
    email = user.email
    created_user = User.query.filter_by(email="test@example.com").first()
    assert_common_model_fields(created_user)
    assert created_user.email == "test@example.com"
    assert created_user.username == "user1"

def test_create_user_email_unique(client, setup_test_data):
    user = setup_test_data["user"]
    user2 = User(username="user2", email="test@example.com", password="password2")
    db.session.add(user2)
    with pytest.raises(Exception):
        db.session.commit()

def test_user_business_relationship(client, setup_test_data):
    user, bsns = setup_test_data["user"], setup_test_data["business"]
    result = db.session.execute(
        user_business_association.select().where(
            (user_business_association.c.user_id == user.id) & 
            (user_business_association.c.business_id == bsns.id)
        )
    ).fetchone()
    assert result.user_id == user.id
    assert result.business_id == bsns.id
    assert result.role == "Owner"
