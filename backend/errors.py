from flask import jsonify
from app import app

class BadRequestJSON(Exception):
    def __init__(self, message='invalid request'):
        self.message = message

@app.errorhandler(BadRequestJSON)
def handle_bad_request_json(err):
    data = {'success': False, 'message': err.message}
    return jsonify(data), 400

