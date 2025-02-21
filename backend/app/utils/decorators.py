from functools import wraps
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from app import db

def handle_exceptions(func):
    """
    Decorator to catch exceptions in route functions and return JSON error responses.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except HTTPException as e:
            response = jsonify({"error": e.name, "message": e.description})
            return response, e.code

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": "Database error", "message": "An internal server error", "details": str(e)}), 500

        except Exception as e:
            return jsonify({"error": "Unexpected error", "message": "An internal server error occurred.", "details": str(e)}), 500

    return wrapper

