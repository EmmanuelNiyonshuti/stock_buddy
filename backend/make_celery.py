"""
Celery Initialization

This module sets up Celery with the Flask app. It initializes the Flask app using 
`create_app()`, imports tasks from `app.tasks`, and connects Celery via Flask's
extensions to handle background tasks.
"""

from app import create_app
from app.tasks import *

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
