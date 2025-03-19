from flask import request
from flask_jwt_extended import jwt_required
from app.api.v1.views import app_views
from app.services.business_services import (
                                            create_business,
                                            update_business_details,
                                            delete_business
                                            )
from app.utils.create_resp import create_resp

@app_views.route("/businesses", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_business_view():
    business_details = request.get_json()
    new_business = create_business(business_details)
    return create_resp(new_business.to_dict(), 201)

@app_views.route("/businesses/<string:business_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_business_view(business_id):
    business = Business.get(business_id)
    return create_resp(business.to_dict())

@app_views.route("/businesses/<string:business_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_business_view(business_id):
    business_details = request.get_json()
    updated_details = update_business_details(business_id, business_details)
    return create_resp(updated_details.to_dict())

@app_views.route("/businesses/<string:business_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_business_view(business_id):
    delete_business(business_id)
    return create_resp({})