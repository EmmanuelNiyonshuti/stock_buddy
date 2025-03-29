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
from flasgger import Swagger
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()

def create_app(config_class=Config, testing=False):
    app = Flask(__name__)
    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_test_secret")
        app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_jwt_secret")
        app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
        app.config["JWT_ACCESS_COOKIE_NAME"] = "access_cookie"
        app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    else:
        app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger = Swagger(app, template_file=os.path.join(os.path.dirname(__file__), 'api/docs/swagger.yaml'))
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    from .api.v1.views import app_views
    app.register_blueprint(app_views)

    return app
