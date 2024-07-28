from app import ma
from app.models import User, UserRole

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "id", "role")
        load_instance = True
    role = ma.Enum(UserRole)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
