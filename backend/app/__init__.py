"""
Flask application factory.

This module sets up the Flask application, configures extensions, and registers blueprints. 
It follows the application factory pattern, allowing flexibility in configuration and testing.

Configured extensions:
- SQLAlchemy (database ORM)
- Flask-Login (user session management)
- Bcrypt (password hashing)
- Flask-Migrate (database migrations)
- Flask-CORS (Cross-Origin Resource Sharing)
- Flask-JWT-Extended (JWT-based authentication)
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    from .api.v1.views import app_views
    app.register_blueprint(app_views)

    return app
