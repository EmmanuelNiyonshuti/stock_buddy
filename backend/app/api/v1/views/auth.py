"""
Authentication routes.
"""
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.api.v1.views import app_views
from app.utils.decorators import handle_exceptions
from app.services.auth_services import register_user, login_user
from app.utils.create_resp import create_resp

@app_views.route("/users", methods=["POST"], strict_slashes=False)
@handle_exceptions
def user_registration_view():
    user_details = request.get_json()
    new_user = register_user(user_details)
    return create_resp(new_user.to_dict(), 201)

@app_views.route("/users/auth", methods=["POST"], strict_slashes=False)
@handle_exceptions
def user_login_view():
    user_details = request.get_json()
    user_tokens = login_user(user_details)
    return create_resp(user_tokens)

# @app_views.route("/auth/refresh", methods=["GET"], strict_slashes=False)
# @jwt_required(refresh=True)
# def refresh():
#     user_id = get_jwt_identity()
#     access_token = create_access_token(identity=user_id)
#     return jsonify(access_token = access_token)
