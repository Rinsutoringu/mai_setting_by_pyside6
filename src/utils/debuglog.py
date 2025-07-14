import datetime

def debug_log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] [调试信息]: {msg}"