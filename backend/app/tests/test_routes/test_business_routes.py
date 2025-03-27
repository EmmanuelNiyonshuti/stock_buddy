import pytest
from app.models.user import user_business_association
from werkzeug.exceptions import NotFound
from app.models.business import Business


BUSINESS_DATA = {
    "name": "My Business",
    "phone_number": "+250787654321",
    "email": "mybiz@gmail.com",
    "description": "Business description."
    }

def test_create_business(auth_client):
    """Test creating a new business."""
    response = auth_client.post('/api/v1/businesses', json=BUSINESS_DATA)
    
    assert response.status_code == 201
    assert response.get_json()["name"] == BUSINESS_DATA["name"]

def test_get_all_businesses(auth_client):
    """Test retrieving all businesses."""
    response = auth_client.get('/api/v1/businesses')
    if response.status_code == 404:
        assert response.get_json() is None
    else:
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)


def test_get_single_business(auth_client):
    """Test retrieving a single business."""
    create_response = auth_client.post('/api/v1/businesses', json=BUSINESS_DATA)
    business_id = create_response.get_json().get("id")

    response = auth_client.get(f'/api/v1/businesses/{business_id}')
    
    assert response.status_code == 200
    assert response.get_json()["name"] == BUSINESS_DATA["name"]


def test_update_business(auth_client):
    """Test updating an existing business."""
    create_response = auth_client.post('/api/v1/businesses', json=BUSINESS_DATA)
    business_id = create_response.get_json().get("id")

    update_data = {"name": "Updated Name", "phone_number": "+250788654321"}
    response = auth_client.put(f'/api/v1/businesses/{business_id}', json=update_data)

    assert response.status_code == 200
    assert response.get_json()["name"] == "Updated Name"


def test_delete_business(auth_client):
    """Test deleting a business."""
    create_response = auth_client.post('/api/v1/businesses', json=BUSINESS_DATA)
    business_id = create_response.get_json().get("id")

    response = auth_client.delete(f'/api/v1/businesses/{business_id}')

    assert response.status_code == 200
    assert response.get_json()["message"] == "Business deleted successfully"



    

