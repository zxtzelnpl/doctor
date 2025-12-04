from utils.excel import get_all_departments
from flask import request
from flask import Blueprint, jsonify, send_file
from services.logic import get_indicator_value, get_indicators
from utils.excel import export_sheet
from utils.excel import get_all_files_sheets
from utils.base import safe_parse_date
from utils.doctor import filter_datas, match_dates, get_date_filters
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.post('/department/list')
def get_departments_list():
    all_data = get_all_files_sheets()
    return jsonify({'departments': get_all_departments(all_data)})

@api_bp.post('/indicator/list')
def get_indicator_list():
    data_in = request.get_json(silent=True) or {}
    indicator = data_in.get('indicator') or request.args.get('indicator')
    if not indicator:
        return jsonify({'error': 'indicator is required'}), 400
    value = get_indicator_value(indicator)
    if not value or not isinstance(value.get('data'), list):
        return jsonify({'indicator': indicator, 'value': value})
  
    filtered = filter_datas(request, value['data'])
    return jsonify({'indicator': indicator, 'value': {'headers': value['headers'], 'data': filtered}})

@api_bp.get('/indicator/export')
def export_indicator():
    indicator = request.args.get('indicator')
    if not indicator:
        return jsonify({'error': 'indicator is required'}), 400
    value = get_indicator_value(indicator)
    if not value or not isinstance(value.get('data'), list):
        return jsonify({'error': 'no data for indicator'}), 404

    filtered = filter_datas(request, value['data'])

    res = export_sheet(f"{indicator}明细", value['headers'], filtered)
    return send_file(
        res['output'],
        as_attachment=True,
        download_name=res['filename'],
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@api_bp.post('/details')
def get_details():
    sheet = get_all_files_sheets()
    data = sheet["data"]
    headers = sheet["headers"]

    filtered = filter_datas(request, data)
    return jsonify({"headers": headers, "data": filtered})
