from flask import request
from flask import Blueprint, jsonify, send_file
from services.logic import get_indicator_value
from utils.excel import export_sheet

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.post('/indicator')
def get_indicator():
    data = request.get_json() or {}
    indicator = data.get('indicator')
    if not indicator:
        return jsonify({'error': 'indicator is required'}), 400
    value = get_indicator_value(indicator)
    return jsonify({'indicator': indicator, 'value': value})

@api_bp.get('/indicator/export')
def export_indicator():
    indicator = request.args.get('indicator')
    if not indicator:
        return jsonify({'error': 'indicator is required'}), 400
    value = get_indicator_value(indicator)
    if not value or not isinstance(value.get('data'), list):
        return jsonify({'error': 'no data for indicator'}), 404
    res = export_sheet(f"{indicator}明细", value['headers'], value['data'])
    return send_file(
        res['output'],
        as_attachment=True,
        download_name=res['filename'],
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
