from utils.doctor import (
    get_actual_inpatient_days,
    get_diagnosis_codes,
    match_diagnosis,
    match_surgery_operation,
    no_admit_diagnosis,
    not_match_diagnosis,
    out_from_endocrinology,
    not_dead
)

def is_endocrinology_department(year: str, department: str):
    if('内分泌' in department):
        return True
    return False

# 病案首页出院科别为内分泌科的患者总数
def 内分泌_同期住院患者总病例数(data: list):
    filter = [
        item for item in data
        if out_from_endocrinology(item)
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 病案首页出院科别为内分泌科的患者住院天数总和
def 内分泌_实际使用的总床日数(data: list):
    filter = [
        item for item in data
        if out_from_endocrinology(item)
    ]
    total_days = get_actual_inpatient_days(filter)

    return {
        "data": filter,
        "value": total_days,
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页主要诊断编码为重点病种：
# 糖尿病伴有酮症酸中毒、
# 2 型糖尿病并发肾病、
# 2 型糖尿病并发增殖性视网膜病、
# 2 型糖尿病足病、
# 甲状腺功能亢进症、
# 甲状腺危象、
# 甲状旁腺肿瘤、
# 甲状旁腺功能亢进症、
# 甲状旁腺功能减退症、
# 垂体肿瘤、
# 肾上腺肿瘤、
# 重度肥胖
#（编码见字典表）的患者总数
# 病案首页离院方式为非死亡
def 内分泌_重点病种患者例数(data: list):
    codes = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '重点病种')

    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
    ]

    return {
        "data": filter,
        "value": len(filter),
    }

def 内分泌_重点病种患者例数_不包含死亡(data: list):
    codes = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '重点病种')

    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
        and not_dead(item)
    ]

    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页主要诊断编码为疑难病种：2 型糖尿病伴有多个并发症、糖尿病性周围血管病变、甲状腺恶性肿瘤、甲状腺功能亢进性突眼症、甲状腺毒症伴有毒性多结节性甲状腺肿、肢端肥大症、抗利尿激素不恰当分泌综合征、尿崩症、库欣综合征、醛固酮增多症、先天性肾上腺皮质增生症、糖原贮积病、多发性内分泌腺瘤病（见字典表）的患者总数
def 内分泌_疑难病种患者例数(data: list):
    codes = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '疑难病种')

    filter = [
        item for item in data
        if out_from_endocrinology(item)
          and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页出院主要诊断不是糖尿病相关诊断编码的患者数（糖尿病相关诊断编码见字典表）
def 非糖尿病住院患者人次数(data: list):
    codes1 = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '糖尿病')
    codes2 = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '2型糖尿病')
    codes3 = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '糖尿病高血糖高渗状态')
    codes4 = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '糖尿病酮症酸中毒')

    codes = codes1 + codes2 + codes3 + codes4

    print(len(codes))

    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (not_match_diagnosis(item, codes, {'from': 0, 'to': 1}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页出院主要诊断编码为糖尿病酮症酸中毒（见字典表）
def 同期糖尿病酮症酸中毒患者总人次数(data: list):
    codes = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '糖尿病酮症酸中毒')

    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页主要诊断编码有高血糖高渗状态（见字典表）
def 同期糖尿病高血糖高渗状态患者总人次数(data: list):
    codes = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '糖尿病高血糖高渗状态')

    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页主要诊断为糖尿病相关编码（见字典表）
def 同期糖尿病住院患者总人次数(data: list):
    codes1 = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '糖尿病')
    codes2 = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '2型糖尿病')
    codes3 = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '糖尿病高血糖高渗状态')
    codes4 = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '糖尿病酮症酸中毒')

    codes = codes1 + codes2 + codes3 + codes4

    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, codes, {'from': 0, 'to': 1}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页主要诊断为糖尿病相关编码（见字典表）
def 糖尿病住院患者应用血糖_血压和血脂监测的人次数(data: list):
    codes = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '糖尿病')

    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, codes))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页前三出院诊断编码中含甲状腺功能亢进编码E05
def 同期甲状腺功能亢进症患者总例数(data: list):
    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, ['E05.'], {'from': 0, 'to': 3}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页主要诊断为甲状腺结节编码D34，E04.0，E04.1，E04.2，E04.9
