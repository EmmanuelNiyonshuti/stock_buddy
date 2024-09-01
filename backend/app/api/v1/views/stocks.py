from flask import request, jsonify, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.api.v1.views import app_views
from app.models import Stock, Product
from app.schemas import stock_schema

@app_views.route(
                "/stocks/<uuid:stock_id>",
                methods=["GET", "PUT", "DELETE"],
                strict_slashes=False
                )
@jwt_required()
def update_stock(stock_id):
    stock = Stock.get(stock_id)
    if stock is None:
        abort(404, description="stock not found")
    if request.method == "GET":
        stock_data = stock_schema.dump(stock)
        stock_data["value"] = stock.get_stock_value()
        return jsonify(stock_data)
    if request.method == "PUT":
        if not request.is_json:
            abort(400, description="Invalid JSON")
        data = request.get_json()
        if "quantity" in data:
            try:
                stock.quantity = stock.validate_quantity("quantity", data["quantity"])
            except (TypeError, ValueError) as e:
                abort(400, description=str(e))
        for attr, val in data.items():
            if not attr  == "quantity":
                setattr(stock, attr, val)
        db.session.commit()
        return stock_schema.jsonify(stock), 200
    if request.method == "DELETE":
        try:
            db.session.delete(stock)
            db.session.commit()
            return jsonify({}), 200
        except Exception as e:
            db.session.rollback()
        return jsonify({
                        "error": "something went wrong! couldn't delete stock",
                        "details": str(e)
                        }), 500

@app_views.route("/stocks/<uuid:stock_id>/movement", methods=["POST"])
@jwt_required()
def stock_movements(stock_id):
    stock  = Stock.get(stock_id)
    if stock is None:
        abort(404, description="stock not found")
    if not request.is_json:
            abort(400, description="Invalid JSON")
    data = request.get_json()
    req_fields = ["quantity_change", "movement_type", "reason"]
    if not all(field in data for field in req_fields):
        abort(400, "Missing required fields")
    try:
        stock.record_movement(
                                data["quantity_change"],
                                data["movement_type"],
                                data["reason"]
                                )
        return stock_schema.jsonify(stock.movements), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "something went wrong!", "details": str(e)}), 500

@app_views.route("/stocks/<uuid:stock_id>/products", strict_slashes=False)
@jwt_required()
def stock_products(stock_id):
    stock = Stock.get(stock_id)
    if stock is None:
        abort(404, description="no stock found")
    return products_schema.jsonify(stock.products)

