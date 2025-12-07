from utils.doctor import is_dead, match_diagnosis, not_match_diagnosis, out_from_neurology


def is_neurology_department(year: str, department: str):
    if('神经内科' in department):
        return True
    return False

# 病案首页主要诊断ICD-10编码：I63.0至I63.9的出院患者数，去除I63.301和 I63.802。
def 同期神经内科收治脑梗死患者总例数(data: list):
    filter = [
        item for item in data
        if out_from_neurology(item)
        and match_diagnosis(item, ['I63'])
        and not_match_diagnosis(item, ['I63.301', 'I63.802'])
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 病案首页出院科室为神经内科的患者数
def 同期神经内科收治患者总例数(data: list):
    filter = [
        item for item in data
        if out_from_neurology(item)
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 病案首页主要诊断ICD-10编码：I61.0至I61.9的出院患者数
def 同期神经内科收治脑出血患者总例数(data: list):
    filter = [
        item for item in data
        if out_from_neurology(item)
        and match_diagnosis(item, ['I61.'])
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科室为神经内科
# 2、病案首页包含诊断惊厥性癫痫持续状态（ICD-10编码：G41.900，）的病例
def 神经内科收治惊厥性癫痫持续状态患者例数(data: list):
    filter = [
        item for item in data
        if out_from_neurology(item)
        and match_diagnosis(item, ['G41.900'])
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科室为神经内科
# 2、病案首页诊断包含癫痫（ICD-10编码：G40.XXX 及 G41.XXX。）的病例
def 同期神经内科癫痫住院患者总例数(data: list):
    filter = [
        item for item in data
        if out_from_neurology(item)
        and match_diagnosis(item, ['G40.', 'G41.'])
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1.病案首页出院科室为神经内科
# 2.病案首页离院方式为死亡
def 神经内科住院患者死亡例数(data: list):
    filter = [
        item for item in data
        if out_from_neurology(item)
        and is_dead(item)
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 病案首页主要诊断ICD-10编码：G20.x00的出院患者数
def 同期住院帕金森病患者总数(data: list):
    filter = [
        item for item in data
        if out_from_neurology(item)
        and match_diagnosis(item, ['G20.x00'])
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

INDICATOR_FUNC_MAP = {
    '同期神经内科收治脑梗死患者总例数': 同期神经内科收治脑梗死患者总例数,
    '同期神经内科收治患者总例数': 同期神经内科收治患者总例数,
    '同期神经内科收治脑出血患者总例数': 同期神经内科收治脑出血患者总例数,
    '神经内科收治惊厥性癫痫持续状态患者例数': 神经内科收治惊厥性癫痫持续状态患者例数,
    '同期神经内科癫痫住院患者总例数': 同期神经内科癫痫住院患者总例数,
    '神经内科住院患者死亡例数': 神经内科住院患者死亡例数,
    '同期住院帕金森病患者总数': 同期住院帕金森病患者总数
}

def get_indicators():
    return list(INDICATOR_FUNC_MAP.keys())

def get_neurology_indicator_detail(data: list, indicator: str):
    fn = INDICATOR_FUNC_MAP.get(indicator)
    if fn:
        return fn(data)
    return {
        "data": [],
        "value": 0,
    }