# 3、病案首页手术及操作编码中含06.1100闭合性[经皮][针吸]甲状腺活组织检查、06.1101超声引导下经皮甲状腺活组织检查术
def 甲状腺结节患者行甲状腺细针穿刺活检例数(data: list):
    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, ['D34.', 'E04.0', 'E04.1', 'E04.2', 'E04.9'], {'from': 0, 'to': 1}))
        and (match_surgery_operation(item, ['06.1100', '06.1101']))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页主要诊断为甲状腺结节编码D34，E04.0，E04.1，E04.2，E04.9
def 同期甲状腺结节患者总例数(data: list):
    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, ['D34.', 'E04.0', 'E04.1', 'E04.2', 'E04.9'], {'from': 0, 'to': 1}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页前三出院诊断编码中含E22.001肢端肥大症
# TODO: 前3是啥意思
def 同期肢端肥大症患者总例数(data: list):
    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, ['E22.001'], {'from': 0, 'to': 3}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页前三出院诊断编码中含E24库欣综合征
# 3、S31020600300010过夜地塞米松抑制试验、S31020600400010地塞米松抑制试验
def 库欣综合征患者完成地塞米松试验的例数(data: list):
    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, ['E24.'], {'from': 0, 'to': 3}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页前三出院诊断编码中含E24库欣综合征
def 同期库欣综合征患者总例数(data: list):
    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, ['E24.'], {'from': 0, 'to': 3}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页前三出院诊断编码中含M81.500特发性骨质疏松、M80.500特发性骨质疏松伴有病理性骨折
# 3、病案首页出院其他诊断中含原发性甲状旁腺亢进症（见字典表）且入院情况为无
def 骨质疏松症患者中PHPT_检出例数(data: list):
    codes = get_diagnosis_codes('./back/内分泌科-重点专业单病种质控指标.xlsx', 1, '原发性甲状旁腺功能亢进症')

    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, ['M81.500', 'M80.500'], {'from': 0, 'to': 3}))
        and (match_diagnosis(item, codes, {'from': 3, 'to': 5}))
        and (no_admit_diagnosis(item))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

# 1、病案首页出院科别为内分泌科
# 2、病案首页前三出院诊断编码中含M81.500特发性骨质疏松、M80.500特发性骨质疏松伴有病理性骨折
def 同期骨质疏松症患者总例数(data: list):
    filter = [
        item for item in data
        if out_from_endocrinology(item)
        and (match_diagnosis(item, ['M81.500', 'M80.500'], {'from': 0, 'to': 3}))
    ]
    return {
        "data": filter,
        "value": len(filter),
    }

INDICATOR_FUNC_MAP = {
    '（内分泌）同期住院患者总病例数': 内分泌_同期住院患者总病例数,
    '（内分泌）实际使用的总床日数': 内分泌_实际使用的总床日数,
    '（内分泌）重点病种患者例数': 内分泌_重点病种患者例数,
    '（内分泌）重点病种患者例数_不包含死亡': 内分泌_重点病种患者例数_不包含死亡,
    '（内分泌）疑难病种患者例数': 内分泌_疑难病种患者例数,
    '非糖尿病住院患者人次数': 非糖尿病住院患者人次数,
    '同期糖尿病酮症酸中毒患者总人次数': 同期糖尿病酮症酸中毒患者总人次数,
    '同期糖尿病高血糖高渗状态患者总人次数': 同期糖尿病高血糖高渗状态患者总人次数,
    '同期糖尿病住院患者总人次数': 同期糖尿病住院患者总人次数,
    '糖尿病住院患者应用血糖、血压和血脂监测的人次数': 糖尿病住院患者应用血糖_血压和血脂监测的人次数,
    '同期甲状腺功能亢进症患者总例数': 同期甲状腺功能亢进症患者总例数,
    '甲状腺结节患者行甲状腺细针穿刺活检例数': 甲状腺结节患者行甲状腺细针穿刺活检例数,
    '同期甲状腺结节患者总例数': 同期甲状腺结节患者总例数,
    '同期肢端肥大症患者总例数': 同期肢端肥大症患者总例数,
    '库欣综合征患者完成地塞米松试验的例数': 库欣综合征患者完成地塞米松试验的例数,
    '同期库欣综合征患者总例数': 同期库欣综合征患者总例数,
    '骨质疏松症患者中PHPT_检出例数': 骨质疏松症患者中PHPT_检出例数,
    '同期骨质疏松症患者总例数': 同期骨质疏松症患者总例数,
}


def get_indicators():
    return list(INDICATOR_FUNC_MAP.keys())

def get_endocrinology_indicator_detail(data: list, indicator: str):
    fn = INDICATOR_FUNC_MAP.get(indicator)
    if fn:
        return fn(data)
    return {
        "data": [],
        "value": 0,
    }