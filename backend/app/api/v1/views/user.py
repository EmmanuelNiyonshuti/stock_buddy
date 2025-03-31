from flask_jwt_extended import get_jwt_identity, jwt_required
from app.api.v1.views import app_views_bp
from app.services.user_services import user_profile
from app.utils.create_resp import create_resp

@app_views_bp.route("/users/profile", methods=["GET"], strict_slashes=False)
@jwt_required()
def user_profile_view():
    user_id = get_jwt_identity()
    user_details = user_profile(user_id)
    return create_resp(user_details)
