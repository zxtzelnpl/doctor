from constants.header import (
    PRIMARY_AGE_HEADER,
    DISCHARGE_PLAN_HEADER_IN_31_DAYS_HEADER
)
from utils.doctor import discharge_plan_in_31_days, get_diagnosis_codes, has_invasive_mechanical_ventilation_treatment, intensive_care_is_empty, intensive_care_is_not_empty, match_surgery_operation, out_from_breath, match_diagnosis, no_admit_diagnosis, not_dead, is_dead

def is_breath_department(year: str, department: str):
        if(year == '2025'):
            if(department == '内科一病区（呼吸）'):
                return True
        if(year == '2024'):
            if(department == '内科一病区（呼吸）'):
                return True
        if(year == '2023'):
            if('呼吸' in department):
                return True
        if(year == '2022'):
            if('呼吸' in department):
                return True
        return False

def get_indicators():
    return [
        '社区获得性肺炎出院患者总例数',
        '肺血栓栓塞症出院患者总例数',
        '慢性阻塞性肺疾病出院患者总例数',
        '哮喘出院患者总例数',
        '普通病房住院患者死亡总数',
        '同期住院患者总人次数',
        'MICU/RICU 住院患者死亡数',
        '同期监护室住院患者总人次数',
        '低风险病种住院患者死亡人数',
        '（呼吸内科）呼吸机相关性肺炎（VAP）发生例数',
        '（呼吸内科）同期住院患者有创机械通气总天数',
        '（呼吸内科）血管内导管相关血流感染（CRBSI）发生例数',
        '（呼吸内科）导尿管相关泌尿系感染（CAUTI）发生例数',
        '同期下呼吸道感染住院患者总例数',
        # '转出ICU 后48h 内重返ICU 的患者人次数',
        '出院31 天内非预期再住院患者人次数',
        # '哮喘/COPD 住院患者完成肺功能检查例数',
        # '同期使用呼吸机患者总例数',
        '曾行有创机械通气的住院患者死亡数',
        '同期曾行有创机械通气的住院患者总人次数',
    ]

def get_breath_indicator_detail(data: list, indicator: str) :
    if indicator == '社区获得性肺炎出院患者总例数':
        return 社区获得性肺炎出院患者总例数(data)
    elif indicator == '肺血栓栓塞症出院患者总例数':
        return 肺血栓栓塞症出院患者总例数(data)
    elif indicator == '慢性阻塞性肺疾病出院患者总例数':
        return 慢性阻塞性肺疾病出院患者总例数(data)
    elif indicator == '哮喘出院患者总例数':
        return 哮喘出院患者总例数(data)
    elif indicator == '普通病房住院患者死亡总数':
        return 普通病房住院患者死亡总数(data)
    elif indicator == '同期住院患者总人次数':
        return 同期住院患者总人次数(data)
    elif indicator == 'MICU/RICU 住院患者死亡数':
        return MICU_RICU_住院患者死亡数(data)
    elif indicator == '同期监护室住院患者总人次数':
        return 同期监护室住院患者总人次数(data)
    elif indicator == '低风险病种住院患者死亡人数':
        return 低风险病种住院患者死亡人数(data)
    elif indicator == '（呼吸内科）呼吸机相关性肺炎（VAP）发生例数':
        return 呼吸内科_呼吸机相关性肺炎_VAP_发生例数(data)
    elif indicator == '（呼吸内科）同期住院患者有创机械通气总天数':
        return 呼吸内科_同期住院患者有创机械通气总天数(data)
    elif indicator == '（呼吸内科）血管内导管相关血流感染（CRBSI）发生例数':
        return 呼吸内科_血管内导管相关血流感染_CRBSI_发生例数(data)
    elif indicator == '（呼吸内科）导尿管相关泌尿系统感染（CAUTI）发生例数':
        return 呼吸内科_导尿管相关泌尿系统感染_CAUTI_发生例数(data)
    elif indicator == '同期下呼吸道感染住院患者总例数':
        return 同期下呼吸道感染住院患者总例数(data)
    elif indicator == '出院31 天内非预期再住院患者人次数':
        return 出院31_天内非预期再住院患者人次数(data)
    elif indicator == '曾行有创机械通气的住院患者死亡数':
        return 曾行有创机械通气的住院患者死亡数(data)
    elif indicator == '同期曾行有创机械通气的住院患者总人次数':
        return 同期曾行有创机械通气的住院患者总人次数(data)
    
    return {
        "data": [],
        "value": 0,
    }

