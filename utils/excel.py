import datetime
import os
import openpyxl
from io import BytesIO
from typing import TypedDict, NotRequired, List

def load_sheet(path: str, number: int = 0):
    key = (path, number)
    if not hasattr(load_sheet, '_cache'):
        load_sheet._cache = {}
    cache = load_sheet._cache
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

def get_all_departments(data: list):
    header = '出院病房(CYBF)'
    # 收集所有非空的入院病房值
    departments = [
        str(item[header])
        for item in data
        if header in item and item[header] is not None and str(item[header]).strip() != ''
    ]
    # 去重并保持原顺序
    seen = set()
    unique_departments = []
    for dept in departments:
        if dept not in seen:
            seen.add(dept)
            unique_departments.append(dept)
    return unique_departments

class SheetSpec(TypedDict):
    path: str
    number: NotRequired[int]

def load_sheets(sheets: List[SheetSpec]):
    headers_all = []
    seen = set()
    data_all = []
    for sheet in sheets:
        result = load_sheet(sheet["path"], sheet.get("number", 0))
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

def _files_signature(base: str = './files/2022'):
    if not os.path.isdir(base):
        return ()
    items = []
    # 递归遍历目录
    for root, _, files in os.walk(base):
        for name in files:
            if not name.lower().endswith('.xlsx'):
                continue
            if name.startswith('~'):
                continue
            p = os.path.join(root, name)
            try:
                m = os.path.getmtime(p)  # 获取文件的最后修改时间戳
            except Exception:
                m = 0
            # 保存相对路径，保持排序一致性
            rel_path = os.path.relpath(p, base)
            items.append((rel_path, m))
    items.sort()
    return tuple(items)

def list_excel_files(base: str = './files/2022') -> List[SheetSpec]:
    res: List[SheetSpec] = []
    if os.path.isdir(base):
        # 递归遍历目录
        for root, _, files in os.walk(base):
            for name in files:
                if not name.lower().endswith('.xlsx'):
                    continue
                if name.startswith('~'):
                    continue
                # 保存相对路径，保持与_files_signature一致
                rel_path = os.path.relpath(os.path.join(root, name), base)
                res.append({"path": os.path.join(base, rel_path)})
    return res

def get_all_files_sheets(base: str = './files/2022'):
    global _ALL_FILES_CACHE, _ALL_FILES_CACHE_SIGNATURE
    sig = _files_signature(base) 
    if _ALL_FILES_CACHE is None or _ALL_FILES_CACHE_SIGNATURE != sig:
        sheets = list_excel_files(base)
        if not sheets:
            _ALL_FILES_CACHE = {"headers": [], "data": []}
        else:
            _ALL_FILES_CACHE = load_sheets(sheets)
        _ALL_FILES_CACHE_SIGNATURE = sig
    return _ALL_FILES_CACHE

def get_diagnosis_names(name: str):
    sheet = load_sheet("./back/0妇科-重点专业单病种质控指标.xlsx", 1)
    data = sheet["data"]
    # 筛选「字典名称」为‘异位妊娠’的数据，取「名称」字段放入列表
    filter_item = [
        item for item in data
        if str(item.get('字典名称')) == name
    ]
    names = [item['名称'] for item in filter_item]
    
    return names