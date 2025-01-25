from flask import jsonify

def bad_request(msg:str):
    respose = jsonify({'error': 'Unvalid', 'message': msg})
    respose.status_code = 400
    return respose