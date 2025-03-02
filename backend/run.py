"""
Flask application entry point.

This module imports and initializes the Flask application, registers error handlers, 
and ensures the database tables are created before running the server. 

It also includes a function to refresh JWTs automatically when their expiration time 
is near, helping maintain user sessions seamlessly.
"""
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import(get_jwt,
                            get_jwt_identity,
                            create_access_token,
                            set_access_cookies)
from app import create_app, db 
from app.error_handlers import register_error_handlers
from app.models.product import Product
from app.models.transaction import Transaction
from app.models.inventory import Inventory

app = create_app()

register_error_handlers(app)

@app.after_request
def refresh_exp_jwts(resp):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(resp, access_token)
        return resp
    except (RuntimeError, KeyError):
        return resp

if __name__== "__main__":
    with app.app_context():
        db.create_all()
        app.run()
