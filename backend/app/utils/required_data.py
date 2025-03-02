"""
This module provides helper functions to ensure incoming JSON requests 
are properly formatted and contain the required fields before processing.
"""
from flask import request, abort

def require_json():
    if not request.is_json:
        abort(400, description="Bad Request: Invalid JSON")

def require_data(data, required_fields, optional_fields=None):
    """
    Validate that all required fields are present in the request data.
    - `data`: The JSON request payload.
    - `required_fields`: List of required field names.
    - `optional_fields`: List of optional field names (default: None).
    """
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        abort(400, description=f"Missing required fields: {', '.join(missing_fields)}")

    optional_fields = optional_fields or []

    allowed_fields = set(required_fields + optional_fields)
    extra_fields = [field for field in data if field not in allowed_fields]

    if extra_fields:
        abort(400, description=f"Unexpected fields found: {', '.join(extra_fields)}")