# 1.病案首页出院科室为呼吸内科
# 2.病案首页出院主要诊断ICD-10编码：J13至J16，J18；
# 3.年龄≥18岁且离院方式非死亡的出院患者
def 社区获得性肺炎出院患者总例数(data: list):
    filtered = [
        item for item in data
        if out_from_breath(item)
        and (match_diagnosis(item, ['J13', 'J14', 'J15', 'J16', 'J18']))
        and int(item.get(PRIMARY_AGE_HEADER, 0)) >= 18
        and not_dead(item)
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

# 1.病案首页出院科室为呼吸内科
# 2.病案首页出院主要诊断ICD-10编码：I26.900、I26.901、I26.000且离院方式非死亡的出院患者
def 肺血栓栓塞症出院患者总例数(data: list):
    filtered = [
        item for item in data
        if out_from_breath(item)
        and (match_diagnosis(item, ['I26.900', 'I26.901', 'I26.000']))
        and not_dead(item)
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

# 1.病案首页出院科室为呼吸内科
# 2.病案首页主要诊断ICD-10编码：J44.0，J44.1且离院方式非死亡的出院患者
def 慢性阻塞性肺疾病出院患者总例数(data: list):
    # 筛选条件：
    # 1. 主要诊断编码在ICD-10的J40-J47范围内
    # 3. 离院方式不为'5'（死亡）
    filtered = [
        item for item in data
        if out_from_breath(item)
        and (match_diagnosis(item, ['J40', 'J41', 'J42', 'J43', 'J44', 'J45', 'J46', 'J47']))
        and not_dead(item)
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

def 哮喘出院患者总例数(data: list):
    # 筛选条件：
    # 1.病案首页出院科室为呼吸内科
    # 2.病案首页主要诊断ICD-10编码：J45，J46；年龄 ≥18岁且离院方式非死亡的出院患者
    filtered = [
        item for item in data
        if out_from_breath(item)
        and (match_diagnosis(item, ['J45', 'J46']))
        and int(item.get(PRIMARY_AGE_HEADER, 0)) >= 18
        and not_dead(item)
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

def 普通病房住院患者死亡总数(data: list):
    # 筛选条件：
    # 1、病案首页出院科室为呼吸内科
    # 2、病案首页重症监护室为空白
    # 3、病案首页离院方式为“死亡”的人数
    filtered = [
        item for item in data
        if out_from_breath(item)
        and intensive_care_is_empty(item)
        and is_dead(item)
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

def 同期住院患者总人次数(data: list):
    # 筛选条件：
    # 1、病案首页出院科室为呼吸内科
    # 2、病案首页重症监护室为空白
    filtered = [
        item for item in data
        if out_from_breath(item)
        and intensive_care_is_empty(item)
        and not_dead(item)
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

def MICU_RICU_住院患者死亡数(data: list):
    # 筛选条件：
    # 1、病案首页出院科室为呼吸内科
    # 2、病案首页重症监护室为MICU/RICU
    # 3、病案首页离院方式为“死亡”的人数
    filtered = [
        item for item in data
        if out_from_breath(item)
        and intensive_care_is_not_empty(item)
        and is_dead(item)
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

# 重症监护怎么判断
def 同期监护室住院患者总人次数(data: list):
    # 筛选条件：
    # 1、病案首页出院科室为呼吸内科
    # 2、病案首页重症监护室为MICU/RICU
    filtered = [
        item for item in data
        if out_from_breath(item)
        and intensive_care_is_not_empty(item)
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

# 1、病案首页出院科室为呼吸内科
# 1、病案首页主要诊断为呼吸内科相关低风险病种的 ICD-10 编码：J04,J06,J20,J21, J40、J45，包括急性喉炎和气管炎、多发性和未特指部位的急性上呼吸道感染、急性支气管炎、急性细支气管炎、支气管炎未特指急性或慢性、哮喘
# 2、病案首页离院方式为“死亡”的人数
def 低风险病种住院患者死亡人数(data: list):
    # 筛选条件：
    # 1. 主要诊断编码在ICD-10的J04、J06、J20、J21、J40、J45范围内
    # 2. 离院方式为'5'（死亡）
    filtered = [
        item for item in data
        if out_from_breath(item)
        and (match_diagnosis(item, ['J04', 'J06', 'J20', 'J21', 'J40', 'J45']))
        and is_dead(item)
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

# （呼吸内科）呼吸机相关性肺炎（VAP）发生例数
# 1、病案首页出院科室为呼吸内科
# 2、病案首页所有诊断编码中含呼吸机相关性肺炎 J95.802 且入院情况为无
def 呼吸内科_呼吸机相关性肺炎_VAP_发生例数(data: list):
    filtered = [
        item for item in data
        if out_from_breath(item)
        and (match_diagnosis(item, ['J95.802']))
        and no_admit_diagnosis(item)
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

# （呼吸内科）同期住院患者有创机械通气总天数
# 1.病案首页出院科室为呼吸内科
# 2.病案首页呼吸机使用时间总和/24
def 呼吸内科_同期住院患者有创机械通气总天数(data: list):
    filtered = [
        item for item in data
        if out_from_breath(item)
        and has_invasive_mechanical_ventilation_treatment(item)
    ]

    total_hours = 0
    for item in filtered:
        # 取出「有创呼吸机使用时间(YCHXJSYSJ)」字段，空值按0处理
        raw = item.get("有创呼吸机使用时间(YCHXJSYSJ)", "0")
        try:
            total_hours += float(raw)
        except (ValueError, TypeError):
            total_hours += 0
    return {
        "data": filtered,
        "value": total_hours / 24,
    }

# （呼吸内科）血管内导管相关血流感染（CRBSI）发生例数
# 1、病案首页出院科室为呼吸内科
# 2、病案首页出院所有诊断编码中包括血管内导管相关血流感染 T82.700x001且入院情况为无
def 呼吸内科_血管内导管相关血流感染_CRBSI_发生例数(data: list):
    filtered = [
        item for item in data
        if out_from_breath(item)
        and (match_diagnosis(item, ['T82.700x001']))
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

# （呼吸内科）导尿管相关泌尿系感染（CAUTI）发生例数
# 1、病案首页出院科室为呼吸内科
# 2、病案首页出院所有诊断编码中包括导尿管相关泌尿系统感染T83.500x003
# 3、且入院情况为无
def 呼吸内科_导尿管相关泌尿系统感染_CAUTI_发生例数(data: list):
    filtered = [
        item for item in data
        if out_from_breath(item)
        and (match_diagnosis(item, ['T83.500x003']))
        and no_admit_diagnosis(item)
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

# 同期下呼吸道感染住院患者总例数
# 1.病案首页出院科室为呼吸内科
# 2.病案首页出院主要诊断编码中包括下呼吸道感染（见字典表）
def 同期下呼吸道感染住院患者总例数(data: list):
    diagnosis_codes = get_diagnosis_codes("./back/0呼吸内科-重点专业单病种质控指标.xlsx", 1, "下呼吸道感染")
    
    filtered = [
        item for item in data
        if out_from_breath(item)
        and (match_diagnosis(item, diagnosis_codes))
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

# 转出ICU 后48h 内重返ICU 的患者人次数 TODO
# def 转出ICU_后48h_内重返ICU_的患者人次数(data: list):
#     return {
#         "data": [],
#         "value": len([]),
#     }

# 出院31 天内非预期再住院患者人次数
# 1、病案首页出院科室为呼吸内科
# 2、上一次出院病案首页“是否有出院 31 天内再住院计划 ”为无或缺失
# 3、病案首页入院时间减去上一次病案首页出院时间≤31天
def 出院31_天内非预期再住院患者人次数(data: list):
    filtered = [
        item for item in data
        if out_from_breath(item)
        and item[DISCHARGE_PLAN_HEADER_IN_31_DAYS_HEADER] == '1'
    ]

    next_res = discharge_plan_in_31_days(filtered)

    return {
        "data": next_res,
        "value": len(next_res),
    }

# 哮喘/COPD 住院患者完成肺功能检查例数
# 1、病案首页出院科室为呼吸内科
# 2、病案首页主要诊断包括J 44 COPD或J45 哮喘的住院患者，
# 2、健康网非药医嘱医嘱中包含肺功能检查（见字典表）
# def 哮喘_COPD_住院患者完成肺功能检查例数(data: list):
#     filtered = [
#         item for item in data
#         if out_from_breath(item)
#         and (match_diagnosis(item, ['J44', 'J45']))
#         and has_lung_function_check(item)
#     ]
#     return {
#         "data": filtered,
#         "value": len(filtered),
#     }


# 同期使用呼吸机患者总例数
# def 同期使用呼吸机患者总例数(data: list):
#     filtered = list
#     return {
#         "data": filtered,
#         "value": len(filtered),
#     }


# 曾行有创机械通气的住院患者死亡数
# 1、病案首页出院科室为呼吸内科
# 2、病案首页有创呼吸机使用时间>0或病案首页手术操作编码含有创机械通气（见字典表）
# 3、病案首页离院方式为死亡
def 曾行有创机械通气的住院患者死亡数(data: list):

    filtered = [
        item for item in data
        if out_from_breath(item)
        and is_dead(item)
        and (
            match_surgery_operation(item, ['96.7000', '96.7100', '96.7101', '96.7200', '96.7201']) or
            has_invasive_mechanical_ventilation_treatment(item)
        )
    ]
    return {
        "data": filtered,
        "value": len(filtered),
    }

# 同期曾行有创机械通气的住院患者总人次数
# 1、病案首页出院科室为呼吸内科
# 2、病案首页有创呼吸机使用时间>0或病案首页手术操作编码含有创机械通气（见字典表）
def 同期曾行有创机械通气的住院患者总人次数(data: list):
    filtered = [
        item for item in data
        if out_from_breath(item)
        and (
            match_surgery_operation(item, ['96.7000', '96.7100', '96.7101', '96.7200', '96.7201']) or
            has_invasive_mechanical_ventilation_treatment(item)
        )
    ]

    return {
        "data": filtered,
        "value": len(filtered),
    }
