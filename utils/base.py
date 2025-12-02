from datetime import datetime

def safe_parse_date(v: str):
    try:
        return datetime.strptime(v, '%Y-%m-%d')
    except Exception:
        return None
