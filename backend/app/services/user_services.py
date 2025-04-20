from app.models.user import User

def user_profile(user_id):
    user = User.get(user_id)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }

def update_account(user_id):
    user = User.get(user_id)
    for k, v in user.items():
        setattr(user, k, v)
    db.session.commit()
    return user

def delete_account(user_id):
    user = User.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return
