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
