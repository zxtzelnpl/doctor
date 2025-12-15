from collections import defaultdict
from constants.header import (
    DISCHARGE_TIME_HEADER,
    ADMIT_TIME_HEADER,
    DISCHARGE_METHOD_HEADER,
    DISCHARGE_WARD_HEADER,
    PRIMARY_DIAGNOSIS_HEADER, PRIMARY_DIAGNOSIS_HEADER1, PRIMARY_DIAGNOSIS_HEADER2, PRIMARY_DIAGNOSIS_HEADER3, PRIMARY_DIAGNOSIS_HEADER4,
    INTENSIVE_CARE_HEADER1, INTENSIVE_CARE_HEADER2, INTENSIVE_CARE_HEADER3, INTENSIVE_CARE_HEADER4, INTENSIVE_CARE_HEADER5,
    ADMIT_DIAGNOSIS_HEADER1, ADMIT_DIAGNOSIS_HEADER2, ADMIT_DIAGNOSIS_HEADER3, ADMIT_DIAGNOSIS_HEADER4, ADMIT_DIAGNOSIS_HEADER5,
    SURGERY_OPERATION_HEADER1, SURGERY_OPERATION_HEADER2, SURGERY_OPERATION_HEADER3, SURGERY_OPERATION_HEADER4, SURGERY_OPERATION_HEADER5,
    SURGERY_OPERATION_HEADER6, SURGERY_OPERATION_HEADER7, SURGERY_OPERATION_HEADER8, SURGERY_OPERATION_HEADER9, SURGERY_OPERATION_HEADER10,
    ACTUAL_INPATIENT_DAYS_HEADER,
    # 出院情况（西医其他诊断1）(XY_CYQK1) ~ 出院情况（西医其他诊断20）(XY_CYQK20)
    DISCHARGE_STATUS_HEADER1, DISCHARGE_STATUS_HEADER2, DISCHARGE_STATUS_HEADER3, DISCHARGE_STATUS_HEADER4,
    DISCHARGE_STATUS_HEADER5, DISCHARGE_STATUS_HEADER6, DISCHARGE_STATUS_HEADER7, DISCHARGE_STATUS_HEADER8,
    DISCHARGE_STATUS_HEADER9, DISCHARGE_STATUS_HEADER10, DISCHARGE_STATUS_HEADER11, DISCHARGE_STATUS_HEADER12,
    DISCHARGE_STATUS_HEADER13, DISCHARGE_STATUS_HEADER14, DISCHARGE_STATUS_HEADER15, DISCHARGE_STATUS_HEADER16,
    DISCHARGE_STATUS_HEADER17, DISCHARGE_STATUS_HEADER18, DISCHARGE_STATUS_HEADER19, DISCHARGE_STATUS_HEADER20,
)
from typing import Any, Dict
from typing import Any
from datetime import datetime

from utils.excel import load_sheet

from typing import Counter

def out_from_breath(item: dict):
    return '呼吸' in item.get(DISCHARGE_WARD_HEADER, '')

def out_from_neurology(item: dict):
    return '神经' in item.get(DISCHARGE_WARD_HEADER, '')

def out_from_endocrinology(item: dict):
    """
    判断是否从内分泌科出院。
    """
    return '内分泌' in item.get(DISCHARGE_WARD_HEADER, '')

def out_from_gastroenterology(item: dict):
    """
    判断是否从消化内科出院。
    """
    return '消化' in item.get(DISCHARGE_WARD_HEADER, '')

def out_from_general_surgery(item: dict):
    """
    判断是否从普通外科出院。
    """
    return '外科一病区' in item.get(DISCHARGE_WARD_HEADER, '')



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

def match_diagnosis(item: dict, diagnosis_codes: list, range: Dict[str, int] = {'from': 0, 'to': 5}):
    headers = [
        PRIMARY_DIAGNOSIS_HEADER,
        PRIMARY_DIAGNOSIS_HEADER1,
        PRIMARY_DIAGNOSIS_HEADER2,
        PRIMARY_DIAGNOSIS_HEADER3,
        PRIMARY_DIAGNOSIS_HEADER4,
    ][range['from']:range['to']]

    return any(
        code.startswith(tuple(diagnosis_codes))
        for code in (item.get(header, '') for header in headers)
    )

def not_match_diagnosis(item: dict, diagnosis_codes: list, range: Dict[str, int] = {'from': 0, 'to': 5}):
    return not match_diagnosis(item, diagnosis_codes, range)

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

def discharge_in_31_days(data: list):
    """
    筛选出出院在31天内又入院的记录。
    """
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
    """
    判断手术操作是否匹配给定的手术操作码列表。
    """
    
    # 检查所有手术操作编码字段
    for header in [
        SURGERY_OPERATION_HEADER1, SURGERY_OPERATION_HEADER2, SURGERY_OPERATION_HEADER3, SURGERY_OPERATION_HEADER4, SURGERY_OPERATION_HEADER5,
        SURGERY_OPERATION_HEADER6, SURGERY_OPERATION_HEADER7, SURGERY_OPERATION_HEADER8, SURGERY_OPERATION_HEADER9, SURGERY_OPERATION_HEADER10,
    ]:
        surgeryCode = item.get(header, '')
        if any(surgeryCode.startswith(code) for code in operation_codes):
            return True
    return False

def has_invasive_mechanical_ventilation_treatment(item: dict):
    raw = item.get("有创呼吸机使用时间(YCHXJSYSJ)", "0")
    try:
        return float(raw) > 0
    except (ValueError, TypeError):
        return False
    
def get_actual_inpatient_days(data: list):
    """
    获取总实际住院天数。
    """
    total_days = 0
    for item in data:
        raw = item.get(ACTUAL_INPATIENT_DAYS_HEADER, "0")
        try:
            total_days += float(raw)
        except (ValueError, TypeError):
            continue
    return total_days

def match_discharge_diagnosis(item: dict, diagnosis_codes: list):
    headers = [
        DISCHARGE_STATUS_HEADER1, DISCHARGE_STATUS_HEADER2, DISCHARGE_STATUS_HEADER3, DISCHARGE_STATUS_HEADER4,
        DISCHARGE_STATUS_HEADER5, DISCHARGE_STATUS_HEADER6, DISCHARGE_STATUS_HEADER7, DISCHARGE_STATUS_HEADER8,
        DISCHARGE_STATUS_HEADER9, DISCHARGE_STATUS_HEADER10, DISCHARGE_STATUS_HEADER11, DISCHARGE_STATUS_HEADER12,
        DISCHARGE_STATUS_HEADER13, DISCHARGE_STATUS_HEADER14, DISCHARGE_STATUS_HEADER15, DISCHARGE_STATUS_HEADER16,
        DISCHARGE_STATUS_HEADER17, DISCHARGE_STATUS_HEADER18, DISCHARGE_STATUS_HEADER19, DISCHARGE_STATUS_HEADER20,
    ]

    return any(
        code.startswith(tuple[Any, ...](diagnosis_codes))
        for code in (item.get(header, '') for header in headers)
    )