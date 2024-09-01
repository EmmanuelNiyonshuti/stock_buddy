from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required
from app import db
from app.api.v1.views import app_views
from app.models import Category, Product
from app.schemas import category_schema

@app_views.route("/category", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_category():
    if not request.is_json:
        abort(400, "Invalid JSON")
    data = request.get_json()
    try:
        category = Category(name=data["name"], brand=data["brand"])
        db.session.add(category)
        db.session.commit()
        return category_schema.jsonify(category), 201
    except Exception as e:
        db.session,rollback()
        return jsonify({"error": "something went wrong", "details": str(e)}), 500

@app_views.route("/category/<uuid:category_id>", strict_slashes=False)
@jwt_required()
def get_category(category_id):
    category = Category.get(category_id)
    if category is None:
        abort(404, description="Category not found")
    return category_schema.jsonify(category)
