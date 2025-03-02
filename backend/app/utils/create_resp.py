"""
Utility module for creating standardized JSON responses.

This module provides a helper function to return JSON responses with 
a specified HTTP status code, ensuring consistency in API responses.
"""

from flask import jsonify
def create_resp(data, status_code=200):
    """Returns a JSON response with the given data and status code."""
    return jsonify(data), status_code
