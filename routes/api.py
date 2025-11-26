from flask import Blueprint, jsonify
from services.logic import get_indicator_value

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.get('/indicator/<indicator>')
def get_indicator(indicator):
    value = get_indicator_value(indicator)
    return jsonify({'indicator': indicator, 'value': value})
