from flask import request
from flask import Blueprint, jsonify
from services.logic import get_indicator_value

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.post('/indicator')
def get_indicator():
    data = request.get_json() or {}
    indicator = data.get('indicator')
    if not indicator:
        return jsonify({'error': 'indicator is required'}), 400
    value = get_indicator_value(indicator)
    return jsonify({'indicator': indicator, 'value': value})
