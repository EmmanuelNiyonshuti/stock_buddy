from flask import request, jsonify, abort
from app.api.v1.views import app_views
from app.models.product import Product
from app import db
from app.utils.create_resp import create_resp
from app.services.product_services import (add_product,
                                           get_all_products,
                                           update_product)
from app.utils.decorators import handle_exceptions

@app_views.route("/products", methods=["POST"], strict_slashes=False)
@handle_exceptions
def add_product_view():
    product_details = request.get_json()
    new_product = add_product(product_details)
    return create_resp(new_product.to_dict(), 201)

@app_views.route("/products", methods=["GET"], strict_slashes=False)
@handle_exceptions
def get_all_products_view():
    products = get_all_products()
    return create_resp([product for product in products])

@app_views.route("/products/<string:product_id>", methods=["GET"], strict_slashes=False)
@handle_exceptions
def get_product_view(product_id):
    product = Product.get(product_id)
    return create_resp(product.to_dict())

@app_views.route("/products/<string:product_id>", methods=["PUT"], strict_slashes=False)
@handle_exceptions
def update_product_view(product_id):
    data = request.get_json()
    updated_product = update_product(product_id, data)
    return create_resp(updated_product.to_dict())

@app_views.route("/products/<string:product_id>", methods=["DELETE"], strict_slashes=False)
@handle_exceptions
def delete_product_view(product_id):
    product = Product.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return create_resp({})

