from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.views import app_views
from app.models.business import Business
from app.services.business_services import (
                                            create_business,
                                            get_all_businesses,
                                            update_business_details,
                                            delete_business
                                            )
from app.utils.create_resp import create_resp

@app_views.route("/businesses", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_business_view():
    user_id = get_jwt_identity()
    business_details = request.get_json()
    new_business = create_business(user_id, business_details)
    return create_resp(new_business.to_dict(), 201)

@app_views.route("/businesses", methods=["GET"], strict_slashes=False)
@jwt_required()
def all_businesses_view():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    user_businesses = get_all_businesses(user_id, page, per_page)
    return create_resp(user_businesses)

@app_views.route("/businesses/<string:business_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_business_view(business_id):
    business = Business.get(business_id)
    return create_resp(business.to_dict())

@app_views.route("/businesses/<string:business_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_business_view(business_id):
    user_id = get_jwt_identity()
    business_details = request.get_json()
    updated_details = update_business_details(user_id, business_id, business_details)
    return create_resp(updated_details.to_dict())

@app_views.route("/businesses/<string:business_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_business_view(business_id):
    user_id = get_jwt_identity()
    msg = delete_business(user_id, business_id)
    return create_resp({"message": "Business deleted successfully"})
