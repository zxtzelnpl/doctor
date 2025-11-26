import datetime
import openpyxl
from io import BytesIO

def get_sheet(path: str, number: int = 0):
    key = (path, number)
    if not hasattr(get_sheet, '_cache'):
        get_sheet._cache = {}
    cache = get_sheet._cache
    if key in cache:
        return cache[key]

    book = openpyxl.load_workbook(path, number)
    sheetnames = book.sheetnames
    sheet = book[sheetnames[number]]

    headers = []
    for cell in sheet[1]:
        headers.append(cell.value)

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_dict = {headers[i]: row[i] for i in range(len(headers))}
        data.append(row_dict)

    result = {
        "headers": headers,
        "data": data,
    }
    cache[key] = result
    return result

def export_sheet(title: str, headers: list, data: list):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = title

    ws.append(headers)

    for record in data:
        row = [record.get(header, "") for header in headers]
        ws.append(row)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'导出{title}_{timestamp}.xlsx'

    return {
        "filename": filename,
        "output": output,
    }

def get_diagnosis_names(name: str):
    sheet = get_sheet("./files/0妇科-重点专业单病种质控指标.xlsx", 1)
    data = sheet["data"]
    # 筛选「字典名称」为‘异位妊娠’的数据，取「名称」字段放入列表
    filter_item = [
        item for item in data
        if str(item.get('字典名称')) == name
    ]
    names = [item['名称'] for item in filter_item]
    
    return names
