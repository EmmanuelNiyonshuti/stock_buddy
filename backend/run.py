"""
Flask application entry point.

This module imports and initializes the Flask application, registers error handlers. 
"""
import os
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
        app.run(
            host=os.getenv("APP_HOST", "127.0.0.1"),
            port=int(os.getenv("APP_PORT", 5000)),
            debug=bool(os.getenv("APP_MODE", False)),
            )
