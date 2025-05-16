import pytest

def test_user_registration(client):
    user_data = {
        "username": "testuser",
        "email": "testuser@gmail.com",
        "password": "SecurePassword123"
    }
    response = client.post('/api/v1/users', json=user_data)
    assert response.status_code == 201
    response_data = response.get_json()
    assert "username" in response_data
    assert response_data["username"] == "testuser"
    assert "email" in response_data
    assert response_data["email"] == "testuser@gmail.com"

def test_invalid_email_registration(client):
    user_data = {
        "username": "testuser",
        "email": "invalid-email",
        "password": "SecurePassword123"
    }
    
    response = client.post('/api/v1/users', json=user_data)
    assert response.status_code == 400

def test_user_login(client, test_user):
    user = test_user
    user_data = {
        "email": user["email"],
        "password": "password123"
    }
    response = client.post('/api/v1/auth/login', json=user_data)
    assert response.status_code == 200
    assert response.get_json()["Success"] is True

def test_invalid_login_credentials(auth_client):
    user_data = {
        "email": "testuser@example.com",
        "password": "WrongPassword"
    }
    response = auth_client.post('/api/v1/auth/login', json=user_data)
    assert response.status_code == 401

def test_user_logout(auth_client):
    response = auth_client.post('/api/v1/auth/logout')
    assert response.status_code == 200
    assert response.get_json()["message"] == "Logged out successfully"

def test_refresh_token(auth_client):
    response = auth_client.post('/api/v1/auth/refresh')
    print('Status code:', response.status_code)
    response_data = response.get_json()
    print('Data', response_data)
    assert response.status_code == 200