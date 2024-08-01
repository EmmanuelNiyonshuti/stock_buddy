from app import db
from app.models import BaseModel


class Business(BaseModel, db.Model):
    business_type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    owner_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        d = super().to_dict()
        d["business_type"] = self.business_type
        d["name"] = self.name
        d["description"] = self.description
        d["owner_id"] = self.owner_id