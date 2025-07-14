import datetime

def debug_log(*args):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = " ".join(str(arg) for arg in args)
    return f"[{timestamp}] [调试信息]: {msg}"