import re

def extract_device_number(device_str):
    match = re.match(r'Device\s+(\d+)', device_str)
    if match:
        return int(match.group(1))
    return None