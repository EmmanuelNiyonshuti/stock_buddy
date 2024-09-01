from flask import jsonify
from app.api.v1.views import app_views
@app_views.route("/status", methods=["GET"], strict_slashes=False)
def stat():
    """
    returns the status of the api.
    """
    return jsonify({
        "status": "OK"
    }), 200