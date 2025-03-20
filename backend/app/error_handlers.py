"""
Error Handlers

This module defines custom error handlers for common HTTP errors in a Flask application.
"""
from werkzeug.exceptions import (
                                NotFound,
                                BadRequest,
                                Conflict,
                                Forbidden,
                                BadGateway,
                                MethodNotAllowed,
                                Unauthorized,
                                InternalServerError
                                )
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from flask import jsonify


def internal_serrsver_error(error):
    """Handles internal server erro (500)"""
    return jsonify({
        "error": "Internal Server Error",
        "message": error.description or "An unexpected error occurred on the server."
    }), 500

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


def conflict_error(error):
    """
    Handles the 409 Conflict error. when a resource already exists (e.g., duplicate email).
    """
    return jsonify({
        "error": "Conflict",
        "message": error.description or "The requested resource already exists."
    }), 409

def method_not_allowed(error):
    return jsonify({
        "error": "Method Not allowed",
        "message": error.description if error.description else "Method not allowed."
    }), 405

def unauthorized_error(error):
    return jsonify({
        "error": "Unauthorized",
        "message": error.description if error.description else "Authentication is required to access this resource."
    }), 401

def jwt_auth_error(error):
    """Handles JWT-related authentication errors"""
    return jsonify({
        "error": "Unauthorized",
        "message": str(error)
    }), 401

def register_error_handlers(app):
    """Register all error handlers with the flask app."""
    app.register_error_handler(InternalServerError, internal_serrsver_error)
    app.register_error_handler(NotFound, not_found_error)
    app.register_error_handler(Forbidden, forbidden_error)
    app.register_error_handler(BadRequest, badrequest_error)
    app.register_error_handler(Conflict, conflict_error)
    app.register_error_handler(MethodNotAllowed, method_not_allowed)
    app.register_error_handler(Unauthorized, unauthorized_error)

    app.register_error_handler(NoAuthorizationError, jwt_auth_error)
    app.register_error_handler(InvalidHeaderError, jwt_auth_error)
