from werkzeug.exceptions import BadRequest, Forbidden, NotFound
from app.models.business import Business
from app.models.user import User, user_business_association
from app.utils.pagination import paginate_query

def create_business(db_session, user_id, business_details):
    new_business = Business(**business_details)
    db_session.add(new_business)
    db_session.flush()
    db_session.execute(user_business_association.insert().values(
        user_id=user_id,
        business_id=new_business.id,
        role="Owner"
    ))
    db_session.commit()
    return new_business

def get_all_businesses(db_session, user_id, page, per_page):
    associations = db_session.query(user_business_association).filter_by(user_id=user_id).all()
    business_ids = [assoc.business_id for assoc in associations]
    businesses_query = Business.query.filter(Business.id.in_(business_ids))
    paginated_bsns = paginate_query(businesses_query, page, per_page)
    if not paginated_bsns["items"]:
        raise NotFound("no business associated with the user.")
    return paginated_bsns

def update_business_details(db_session, user_id, business_id, business_details):
    valid_fields = {"name", "phone_number", "email", "description"}
    if any(field not in valid_fields for field in business_details):
        raise BadRequest(f"Invalid field(s). Allowed fields: {valid_fields}")
    associations = db_session.query(user_business_association).filter_by(
    user_id=user_id, business_id=business_id, role="Owner"
    ).first()
    if not associations:
        raise Forbidden("Forbidden: You are not the owner of this business")
    for k, v in business_details.items():
        setattr(business, k, v)
    db_session.commit()
    return business

def delete_business(db_session, user_id, business_id):
    associations = db.session.query(user_business_association).filter_by(
        user_id=user_id, business_id=business_id, role="Owner"
        ).first()
    if not associations:
        raise Forbidden("Forbidden: you are not the owner of this business.")
    db_session.query(user_business_association).filter_by(business_id=business_id).delete()
    db_session.delete(business)
    db_session.commit()
    return
