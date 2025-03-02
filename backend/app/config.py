"""
Application Configuration

This module loads environment variables and defines the Config class, 
which sets up configurations for the Flask application, including:
- Database settings
- Mail server settings
- JWT authentication settings
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

db_username = os.getenv("MYSQL_DEV_USERNAME")
db_pwd = os.getenv("MYSQL_DEV_PWD")
db_host = os.getenv("MYSQL_DEV_HOST")
db_name = os.getenv("MYSQL_DEV_DB")

class Config:
    # SECRET_KEY=os.getenv("SECRET_KEY")
    # SECURITY_PASSWORD_SALT=os.getenv("SECURITY_PASSWORD_SALT")
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://{}:{}@{}/{}".format(db_username,
        db_pwd, db_host, db_name)

    MAIL_SERVER="smtp.googlemail.com"
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USER=os.getenv("MAIL_USER")
    MAIL_PASSWORD=os.getenv("MAIL_PWD")
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_USER")
    # WTF_CSRF_CHECK_DEFAULT=False

    # JWT_KEY_SECURE=False
    # JWT_TOKEN_LOCATION=["cookies"]
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15)
    JWT_COOKIE_CSRF_PROTECT=True
