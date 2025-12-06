from collections import defaultdict
from constants.header import (
    DISCHARGE_TIME_HEADER,
    ADMIT_TIME_HEADER,
    DISCHARGE_METHOD_HEADER,
    DISCHARGE_WARD_HEADER,
    PRIMARY_DIAGNOSIS_HEADER, PRIMARY_DIAGNOSIS_HEADER1, PRIMARY_DIAGNOSIS_HEADER2, PRIMARY_DIAGNOSIS_HEADER3, PRIMARY_DIAGNOSIS_HEADER4,
    INTENSIVE_CARE_HEADER1, INTENSIVE_CARE_HEADER2, INTENSIVE_CARE_HEADER3, INTENSIVE_CARE_HEADER4, INTENSIVE_CARE_HEADER5,
    ADMIT_DIAGNOSIS_HEADER1, ADMIT_DIAGNOSIS_HEADER2, ADMIT_DIAGNOSIS_HEADER3, ADMIT_DIAGNOSIS_HEADER4, ADMIT_DIAGNOSIS_HEADER5,
    SURGERY_OPERATION_HEADER
)
from typing import Dict
from typing import Any
from datetime import datetime

from utils.excel import load_sheet

from typing import Counter

def match_admission_date(row, start_dt=None, end_dt=None):
    """
    根据入院日期筛选记录。
    
    参数:
        row (dict): 包含入院日期字段的数据行
        start_dt (datetime, optional): 起始日期，若提供则只保留入院日期大于等于该值的记录
        end_dt (datetime, optional): 结束日期，若提供则只保留入院日期小于等于该值的记录
    
    返回:
        bool: 若记录符合日期范围则返回True，否则返回False
    """
    if not (start_dt or end_dt):
        return True
    rv = row.get(ADMIT_TIME_HEADER)
    if not rv:
        return False
    try:
        rdt = datetime.strptime(str(rv), '%Y-%m-%d %H:%M:%S')
    except Exception:
        return False
    if start_dt and rdt < start_dt:
        return False
    if end_dt and rdt > end_dt:
        return False
    return True

def match_discharge_date(row, start_dt=None, end_dt=None):
    """
    根据出院日期筛选记录。
    
    参数:
        row (dict): 包含出院日期字段的数据行
        start_dt (datetime, optional): 起始日期，若提供则只保留出院日期大于等于该值的记录
        end_dt (datetime, optional): 结束日期，若提供则只保留出院日期小于等于该值的记录
    
    返回:
        bool: 若记录符合日期范围则返回True，否则返回False
    """
    if not (start_dt or end_dt):
        return True
    rv = row.get(DISCHARGE_TIME_HEADER)
    if not rv:
        return False
    try:
        rdt = datetime.strptime(str(rv), '%Y-%m-%d %H:%M:%S')
    except Exception:
        return False
    if start_dt and rdt < start_dt:
        return False
    if end_dt and rdt > end_dt:
        return False
    return True

# 筛选数据，根据入院日期和出院日期筛选数据
def filter_by_datas(data:list, params: Dict[str, Any]):
    """
    根据请求参数筛选数据列表，根据入院日期和出院日期进行筛选。
    
    参数:
        req (Request): Flask请求对象，包含查询参数和JSON体
        data (list): 包含数据行的列表，每个数据行是一个字典
    
    返回:
        list: 筛选后的符合条件的数据行列表
    """
    admit_start_dt = params['admit_start_dt']
    admit_end_dt = params['admit_end_dt']
    discharge_start_dt = params['discharge_start_dt']
    discharge_end_dt = params['discharge_end_dt']
  
    return [
        row for row in data 
        if match_admission_date(row, admit_start_dt, admit_end_dt) and match_discharge_date(row, discharge_start_dt, discharge_end_dt)
    ]

def not_dead(item: dict):
    return item.get(DISCHARGE_METHOD_HEADER, '') != '5'

def is_dead(item: dict):
    return item.get(DISCHARGE_METHOD_HEADER, '') == '5'

def match_diagnosis(item: dict, diagnosis_codes: list):
    return any(code.startswith(tuple(diagnosis_codes)) for code in [
                item.get(PRIMARY_DIAGNOSIS_HEADER, ''),
                item.get(PRIMARY_DIAGNOSIS_HEADER1, ''),
                item.get(PRIMARY_DIAGNOSIS_HEADER2, ''),
                item.get(PRIMARY_DIAGNOSIS_HEADER3, ''),
                item.get(PRIMARY_DIAGNOSIS_HEADER4, ''),
            ])

