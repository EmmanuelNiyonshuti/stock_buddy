from flask import abort
from flask_jwt_extended import get_jwt_identity
from app import db
from app.models.business import Business
from app.utils.required_data import require_json, require_data
from app.models.user import User

def create_business(business_details):
    require_json()
    require_data(business_details, ["name", "phone_number"], ["email", "description"])
    user_id = get_jwt_identity()
    user = User.get(user_id)
    if not user or user.role != "Owner":
        abort(403, "you must be the owner to create a business")
    new_business = Business(
                            **business_details,
                            owner_id=user_id)
    db.session.add(new_business)
    db.session.commit()

    return new_business

def update_business_details(business_id, business_details):
    require_json()
    require_data(business_details, ["name", "phone_number"], ["email", "description"])
    user_id = get_jwt_identity()
    business = Business.query.filter_by(id=business_id, owner_id=user_id).first()
    if not business:
        abort(404, "Business not found")
    for k, v in business_details.items():
        setattr(business, k, v)
    db.session.commit()
    return business

def delete_business(business_id):
    user_id = get_jwt_identity()
    business = Business.query.filter_by(id=business_id, owner_id=user_id).first()
    if not business:
        abort(404, "Business not found")
    db.session.delete(business)
    db.session.commit()
    return {}
