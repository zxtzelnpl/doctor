from flask import request
from flask import Blueprint, jsonify, send_file
from services.logic import get_indicator_value, get_indicators
from utils.excel import export_sheet
from utils.excel import get_sheet
from utils.doctor import match_admission_date, match_discharge_date
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.post('/indicator')
def get_indicator():
    data = request.get_json() or {}
    indicator = data.get('indicator')
    if not indicator:
        return jsonify({'error': 'indicator is required'}), 400
    value = get_indicator_value(indicator)
    return jsonify({'indicator': indicator, 'value': value})

@api_bp.get('/indicators')
def list_indicators():
    return jsonify({'indicators': get_indicators()})

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

@api_bp.get('/sheet')
def get_sheet_data():
    sheet = get_sheet("./files/2024年病案首页.xlsx", 0)
    data = sheet["data"]
    headers = sheet["headers"]

    args = request.args

    def parse_date(v):
        try:
            return datetime.strptime(v, '%Y-%m-%d')
        except Exception:
            return None

    admit_start = args.get('入院日期_start')
    admit_end = args.get('入院日期_end')
    discharge_start = args.get('出院日期_start')
    discharge_end = args.get('出院日期_end')

    admit_start_dt = parse_date(admit_start) if admit_start else None
    admit_end_dt = parse_date(admit_end) if admit_end else None
    discharge_start_dt = parse_date(discharge_start) if discharge_start else None
    discharge_end_dt = parse_date(discharge_end) if discharge_end else None

    simple_filters = {
        k: v for k, v in args.items()
        if k not in {'入院日期_start', '入院日期_end', '出院日期_start', '出院日期_end'} and v
    }

    def match_row(row):
        for k, v in simple_filters.items():
            if k not in row:
                continue
            val = '' if row.get(k) is None else str(row.get(k))
            if str(v) not in val:
                return False
        if not match_admission_date(row, admit_start_dt, admit_end_dt):
            return False
        if not match_discharge_date(row, discharge_start_dt, discharge_end_dt):
            return False
        return True

    filtered = [r for r in data if match_row(r)] if (simple_filters or admit_start_dt or admit_end_dt or discharge_start_dt or discharge_end_dt) else data
    return jsonify({"headers": headers, "data": filtered})
