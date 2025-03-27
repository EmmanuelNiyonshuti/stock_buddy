import pytest
from werkzeug.exceptions import Unauthorized
from app import db
from app.services.auth_services import register_user, login_user


def test_register_existing_user(test_app, db_session, test_user):
    user_data = {
        "username": "john doe",
        "email": "john_doe@gmail.com",
        "password": "password123"
    }
    with pytest.raises(ValueError):
        user = register_user(db_session, user_data)

def test_login_service(test_app, test_user):
    with test_app.app_context():
        resp = login_user({"email": test_user["email"], "password": "password123"})
        assert resp["id"] == test_user["id"]

        invalid_login_details = {
            "email": test_user["email"],
            "password": "password12"
            }
        with pytest.raises(Unauthorized):
            resp = login_user(invalid_login_details)
