
from typing import Any
from utils.doctor import (
    get_diagnosis_codes,
    match_diagnosis,
    get_actual_inpatient_days,
    out_from_gastroenterology,
    not_dead,
    match_discharge_diagnosis,
)

def is_gastroenterology_department(year: str, department: str):
    if('消化内科' in department):
        return True
    return False

# （消化内科）同期出院的重点病种患者总例数
# 1、病案首页出院科别为消化内科
# 2、病案首页中出院主要诊断为重点病种诊断编码：血消化道出（见字典表）、急性胰腺炎（见字典表）
# 3、病案首页离院方式为非死亡
def 同期出院的重点病种患者总例数(data: list):
    codes1 = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '血消化道出')
    codes2 = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '急性胰腺炎')
    codes = codes1 + codes2

    filter = [
        item for item in data
        if out_from_gastroenterology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
        and not_dead(item)
    ]
    
    return {
        "data": filter,
        "value": len(filter),
    }

# 病案首页出院科别为消化内科的患者住院天数的总和
def 实际占用的总床日数(data: list):
    filter = [
        item for item in data
        if out_from_gastroenterology(item)
    ]

    total_days = get_actual_inpatient_days(filter)
    return {
        "data": filter,
        "value": total_days,
    }

#  病案首页出院科别为消化内科的患者数
def 同期住院患者总例数(data: list):
    filter = [
        item for item in data
        if out_from_gastroenterology(item)
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为消化内科
# 2、病案首页主要诊断ICD-10编码：K20.x00x011、K22.300x002、K22.600、K22.804、K25.000、K25.2\K25.4、K25.6、K26.0、K26.2、K26.4、K26.6、K27.0、K27.2、K27.4、K27.6、K28.0、K28.2、K28.4、K28.600、K28.600x001、K29.0、K51.800x001K55.000x022、K55.003、K55.100x011、K55.900x004、K62.100x002、K62.5、K62.800x001、K63.300x005、K63.800x012、K91.800x102、K91.800x103、K91.800x106、K91.800x702、K91.800x706、K92.0、K92.100x001、K92.2、R19.501的出院患者
def 同期收治的消化道出血患者总例数(data: list):
    codes = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '消化道出血')

    filter = [
        item for item in data
        if out_from_gastroenterology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为消化内科
# 2、病案首页主要诊断ICD-10编码：K20.x00x011、K22.300x002、K22.600、K22.804、K25.000、K25.2、K25.4、K25.6、K26.0、K26.2、K26.4、K26.6、K27.0、K27.2、K27.4、K27.6、K28.0、K28.2、K28.4、K28.600、K28.600x001、K29.0、K51.800x001、K55.000x022、K55.003、K55.100x011、K55.900x004、K62.100x002、K62.5、K62.800x001、K63.300x005、K63.800x012、K91.800x102、K91.800x103、K91.800x106、K91.800x702、K91.800x706、K92.0、K92.100x001、K92.2、R19.501的出院患者
# 3、病案首页出院所有诊断编码包含消化道出血病因诊断对应编码（见字典表）
def 消化道出血患者出院诊断包含病因的例数(data: list):
    codes = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '消化道出血')

    filter = [
        item for item in data
        if out_from_gastroenterology(item)
        and (match_diagnosis(item, codes), {'from':0, 'to': 1})
        and (match_discharge_diagnosis(item, codes))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为消化内科
# 2、病案首页主要诊断ICD-10编码：K20.x00x011、K22.300x002、K22.600、K22.804、K25.000、K25.2、K25.4、K25.6、K26.0、K26.2、K26.4、K26.6、K27.0、K27.2、K27.4、K27.6、K28.0、K28.2、K28.4、K28.600、K28.600x001、K29.0、K51.800x001、K55.000x022、K55.003、K55.100x011、K55.900x004、K62.100x002、K62.5、K62.800x001、K63.300x005、K63.800x012、K91.800x102、K91.800x103、K91.800x106、K91.800x702、K91.800x706、K92.0、K92.100x001、K92.2、R19.501的出院患者
def 消化道出血住院患者总例数(data: list):
    codes = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '消化道出血')

    filter = [
        item for item in data
        if out_from_gastroenterology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为消化内科
# 2、病案首页主要诊断为炎症性肠病诊断编码（见字典表）
def 同期炎症性肠病住院患者总例数(data: list):
    codes = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '炎症性肠病')

    filter = [
        item for item in data
        if out_from_gastroenterology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为消化内科
# 2、病案首页出院出院所有诊断含肝硬化病因诊断编码（见字典表）
def 病因明确的肝硬化患者例数(data: list):
    codes = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '肝硬化病因诊断')

    filter = [
        item for item in data
        if out_from_gastroenterology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
        and (match_discharge_diagnosis(item, codes))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为消化内科
# 2、病案首页主要诊断为肝硬化诊断编码（见字典表）
def 同期肝硬化住院患者总例数(data: list):
    codes = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '肝硬化')

    filter = [
        item for item in data
        if out_from_gastroenterology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为消化内科
# 2、病案首页主要诊断为肝硬化失代偿诊断编码（见字典表）
def 同期肝硬化失代偿住院患者总例数(data: list):
    codes = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '肝硬化失代偿')

    filter = [
        item for item in data
        if out_from_gastroenterology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }
