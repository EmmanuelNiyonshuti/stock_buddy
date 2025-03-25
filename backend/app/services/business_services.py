from flask import abort
from app import db
from app.utils.required_data import require_json, require_data
from app.models.business import Business
from app.models.user import User, user_business_association
from app.utils.pagination import paginate_query

def create_business(user_id, business_details):
    user = User.get(user_id)
    require_json()
    require_data(business_details, ["name", "phone_number"], ["email", "description"])
    new_business = Business(**business_details)
    db.session.add(new_business)
    db.session.flush()
    db.session.execute(user_business_association.insert().values(
        user_id=user_id,
        business_id=new_business.id,
        role="Owner"
    ))
    db.session.commit()
    return new_business

def get_all_businesses(user_id, page, per_page):
    associations = db.session.query(user_business_association).filter_by(user_id=user_id).all()
    business_ids = [assoc.business_id for assoc in associations]
    businesses_query = Business.query.filter(Business.id.in_(business_ids))
    paginated_bsns = paginate_query(businesses_query, page, per_page)
    if not paginated_bsns["items"]:
        abort(404, description="no business associated with the user.")
    return paginated_bsns


def update_business_details(user_id, business_id, business_details):
    business = Business.get(business_id)
    require_json()
    valid_fields = {"name", "phone_number", "email", "description"}
    if any(field not in valid_fields for field in business_details):
        abort(400, f"Invalid field(s). Allowed fields: {valid_fields}")
    associations = db.session.query(user_business_association).filter_by(
    user_id=user_id, business_id=business_id, role="Owner"
    ).first()
    if not associations:
        abort(403, description="Forbidden: You are not the owner of this business")
    for k, v in business_details.items():
        setattr(business, k, v)
    db.session.commit()
    return business

def delete_business(user_id, business_id):
    business = Business.get(business_id)
    associations = db.session.query(user_business_association).filter_by(
        user_id=user_id, business_id=business_id, role="Owner"
        ).first()
    if not associations:
        abort(403, description="Forbidden: you are not the owner of this business.")
    db.session.query(user_business_association).filter_by(business_id=business_id).delete()
    db.session.delete(business)
    db.session.commit()
    return
