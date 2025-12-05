from utils.doctor import filter_by_datas, filter_by_department
from services.breath import get_breath_indicator_detail, get_indicators as get_breath_indicators
from utils.json import get_all_files_jsons
from typing import Dict, Any

from constants.header import DEPARTMENT_HEADER

def get_all_departments(data: list):
    header = DEPARTMENT_HEADER
    # 收集所有非空的入院病房值
    departments = [
        str(item[header])
        for item in data
        if header in item and item[header] is not None and str(item[header]).strip() != ''
    ]
    # 去重并保持原顺序
    seen = set()
    unique_departments = []
    for dept in departments:
        if dept not in seen:
            seen.add(dept)
            unique_departments.append(dept)
    return unique_departments

def get_indicator_detail(params: Dict[str, Any]) -> Dict[str, Any] | None:
    year = params['year']
    indicator = params['indicator']
    department = params['department']
    sheet = get_all_files_jsons(year)
    headers = sheet["headers"]
    data = sheet["data"]

    # 这里开始调用指标
    if(year == '2025'):
        if(department == '内科一病区（呼吸）'):
            result = get_breath_indicator_detail(data, indicator)
    else:
        result = data

    admit_start_dt = params['admit_start_dt']
    admit_end_dt = params['admit_end_dt']
    discharge_start_dt = params['discharge_start_dt']
    discharge_end_dt = params['discharge_end_dt']

    filtered_data = filter_by_datas(result, {
        'admit_start_dt': admit_start_dt,
        'admit_end_dt': admit_end_dt,
        'discharge_start_dt': discharge_start_dt,
        'discharge_end_dt': discharge_end_dt,
    })
    filtered_data = filter_by_department(filtered_data, department)


    return None if filtered_data is None else {"headers": headers, "data": filtered_data}

def get_department_indicators(year: str, department: str):
    if(year == '2025'):
        if(department == '内科一病区（呼吸）'):
            return get_breath_indicators()
    return [
        'test'
    ]
