from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required
from app import db
from app.api.v1.views import app_views
from app.schemas import product_schema, products_schema
from app.models import Product, Supplier, Category

@app_views.route("/supplier", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_supplier():
    if not request.is_json:
        abort(400, "Invalid JSON")
    data = request.get_json()
    try:
        new_supplier = Supplier(
                                name=data["name"],
                                contact_info=data["contact_info"]
                                )
        db.session.add(new_supplier)
        db.session.commit()
        return supplier_schema.jsonify(supplier), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "something went wrong", "details": str(e)}), 500

@app_views.route("/supplier/<uuid:supplier_id>", strict_slashes=False)
@jwt_required()
def one_supplier(supplier_id):
    supplier = Supplier.get(supplier_id)
    if supplier is None:
        abort(404, description="supplier not found")
    return supplier_schema.jsonify(supplier)

