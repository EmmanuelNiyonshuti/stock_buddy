from flask import jsonify
def create_resp(data, status_code=200):
    return jsonify(data), status_code
