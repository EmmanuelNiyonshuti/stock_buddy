"""
 imports create_app function and runs the Flask application.
 """
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import(get_jwt,
                            get_jwt_identity,
                            create_access_token,
                            set_access_cookies)
from werkzeug.exceptions import NotFound, BadRequest, Forbidden, BadGateway
from flask import jsonify
from app import create_app, db 

app = create_app()

@app.errorhandler(NotFound)
def not_found_error(error):
    """
    Not found error
    """
    return jsonify(
        {
            "error": "Not found",
            "message": error.description if error.description else "resource does not exist!"
            }), 404


@app.errorhandler(Forbidden)
def forbidden_error(error):
    """ """
    return jsonify(
        {
        "error": "InsufficientPermissions.",
        "message": error.description if error.description else "You do not have permission to access this resource"
    }), 403

@app.errorhandler(BadRequest)
def badrequest_error(error):
    return jsonify(
        {
            "error": "Bad request",
            "message": error.description if error.description else  "Request body could not be read properly.",
            }), 400

@app.after_request
def refresh_exp_jwts(resp):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(resp, access_token)
        return resp
    except (RuntimeError, KeyError):
        return resp

if __name__=="__main__":
    app.run(debug=True)
