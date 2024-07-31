from flask import request, jsonify, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.api.v1.views import app_views
from app.models import Business, User
from app.schemas import business_schema, businesses_schema, user_schema


@app_views.route("/businesses", methods=["POST"])
@jwt_required()
def create_business(): 
    curr_user_id = get_jwt_identity()
    user = User.query.get(curr_user_id)
    if not user:
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
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "couldn't create a business", "details": str(e)}), 500
    # return business_schema.jsonify(business), 201
    return jsonify(business.to_dict())


@app_views.route("/businesses/<uuid:business_id>")
@jwt_required()
def get_business(business_id):
    curr_user_id = get_jwt_identity()
    bsns = Business.query.get(business_id)
    if not bsns:
        abort(404, description="business is not found")
    if str(bsns.owner_id) != str(curr_user_id):
        abort(403)
    return business_schema.jsonify(bsns)

@app_views.route("/businesses/<uuid:business_id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_business(business_id):
    curr_user_id = get_jwt_identity()
    bsns = Business.query.get(business_id)
    if not bsns:
        abort(404)
    if str(bsns.owner_id) != str(curr_user_id):
        abort(403)
    if request.method == "PUT":
        if not request.is_json:
            abort(400)
        data = request.get_json()
        try:
            for k, v in data.items():
                setattr(bsns, k, v)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not edit the business details", "details": str(e)}), 500
        return business_schema.jsonify(bsns), 200
    elif request.method == "DELETE":
        try:
            db.session.delete(bsns)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not delete the business", "details": str(e)}), 500
        return jsonify({}), 200
