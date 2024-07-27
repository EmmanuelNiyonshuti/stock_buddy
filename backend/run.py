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
    return jsonify({"error": "Not found"}), 404


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