# 1、病案首页出院科别为消化内科
# 2、病案首页主要诊断为急性胰腺炎诊断编码（见字典表）
def 同期收治AP_患者总例数(data: list):
    codes = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '急性胰腺炎')

    filter = [
        item for item in data
        if out_from_gastroenterology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为消化内科
# 2、病案首页主要诊断为急性胰腺炎诊断编码（见字典表）
# 3、病案首页出院所有诊断含急性胰腺炎病因单一诊断（见字典表）
# 或病案首页出院所有诊断编码含急性胰腺炎病因组合诊断之一（见字典表）同时含有急性胰腺炎病因组合诊断之二（见字典表）
def 出院诊断包含病因的AP_患者例数(data: list):
    codes = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '急性胰腺炎')
    codes0 = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '急性胰腺炎病因单一诊断')
    codes1 = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '急性胰腺炎病因组合诊断之一')
    codes2 = get_diagnosis_codes('./back/消化内科-重点专业单病种质控指标.xlsx', 1, '急性胰腺炎病因组合诊断之二')

    filter = [
        item for item in data
        if out_from_gastroenterology(item)
        and (match_discharge_diagnosis(item, codes))
        and (
            match_discharge_diagnosis(item, codes0)
            or (match_discharge_diagnosis(item, codes1) and match_discharge_diagnosis(item, codes2))
        )

    ]
    return {
        "data": filter,
        "value": len(filter),
    }

INDICATOR_FUNC_MAP = {
    '（消化内科）同期出院的重点病种患者总例数': 同期出院的重点病种患者总例数,
    '（消化内科）实际占用的总床日数': 实际占用的总床日数,
    '（消化内科）同期住院患者总例数': 同期住院患者总例数,
    '同期收治的消化道出血患者总例数': 同期收治的消化道出血患者总例数,
    '消化道出血患者出院诊断包含病因的例数': 消化道出血患者出院诊断包含病因的例数,
    '消化道出血住院患者总例数': 消化道出血住院患者总例数,
    '同期炎症性肠病住院患者总例数': 同期炎症性肠病住院患者总例数,
    '病因明确的肝硬化患者例数': 病因明确的肝硬化患者例数,
    '同期肝硬化住院患者总例数': 同期肝硬化住院患者总例数,
    '同期肝硬化失代偿住院患者总例数': 同期肝硬化失代偿住院患者总例数,
    '同期收治AP 患者总例数': 同期收治AP_患者总例数,
    '出院诊断包含病因的AP 患者例数': 出院诊断包含病因的AP_患者例数,
}


def get_indicators():
    return list[Any](INDICATOR_FUNC_MAP.keys())

def get_gastroenterology_indicator_detail(data: list, indicator: str) :
    fn = INDICATOR_FUNC_MAP.get(indicator)
    if fn:
        return fn(data)
    return {
        "data": [],
        "value": 0,
    }
