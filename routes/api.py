from utils.excel import get_all_departments
from flask import request
from flask import Blueprint, jsonify, send_file
from services.logic import get_indicator_value
from services.logic import get_department_indicators
from utils.excel import export_sheet
from utils.excel import get_all_files_sheets
from utils.doctor import filter_datas
from constants.departments import departmentsByYear



api_bp = Blueprint('api', __name__, url_prefix='/api')

# 获取部门信息：根据年份返回对应科室列表
# 若年份在 departmentsByYear 配置中存在，直接返回配置；否则读取 Excel 数据动态提取
@api_bp.post('/department/list')
def get_departments_list():
    data_in = request.get_json(silent=True) or {}
    year =data_in.get('year') or request.args.get('year')
    print(year)
    if not year:
        return jsonify({'error': 'year is required'}), 400
    
    if year in departmentsByYear:
        print(departmentsByYear[year])
        return jsonify({'departments': departmentsByYear[year]})
    else:
        all_data = get_all_files_sheets(year)
        return jsonify({'departments': get_all_departments(all_data["data"])})

# 获取指标信息：根据年份和科室返回指标列表
@api_bp.post('/indicators')
def get_indicators_api():
    data_in = request.get_json(silent=True) or {}
    year = data_in.get('year') or request.args.get('year')
    department = data_in.get('department') or request.args.get('department') or data_in.get('出院科室') or request.args.get('出院科室')
    if not year or not department:
        return jsonify({'error': 'year and department are required'}), 400
    indicators = get_department_indicators(str(year), str(department))
    return jsonify({'indicators': indicators})

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
    data_in = request.get_json(silent=True) or {}
    year = data_in.get('year') or request.args.get('year')
    if not year:
        return jsonify({'error': 'year is required'}), 400
    sheet = get_all_files_sheets(year)
    data = sheet["data"]
    headers = sheet["headers"]

    filtered = filter_datas(request, data)
    return jsonify({"headers": headers, "data": filtered})
