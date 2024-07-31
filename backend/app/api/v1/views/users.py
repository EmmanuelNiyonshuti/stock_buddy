from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.api.v1.views import app_views
from app.models import User, Business
from app.schemas import user_schema, users_schema

@app_views.route("/users/<uuid:user_id>")
@jwt_required()
def get_user(user_id):
    curr_user_id = get_jwt_identity()
    if str(curr_user_id) != str(user_id):
        abort(403, description="Retrieving a user requires you to be that 'user'or 'admin'.")
    user = User.query.get(user_id)
    if not user:
        abort(404, description="user not found")
    return jsonify(user.to_dict()), 200

@app_views.route("/users/<uuid:user_id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_user(user_id):
    curr_user_id = get_jwt_identity()
    if str(curr_user_id) != str(user_id):
        abort(403, description="Updating user info requires you to be that 'user'.")
    user = User.query.get(user_id)
    if request.method == "PUT":
        if not request.is_json:
            abort(400, description="Invalid JSON")
        data = request.get_json()
        try:
            for attr, val in data.items():
                setattr(user, attr, val)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "could not update user info", "details": str(e)}), 500
        return jsonify(user.to_dict()), 200
    elif request.method == "DELETE":
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "could not delete the user", "details": str(e)}), 500
        return jsonify({}), 200




@app_views.route("/users/<uuid:user_id>/business")
@jwt_required()
def user_business(user_id):
    curr_user_id = get_jwt_identity()
    if str(user_id) != str(curr_user_id):
        abort(403, description="You don't have the permission to access the requested resource")
    user = User.query.get(user_id)
    user_roles = ["owner", "admin", "manager", "employee"]
    if user.role in user_roles:
        abort(403, description="You don't have the permission to access the requested resource")
    return businesses_schema.jsonify(user.business)
