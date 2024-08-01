from flask import request, jsonify, abort
from flask_jwt_extended import jwt_identity, jwt_required
from app import db
from app.api.v1.views import app_views
from app.models import Stock, Product
from app.schemas import stock_schema


@app_views.route("/stocks/<uuid:stock_id>")
@jwt_required()
def one_stock(stock_id):
    stock = Stock.get(stock_id)
    if stock is None:
        abort(404, description="stock not found")
    return stock_schema.jsonify(stock)

@app_views.route("stocks/<uuid:stock_id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_stock(stock_id):
    stock = Stock.get(stock_id)
    if stock is None:
        abort(404, description="stock not found")
    if request.method == "PUT":
        if not request.is_json:
            abort(400, description="Invalid JSON")
        data = request.get_json()
        for attr, val in data.items():
            setattr(stock, attr, val)
        db.session.commit()
        return stock_schema.jsonify(stock)
    elif request.method == "DELETE":
        try:
            db.session.delete(stock)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return jsonify({
                        "error": "something went wrong! couldn't delete stock",
                        "details": str(e)
                        }), 500
        return jsonify({}), 200