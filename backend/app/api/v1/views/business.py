from flask import request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound
from app import db
from app.api.v1.views import app_views
from app.utils.required_data import require_json, require_data
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
    require_json()
    business_details = request.get_json()
    require_data(business_details, ["name", "phone_number"], ["email", "description"])
    user_id = get_jwt_identity()
    new_business = create_business(db.session, user_id, business_details)
    return create_resp(new_business.to_dict(), 201)

@app_views.route("/businesses", methods=["GET"], strict_slashes=False)
@jwt_required()
def all_businesses_view():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    try:
        user_businesses = get_all_businesses(db.session, user_id, page, per_page)
        return create_resp(user_businesses)
    except NotFound as e:
        abort(404, description=str(e))

@app_views.route("/businesses/<string:business_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_business_view(business_id):
    business = Business.get(business_id)
    return create_resp(business.to_dict())

@app_views.route("/businesses/<string:business_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_business_view(business_id):
    require_json()
    user_id = get_jwt_identity()
    business = Business.get(business_id)
    business_details = request.get_json()
    try:
        updated_details = update_business_details(db.session, user_id, business_id, business_details)
        return create_resp(updated_details.to_dict())
    except BadRequest as e:
        abort(400, description=str(e))
    except Forbidden as e:
        abort(403, description=str(e))

@app_views.route("/businesses/<string:business_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_business_view(business_id):
    business = Business.get(business_id)
    user_id = get_jwt_identity()
    try:
        msg = delete_business(db.session, user_id, business_id)
        return create_resp({"message": "Business deleted successfully"})
    except Forbidden as e:
        abort(403, description=str(e))

