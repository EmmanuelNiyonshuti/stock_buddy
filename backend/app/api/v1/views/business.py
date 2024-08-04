from flask import request, jsonify, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.api.v1.views import app_views
from app.models import Business, User
from app.schemas import (business_schema, businesses_schema,
                        user_schema, stocks_schema)

@app_views.route("/businesses", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_business(): 
    """ Create a business """
    curr_user_id = get_jwt_identity()
    user = User.get(curr_user_id)
    if user is None:
        abort(404, description="User not found")
    if not request.is_json:
        abort(400, description="Invalid JSON")
    data = request.get_json()
    req_fields = ["business_type", "name", "description"]
    for field in req_fields:
        if field not in data:
            abort(400, description="Missing {} field".format(field))
    try:
        business = Business(
            business_type= data["business_type"],
            name=data["name"],
            description=data["description"],
            owner=user,
        )
        db.session.add(business)
        db.session.commit()
        return business_schema.jsonify(business)
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "couldn't create a business", "details": str(e)}), 500

@app_views.route("/businesses/<uuid:business_id>", strict_slashes=False)
@jwt_required()
def get_business(business_id):
    """ retrieve a business"""
    curr_user_id = get_jwt_identity()
    business = Business.get(business_id)
    if business is None:
        abort(404, description="business is not found")
    if str(business.owner_id) != str(curr_user_id):
        abort(403, description="you don't have the required permissions to access this resource!")
    return business_schema.jsonify(business)

@app_views.route("/businesses/<uuid:business_id>", methods=["PUT", "DELETE"], strict_slashes=False)
@jwt_required()
def update_business(business_id):
    """ update or delete a business """
    curr_user_id = get_jwt_identity()
    business = Business.get(business_id)
    if business is None:
        abort(404)
    if str(business.owner_id) != str(curr_user_id):
        abort(403)
    if request.method == "PUT":
        if not request.is_json:
            abort(400, description="Invalid JSON")
        data = request.get_json()
        try:
            for k, v in data.items():
                setattr(business, k, v)
            db.session.commit()
            return business_schema.jsonify(business), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not edit the business details", "details": str(e)}), 500
    elif request.method == "DELETE":
        try:
            db.session.delete(business)
            db.session.commit()
            return jsonify({}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not delete the business", "details": str(e)}), 500

@app_views.route("/business/<uuid:business_id>/stocks", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_stock(business_id):
    """ create a stock """
    business = Business.get(business_id)
    if business is None:
        abort(404, description="business not found")
    if not request.is_json:
        abort(400, description="Invalid JSON")
    data = request.get_json()
    if "quantity" not in data:
        return jsonify({"error": "Missing a required field"})
    try:
        new_stock = Stock(
                        data["quantity"],
                        business=business,
                        location=business.location
                        )
        db.session.add(new_stock)
        db.session.commit()
        return stock_schema.jsonify(new_stock), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
                        "error": "something went wrong! couldn't create a stock",
                        "details": str(e)
                        }), 500

@app_views.route("/business/<uuid:business_id>/stocks", strict_slashes=False)
@jwt_required()
def all_stocks(business_id):
    """ retrieve all stocks of a particular business"""
    business = Business.get(business_id)
    if business is None:
        abort(404, description="business not found")
    return stocks_schema.jsonify(business.stocks)
