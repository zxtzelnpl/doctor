from constants.header import ADMIT_TIME_HEADER
from constants.header import DISCHARGE_TIME_HEADER
from constants.header import DEPARTMENT_HEADER
from typing import Dict
from typing import Any
from datetime import datetime

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

def filter_by_department(data: list, department: str):
    return [item for item in data if department in str(item.get(DEPARTMENT_HEADER, ''))]
