import pytest
from app import db, create_app
from app.models.user import User, user_business_association
from app.models.business import Business
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.transaction import Transaction
from app.models.notification import Notification
from app.services.auth_services import register_user

@pytest.fixture
def test_app():
    """Create a Flask app for testing."""
    app = create_app(testing=True)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    """Create a test client for making requests."""
    return test_app.test_client()

@pytest.fixture
def db_session(test_app):
    """Provide a database session for tests."""
    with test_app.app_context():
        yield db.session
        db.session.rollback()  # Ensure a clean state after each test

@pytest.fixture
def setup_test_data(db_session):
    """Fixture to set up initial test data, including a user and business."""
    user = User(username="user1", email="test@example.com", password="password1")
    business = Business(name="TechCorp", phone_number="078901212", email="contact@techcorp.com")

    db_session.execute(user_business_association.insert().values(
        user_id=user.id,
        business_id=business.id,
        role="Owner"
    ))
    db_session.commit()

    db_session.add_all([user, business])
    db_session.flush()  # Ensure IDs are available

    product = Product(
        name="Sample product",
        description="This is a sample product for testing",
        sku="SP-001",
        price=20.5
    )
    inventory = Inventory(
        stock_level=200,
        low_stock_alert=20,
        product_id=product.id,
        business_id=business.id
    )
    transaction = Transaction(
        transaction_type="Purchase",
        quantity=50,
        total_price=1025,
        product_id=product.id
    )

    notification = Notification(
        message="Stock is running low!",
        channel="Email",
        status="Pending",
        business_id=business.id,
        inventory_id=inventory.id
    )

    db_session.add_all([product, inventory, transaction, notification])
    db_session.commit()

    return {
        "user": user,
        "business": business,
        "product": product,
        "inventory": inventory,
        "transaction": transaction,
        "notification": notification
    }

@pytest.fixture
def test_user(db_session):
    """Fixture to create and return a registered user."""
    user_data = {
        "username": "john doe",
        "email": "john_doe@gmail.com",
        "password": "password123"
    }
    user = register_user(db_session, user_data)
    return user


@pytest.fixture
def auth_client(client, test_user):
    """Logs in a user and returns an authenticated client with cookies set."""
    login_data = {"email": test_user["email"], "password": "password123"}
    login_response = client.post('/api/v1/auth/login', json=login_data)

    assert login_response.status_code == 200

    return client
