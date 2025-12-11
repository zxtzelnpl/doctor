from utils.base import safe_parse_data
from utils.json import get_all_files_jsons
from flask import request
from flask import Blueprint, jsonify, send_file
from services.logic import get_all_departments, get_indicator_detail
from services.logic import get_department_indicators
from utils.excel import export_sheet

api_bp = Blueprint('api', __name__, url_prefix='/api')

# 获取部门信息：根据年份返回对应科室列表
# 若年份在 departmentsByYear 配置中存在，直接返回配置；否则读取 Excel 数据动态提取
@api_bp.post('/department/list')
def get_department_list():
    data_in = request.get_json(silent=True) or {}
    year =data_in.get('year') or request.args.get('year')
    print(year)
    if not year:
        return jsonify({'error': 'year is required'}), 400
    # if year in departmentsByYear:
    #     return jsonify({'departments': departmentsByYear[year]})
    else:
        all_data = get_all_files_jsons(year)
        departments = sorted(get_all_departments(all_data["data"]))
        return jsonify({'departments': departments})

# 获取指标信息：根据年份和科室返回指标列表
@api_bp.post('/indicators')
def get_indicators():
    data_in = request.get_json(silent=True) or {}
    year = data_in.get('year')
    department = data_in.get('department')
    if not year or not department:
        return jsonify({'error': 'year and department are required'}), 400
    
    # 获取指标列表
    indicators = get_department_indicators(str(year), str(department))
    
    # 串行获取每个指标的详细数据
    result_list = []
    for indicator in indicators:
        # 获取指标详细数据
        result = get_indicator_detail({
            'year': str(year),
            'department': department,
            'indicator': indicator
        })
        
        # 构造返回格式
        if result is not None:
            result_list.append({
                'department': department,
                'year': year,
                'indicator': indicator,
                'number': result['value']
            })
    
    return jsonify(result_list)

@api_bp.post('/indicator/detail')
def indicator_detail():
    data_json = request.get_json(silent=True) or {}
    args = getattr(request, 'args', {}) or {}
    def _pick(k):
        v = data_json.get(k)
        return v if v not in (None, '') else args.get(k)

    indicator = _pick('indicator')
    year = _pick('year')
    department = _pick('department')
    admit_start_dt = safe_parse_data(_pick('入院日期_start'))
    admit_end_dt = safe_parse_data(_pick('入院日期_end'))
    discharge_start_dt = safe_parse_data(_pick('出院日期_start'))
    discharge_end_dt = safe_parse_data(_pick('出院日期_end'))

    if not indicator or not year or not department:
        return jsonify({'error': 'indicator, year, and department are required'}), 400
    
    result = get_indicator_detail({
        'year': str(year), 
        'department': department, 
        'indicator': indicator,
        'admit_start_dt': admit_start_dt,
        'admit_end_dt': admit_end_dt,
        'discharge_start_dt': discharge_start_dt,
        'discharge_end_dt': discharge_end_dt
    })

    return jsonify({'indicator': indicator, 'value': result['value'], 'sheet': result['sheet']})

@api_bp.get('/indicator/export')
def export_indicator():
    data_json = request.get_json(silent=True) or {}
    args = getattr(request, 'args', {}) or {}
    def _pick(k):
        v = data_json.get(k)
        return v if v not in (None, '') else args.get(k)

    indicator = _pick('indicator')
    year = _pick('year')
    department = _pick('department')
    admit_start_dt = safe_parse_data(_pick('入院日期_start'))
    admit_end_dt = safe_parse_data(_pick('入院日期_end'))
    discharge_start_dt = safe_parse_data(_pick('出院日期_start'))
    discharge_end_dt = safe_parse_data(_pick('出院日期_end'))

    if not indicator or not year or not department:
        return jsonify({'error': 'indicator, year, and department are required'}), 400
    
    value = get_indicator_detail({
        'year': str(year), 
        'department': department, 
        'indicator': indicator,
        'admit_start_dt': admit_start_dt,
        'admit_end_dt': admit_end_dt,
        'discharge_start_dt': discharge_start_dt,
        'discharge_end_dt': discharge_end_dt
    })

    res = export_sheet(f"{year}{indicator}明细", value['headers'], value['data'])
    return send_file(
        res['output'],
        as_attachment=True,
        download_name=res['filename'],
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
