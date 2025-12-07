def is_neurology_department(year: str, department: str):
    if('神经内科' in department):
        return True
    return False

def get_indicators():
    return [
      '同期神经内科收治脑梗死患者总例数',
      '同期神经内科收治患者总例数',
      '同期神经内科收治脑出血患者总例数',
      '神经内科收治惊厥性癫痫持续状态患者例数',
      '同期神经内科癫痫住院患者总例数',
      '神经内科收治惊厥性癫痫持续状态患者例数',
      '同期神经内科收治患者总例数',
      '神经内科住院患者死亡例数',
      '同期住院帕金森病患者总数',
    ]

def get_neurology_indicator_detail(data: list, indicator: str):
    return {
        "data": [],
        "value": 0,
    }

# 神经内科
# 同期神经内科收治脑梗死患者总例数
# 同期神经内科收治患者总例数
# 同期神经内科收治脑出血患者总例数
# 神经内科收治惊厥性癫痫持续状态患者例数
# 同期神经内科癫痫住院患者总例数
# 神经内科收治惊厥性癫痫持续状态患者例数
# 同期神经内科收治患者总例数
# 神经内科住院患者死亡例数
# 同期住院帕金森病患者总数