from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required
from app import db
from app.api.v1.views import app_views
from app.schemas import product_schema, products_schema
from app.models import Product, Supplier, Category

@app_views.route("/products", methods=["POST"], strict_slashes=False)
@jwt_required()
def product():
    if not request.is_json:
        abort(400, "Invalid JSON")
    supplier = Supplier.get(supplier_id)
    if supplier is None:
        abort(404, description="product supplier not found")
    category = Category.get(category_id)
    if category is None:
        abort(404, description="product category not found")
    data = request.get_json()
    req_fields = ["name", "description", "unit_cost", "category_id", "supplier_id"]
    if not all(field in data for field in req_fields):
        abort(400, description="Missing required fields")
    try:
        new_product = Product(
                            name=data["name"],
                            description=data["description"],
                            size=data["size"],
                            weight=data["weight"],
                            sku=data["sku"],
                            unit_cost=data["unit_cost"],
                            is_active=data["is_active"],
                            expiry_date=data["expiry_date"],
                            is_perishable=data["is_perishable"],
                            supplier = supplier,
                            category = category
                            )
        db.session.add(new_product)
        db.session.commit()
        return product_schema.jsonify(product), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "something went wrong", "details": str(e)}), 500


@app_views.route("/products/<uuid:product_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
@jwt_required()
def update_product(product_id):
    product = Product.get(product_id)
    if product is None:
        abort(404, description="Product not found")
    if request.method == "GET":
        return product_schema.jsonify(product)
    elif request.method == "PUT":
        if not request.is_json:
            abort(400, description="Invalid JSON")
        data = request.get_json()
        for attr, val in data.items():
            setattr(product, attr, val)
        try:
            db.session.commit()
            return product_schema.jsonify(product)
        except Exception as e:
            return jsonify({"error": "something went wrong", "details": str(e)}), 500
    elif request.method == "DELETE":
        try:
            db.session.delete(product)
            db.session.commit()
            return jsonify({}), 200
        except Exception as e:
            return jsonify({"error": "something went wrong", "details": str(e)}), 500

