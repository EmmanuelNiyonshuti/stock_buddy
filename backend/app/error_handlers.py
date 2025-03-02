"""
Error Handlers

This module defines custom error handlers for common HTTP errors in a Flask application.
"""
from werkzeug.exceptions import (
                                NotFound,
                                BadRequest,
                                Forbidden,
                                BadGateway,
                                MethodNotAllowed
                                )
from flask import jsonify

def not_found_error(error):
    """
    Not found error
    """
    return jsonify(
        {
            "error": "Not found",
            "message": error.description if error.description else "resource does not exist!"
            }), 404

def forbidden_error(error):
    """ """
    return jsonify(
        {
        "error": "InsufficientPermissions.",
        "message": error.description if error.description else "You do not have permission to access this resource"
    }), 403

def badrequest_error(error):
    return jsonify(
        {
            "error": "Bad request",
            "message": error.description if error.description else  "Request body could not be read properly.",
            }), 400

def method_not_allowed(error):
    return jsonify({
        "error": "Method Not allowed",
        "message": error.description if error.description else "Method not allowed."
    }), 405

def register_error_handlers(app):
    """Register all error handlers with the flask app."""
    app.register_error_handler(NotFound, not_found_error)
    app.register_error_handler(Forbidden, forbidden_error)
    app.register_error_handler(BadRequest, badrequest_error)
    app.register_error_handler(MethodNotAllowed, method_not_allowed)
