import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import models.device_model as device_model
from utils.port_utils import find_device_usb_path


device_paths = find_device_usb_path("0CA3", "0021")
devices = {}
# device = device_model.Device()

for i in range(len(device_paths)):
    devices[i] = device_model.Device(device_path=device_paths[i])
    if devices[i].check_connect():
        print(devices[i].getDevicePath()[0][58:68])
pass