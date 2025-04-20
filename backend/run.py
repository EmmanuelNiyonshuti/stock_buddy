"""
Flask application entry point.

This module imports and initializes the Flask application, registers error handlers. 
"""
from app.error_handlers import register_error_handlers
from app.models.user import User
from app.models.business import Business
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.transaction import Transaction
from app.models.notification import Notification
from app import create_app, db 

app = create_app()
register_error_handlers(app)

if __name__== "__main__":
    with app.app_context():
        app.run()
