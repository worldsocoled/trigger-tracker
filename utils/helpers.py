from datetime import datetime

def format_timestamp(ts=None):
    if ts is None:
        ts = datetime.now()
    return ts.strftime("%Y-%m-%d %H:%M:%S")

def validate_intensity(value):
    return max(1, min(10, value))