from flask import jsonify


class ApiError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        result = dict()
        result['message'] = self.message
        return result

    def to_response(self):
        response = jsonify(self.to_dict())
        response.status_code = self.status_code
        return response
