from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from app.api.v1.views.index import *
from app.api.v1.views.users import *
from app.api.v1.views.business import *
