from flask import jsonify, request

def create_response(data, status_code=200):
    return jsonify(data), status_code

def get_ticker_from_json():
    try:
        data = request.get_json()
        if not data:
            return None, 'Invalid JSON'
        ticker = data.get('ticker') if isinstance(data, dict) else data
        return ticker, None
    except Exception:
        return None, 'Invalid request format'
