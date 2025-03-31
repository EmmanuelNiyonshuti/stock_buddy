"""
API Blueprint setup for version 1 of the application.

This module initializes the `app_views_bp` Blueprint, which serves as the central 
entry point for all API endpoints under `/api/v1`. It imports and registers 
various route handlers for different resources, including authentication, 
products, transactions, inventory, and user management.
"""
from flask import Blueprint, request, current_app
from app.utils.decorators import handle_exceptions

app_views_bp = Blueprint("app_views_bp", __name__, url_prefix="/api/v1")

@app_views_bp.before_request
def before_request():
    """
    Applies `handle_exceptions` decorator to all routes dynamically.
    """
    view_func = current_app.view_functions.get(request.endpoint)
    if view_func:
        wrapped_func = handle_exceptions(view_func)
        current_app.view_functions[request.endpoint] = wrapped_func

from app.api.v1.views.index import *
from app.api.v1.views.auth import *
from app.api.v1.views.business import *
from app.api.v1.views.user import *
from app.api.v1.views.inventory import *
from app.api.v1.views.products import *
from app.api.v1.views.transactions import *
