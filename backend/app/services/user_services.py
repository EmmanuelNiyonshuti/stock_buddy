from app.models.user import User

def user_profile(user_id):
    user = User.get(user_id)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at,
    }
