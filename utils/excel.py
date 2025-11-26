import datetime
import openpyxl
from io import BytesIO

def get_sheet(path: str, number: int = 0):
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

    return {
        "headers": headers,
        "data": data,
    }

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
