import datetime
import os
import openpyxl
from io import BytesIO
from typing import TypedDict, NotRequired, List

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

class SheetSpec(TypedDict):
    path: str
    number: NotRequired[int]

def get_sheets(sheets: List[SheetSpec]):
    headers_all = []
    seen = set()
    data_all = []
    for sheet in sheets:
        result = get_sheet(sheet["path"], sheet.get("number", 0))
        headers = result["headers"]
        data = result["data"]
        for h in headers:
            if h not in seen:
                seen.add(h)
                headers_all.append(h)
        data_all.extend(data)
    return {
        "headers": headers_all,
        "data": data_all,
    }

_ALL_FILES_CACHE = None
_ALL_FILES_CACHE_SIGNATURE = None

def _files_signature(base: str = './files'):
    if not os.path.isdir(base):
        return ()
    items = []
    for name in os.listdir(base):
        if not name.lower().endswith('.xlsx'):
            continue
        if name.startswith('~'):
            continue
        p = os.path.join(base, name)
        try:
            m = os.path.getmtime(p)
        except Exception:
            m = 0
        items.append((name, m))
    items.sort()
    return tuple(items)

def list_excel_files(base: str = './files') -> List[SheetSpec]:
    res: List[SheetSpec] = []
    if os.path.isdir(base):
        for name in os.listdir(base):
            if not name.lower().endswith('.xlsx'):
                continue
            if name.startswith('~'):
                continue
            res.append({"path": os.path.join(base, name)})
    return res

def get_all_files_sheets(base: str = './files'):
    global _ALL_FILES_CACHE, _ALL_FILES_CACHE_SIGNATURE
    sig = _files_signature(base)
    if _ALL_FILES_CACHE is None or _ALL_FILES_CACHE_SIGNATURE != sig:
        sheets = list_excel_files(base)
        if not sheets:
            _ALL_FILES_CACHE = {"headers": [], "data": []}
        else:
            _ALL_FILES_CACHE = get_sheets(sheets)
        _ALL_FILES_CACHE_SIGNATURE = sig
    return _ALL_FILES_CACHE
