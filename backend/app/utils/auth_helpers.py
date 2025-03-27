from flask import jsonify
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                set_access_cookies,
                                set_refresh_cookies,
                                unset_jwt_cookies,
                                jwt_required
                                )


def create_auth_response(user_data, message={"Success": True}, status=200):
    """
    Generates a JSON response with JWT access and refresh tokens stored in HttpOnly cookies.
    """
    access_token = create_access_token(identity=user_data["id"])
    refresh_token = create_refresh_token(identity=user_data["id"])

    response = jsonify(message)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, status

def create_logout_response(message="Logged out successfully"):
    """
    Clears JWT cookies on logout.
    """
    response = jsonify({"message": message})
    unset_jwt_cookies(response)
    return response
