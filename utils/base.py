from datetime import datetime

def safe_parse_data(v: str | None):
    try:
        if not v:
            return None
        return datetime.strptime(v, '%Y-%m-%d')
    except Exception:
        return None
