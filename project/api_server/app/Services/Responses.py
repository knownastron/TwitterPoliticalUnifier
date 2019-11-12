# import sys
# sys.path.append('../../')
# from app import app

from flask import jsonify, request

# @app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

# @app.errorhandler(401)
def auth_error(error=None):
    message = {
        'status': 401,
        'message': 'Authentication Error'
    }
    resp = jsonify(message)
    resp.status_code = 401

    return resp
