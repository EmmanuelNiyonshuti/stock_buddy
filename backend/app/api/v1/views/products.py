from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.api.v1.views import app_views
from app.models.product import Product
from app import db
from app.utils.create_resp import create_resp
from app.services.product_services import (add_product,
                                           get_all_products,
                                           update_product)

@app_views.route("/products", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_product_view():
    require_json()
    require_data(product_details, ["name", "price", "sku"], ["description"])
    user_id = get_jwt_identity()
    product_details = request.get_json()
    try:
        new_product = add_product(db.session, user_id, product_details)
        return create_resp(new_product.to_dict(), 201)
    except Unauthorized as e:
        abort(401, description=str(e))

@app_views.route("/products", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_all_products_view():
    products = get_all_products()
    return create_resp(products)

@app_views.route("/products/<string:product_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_product_view(product_id):
    product = Product.get(product_id)
    return create_resp(product.to_dict())

@app_views.route("/products/<string:product_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_product_view(product_id):
    require_json()
    data = request.get_json()
    updated_product = update_product(db.session, product_id, data)
    return create_resp(updated_product.to_dict())

@app_views.route("/products/<string:product_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_product_view(product_id):
    product = Product.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return create_resp({})

