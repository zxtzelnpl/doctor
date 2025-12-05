import os
import json
from typing import TypedDict, NotRequired, List

def load_json(path: str, number: int = 0):
    key = (path, number)
    if not hasattr(load_json, '_cache'):
        load_json._cache = {}
    cache = load_json._cache
    if key in cache:
        return cache[key]

    with open(path, 'r', encoding='utf-8') as f:
        payload = json.load(f)
    sheets = payload.get('sheets', [])
    sheet = sheets[number] if number < len(sheets) else {}
    headers = sheet.get('headers', [])
    data = sheet.get('data', [])

    result = {
        "headers": headers,
        "data": data,
    }
    cache[key] = result
    return result

class JsonSpec(TypedDict):
    path: str
    number: NotRequired[int]

def load_jsons(file_list: List[JsonSpec]):
    from concurrent.futures import ThreadPoolExecutor
    headers_all = []
    seen = set()
    data_all = []
    max_workers = min(len(file_list) or 1, max(1, (os.cpu_count() or 4)))
    work_items = [{"path": os.path.abspath(s["path"]), "number": s.get("number", 0)} for s in file_list]
    def _task(spec: JsonSpec):
        return load_json(spec["path"], spec.get("number", 0))
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(_task, s) for s in work_items]
        results = []
        for fut in futures:
            try:
                results.append(fut.result())
            except Exception:
                results.append({"headers": [], "data": []})
    for result in results:
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

def list_json_files(base: str) -> List[JsonSpec]:
    res: List[JsonSpec] = []
    if os.path.isdir(base):
        for root, _, files in os.walk(base):
            for name in files:
                if not name.lower().endswith('.json'):
                    continue
                rel_path = os.path.relpath(os.path.join(root, name), base)
                res.append({"path": os.path.join(base, rel_path)})
    return res

def get_all_files_jsons(year: str):
    base_path = os.path.join('./files', year)
    sheets = list_json_files(base_path)        
    return load_jsons(sheets)
