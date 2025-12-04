from utils.excel import get_sheet
from datetime import datetime
from collections import defaultdict
from typing import Counter
from utils.excel import get_diagnosis_names

# 24行 - 因异位妊娠死亡的患者例数
def 因异位妊娠死亡的患者例数(data: list):
    diagnosis_names = get_diagnosis_names('异位妊娠')

    filtered_data = [
        item for item in data
        if '妇科' in str(item.get('出院科室'))
        and any(name in str(item.get('主诊断')) for name in diagnosis_names)
        and '死亡' in str(item.get('治疗结果'))
    ]
    return filtered_data

# 27行 - 同期妇科恶性肿瘤住院患者总例数
def 同期妇科恶性肿瘤住院患者总例数(data: list):
    diagnosis_names = get_diagnosis_names('妇科恶性肿瘤')

    filtered_data = [
        item for item in data
        if '妇科' in str(item.get('出院科室', ''))
        and any(name in str(item.get('主诊断')) for name in diagnosis_names)
    ]
    return filtered_data

# 34行 - 出院31天内非预期再住院患者人次数
def 出院31天内非预期再住院患者人次数(data: list): 
    # 1. 筛选「出院科室」包含「呼吸」的数据
    filtered_data = [
        item for item in data
        if '呼吸' in str(item.get('出院科室', ''))
    ]

    # 统计每个病人身份证号出现的次数
    name_counts = Counter(item['身份证号'] for item in filtered_data)
    # 筛选出出现多次的病人身份证号
    duplicate_names = {name for name, count in name_counts.items() if count > 1}
    # 按病人姓名分组，只保留出现多次的病人姓名的数据
    grouped_data = defaultdict(list)
    for item in filtered_data:
        name = item['身份证号']
        if name in duplicate_names:
            grouped_data[name].append(item)

    # 转成普通字典方便查看
    grouped_data = dict(grouped_data)

    next_res = []
    for(name, items) in grouped_data.items():
        # 2. 按入院日期排序
        sorted_data = sorted(items, key=lambda x: x['入院日期'])
        # 遍历数据，从第二条开始
        for i in range(1, len(sorted_data)):
            # 解析日期字符串为 datetime 对象
            prev_discharge = datetime.strptime(sorted_data[i-1]['出院日期'], '%Y-%m-%d')
            curr_admission = datetime.strptime(sorted_data[i]['入院日期'], '%Y-%m-%d')
            
            # 计算时间差（天数）
            diff_days = (curr_admission - prev_discharge).days
            
            # 判断时间差是否小于等于31天
            if 0 <= diff_days <= 31:
                next_res.append(sorted_data[i])
    return next_res

def get_indicators():
    return [
        '因异位妊娠死亡的患者例数',
        '同期妇科恶性肿瘤住院患者总例数',
        '出院31天内非预期再住院患者人次数',
    ]

def get_indicator_value(indicator: str):
    sheet = get_sheet("./files/2024年病案首页.xlsx", 0)
    data = sheet["data"]
    headers = sheet["headers"]
    match indicator:
        case '因异位妊娠死亡的患者例数':
            result = 因异位妊娠死亡的患者例数(data)
        case '同期妇科恶性肿瘤住院患者总例数':
            result = 同期妇科恶性肿瘤住院患者总例数(data)
        case '出院31天内非预期再住院患者人次数':
            result = 出院31天内非预期再住院患者人次数(data)
        case _:
            result = None
    return None if result is None else {"headers": headers, "data": result}

