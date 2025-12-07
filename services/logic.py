from services.breath import (
    get_breath_indicator_detail,
    get_indicators as get_breath_indicators,
    is_breath_department
)
from services.endocrinology import (
    get_endocrinology_indicator_detail,
    get_indicators as get_endocrinology_indicators,
    is_endocrinology_department
)
from utils.json import get_all_files_jsons
from typing import Dict, Any
from services.neurology import (
    get_indicators as get_neurology_indicators,
    get_neurology_indicator_detail,   
    is_neurology_department
)
from constants.header import ADMIT_WARD_HEADER

def get_all_departments(data: list):
    header = ADMIT_WARD_HEADER
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

def get_department_indicators(year: str, department: str):
    if(is_breath_department(year, department)):
        return get_breath_indicators()
    elif(is_neurology_department(year, department)):
        return get_neurology_indicators()
    elif(is_endocrinology_department(year, department)):
        return get_endocrinology_indicators()
    return [
        'test'
    ]

def get_indicator_detail(params: Dict[str, Any]) -> Dict[str, Any] | None:
    year = params['year']
    indicator = params['indicator']
    department = params['department']
    sheet = get_all_files_jsons(year)
    headers = sheet["headers"]
    data = sheet["data"]
    if(is_breath_department(year, department)):
        result = get_breath_indicator_detail(data, indicator)
    elif(is_neurology_department(year, department)):
        result = get_neurology_indicator_detail(data, indicator)
    elif(is_endocrinology_department(year, department)):
        result = get_endocrinology_indicator_detail(data, indicator)
    else:
        result = None

    # 时间范围筛选
    # admit_start_dt = params['admit_start_dt']
    # admit_end_dt = params['admit_end_dt']
    # discharge_start_dt = params['discharge_start_dt']
    # discharge_end_dt = params['discharge_end_dt']
    # filtered_data = filter_by_datas(result, {
    #     'admit_start_dt': admit_start_dt,
    #     'admit_end_dt': admit_end_dt,
    #     'discharge_start_dt': discharge_start_dt,
    #     'discharge_end_dt': discharge_end_dt,
    # })


    return (
        None
        if result is None
        else {
            "sheet": {
                "headers": headers,
                "data": result["data"],
            },
            "value": result["value"],
        }
    )

