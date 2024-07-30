"""
 imports create_app function and runs the Flask application.
 """
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

if __name__=="__main__":
    app.run(debug=True)