def intensive_care_is_empty(item: dict):
    # 当所有字段都不存在（即为空字符串或 None）时返回 True
    return all(
        (item.get(header) is None or str(item.get(header, '')).strip() == '')
        for header in [
            INTENSIVE_CARE_HEADER1,
            INTENSIVE_CARE_HEADER2,
            INTENSIVE_CARE_HEADER3,
            INTENSIVE_CARE_HEADER4,
            INTENSIVE_CARE_HEADER5
        ]
    )

def intensive_care_is_not_empty(item: dict):
    # 当所有字段都不存在（即为空字符串或 None）时返回 True
    return any(
        str(item.get(header, '')).strip() != ''
        for header in [
            INTENSIVE_CARE_HEADER1,
            INTENSIVE_CARE_HEADER2,
            INTENSIVE_CARE_HEADER3,
            INTENSIVE_CARE_HEADER4,
            INTENSIVE_CARE_HEADER5
        ]
    )

def out_from_breath(item: dict):
    return '呼吸' in item.get(DISCHARGE_WARD_HEADER, '')

def no_admit_diagnosis(item: dict):
    """
    入院诊断是否为空（即入院情况为无）。
    """
    return all(
        (item.get(header) is None or str(item.get(header, '')).strip() == '')
        for header in [
            ADMIT_DIAGNOSIS_HEADER1,
            ADMIT_DIAGNOSIS_HEADER2,
            ADMIT_DIAGNOSIS_HEADER3,
            ADMIT_DIAGNOSIS_HEADER4,
            ADMIT_DIAGNOSIS_HEADER5
        ]
    )


def get_diagnosis_codes(file: str, sheet_index: int, name: str):
    """
    从对应的文件中获取疾病的名字
    """
    sheet = load_sheet(file, sheet_index)
    data = sheet["data"]
  
    filter_item = [
        item for item in data
        if str(item.get('字典名称')) == name
    ]
    names = [item['编码'] for item in filter_item]
    
    return names


def discharge_plan_in_31_days(data: list):
    print(type(data[0][ADMIT_TIME_HEADER]))
    ID_HEADER = '身份证号(SFZH)'
    # 统计每个病人身份证号出现的次数
    name_counts = Counter(item[ID_HEADER] for item in data)
    # 筛选出出现多次的病人身份证号
    duplicate_names = {name for name, count in name_counts.items() if count > 1}
    # 按病人姓名分组，只保留出现多次的病人姓名的数据
    grouped_data = defaultdict(list)
    for item in data:
        name = item[ID_HEADER]
        if name in duplicate_names:
            grouped_data[name].append(item)

    # 转成普通字典方便查看
    grouped_data = dict(grouped_data)
    next_res = []
    for name, items in grouped_data.items():
         # 2. 按入院日期排序
        sorted_data = sorted(items, key=lambda x: datetime.strptime(str(x[ADMIT_TIME_HEADER]), '%Y-%m-%d %H:%M:%S'))
        for i in range(1, len(sorted_data)):
                # 解析日期字符串为 datetime 对象
                prev_discharge = datetime.strptime(sorted_data[i-1][DISCHARGE_TIME_HEADER], '%Y-%m-%d %H:%M:%S')
                curr_admission = datetime.strptime(sorted_data[i][ADMIT_TIME_HEADER], '%Y-%m-%d %H:%M:%S')
                
                # 计算时间差（天数）
                diff_days = (curr_admission - prev_discharge).days
                
                # 判断时间差是否小于等于31天
                if 0 <= diff_days <= 31:
                    next_res.append(sorted_data[i])
    return next_res

def match_surgery_operation(item: dict, operation_codes: list):
    surgeryCode = item.get(SURGERY_OPERATION_HEADER, '')
    return any(surgeryCode.startswith(code) for code in operation_codes)

def has_invasive_mechanical_ventilation_treatment(item: dict):
    raw = item.get("有创呼吸机使用时间(YCHXJSYSJ)", "0")
    try:
        return float(raw) > 0
    except (ValueError, TypeError):
        return False