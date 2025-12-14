
from typing import Any

def is_general_surgery_department(year: str, department: str):
    if('外科一病区' in department):
        return True
    return False

INDICATOR_FUNC_MAP = [
    'test'
]

def get_indicators():
    return list[Any](INDICATOR_FUNC_MAP.keys())

def get_general_surgery_indicator_detail(data: list, indicator: str) :
    fn = INDICATOR_FUNC_MAP.get(indicator)
    if fn:
        return fn(data)
    return {
        "data": [],
        "value": 0,
    }
