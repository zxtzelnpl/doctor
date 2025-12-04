from datetime import datetime
from utils.base import safe_parse_data

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
    rv = row.get('入院日期')
    if not rv:
        return False
    try:
        rdt = datetime.strptime(str(rv), '%Y-%m-%d')
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
    rv = row.get('出院日期')
    if not rv:
        return False
    try:
        rdt = datetime.strptime(str(rv), '%Y-%m-%d')
    except Exception:
        return False
    if start_dt and rdt < start_dt:
        return False
    if end_dt and rdt > end_dt:
        return False
    return True

def match_row(row, admit_start_dt=None, admit_end_dt=None, discharge_start_dt=None, discharge_end_dt=None):
    if not match_admission_date(row, admit_start_dt, admit_end_dt):
        return False
    if not match_discharge_date(row, discharge_start_dt, discharge_end_dt):
        return False
    return True

def filter_datas(req, data:list):
    data_json = None
    try:
        data_json = req.get_json(silent=True) or {}
    except Exception:
        data_json = {}
    args = getattr(req, 'args', {}) or {}
    def _pick(k):
        v = data_json.get(k)
        return v if v not in (None, '') else args.get(k)
    admit_start_dt = safe_parse_data(_pick('入院日期_start')) if _pick('入院日期_start') else None
    admit_end_dt = safe_parse_data(_pick('入院日期_end')) if _pick('入院日期_end') else None
    discharge_start_dt = safe_parse_data(_pick('出院日期_start')) if _pick('出院日期_start') else None
    discharge_end_dt = safe_parse_data(_pick('出院日期_end')) if _pick('出院日期_end') else None
    return [row for row in data if filter_datas(req, row, admit_start_dt, admit_end_dt, discharge_start_dt, discharge_end_dt)]