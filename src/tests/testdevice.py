import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
import models.device_model as device_model
from utils.port_utils import find_device_usb_path

class TestDeviceModel(unittest.TestCase):
    def test_device_connect(self):
        device_paths = find_device_usb_path("0CA3", "0021")
        for path in device_paths:
            device = device_model.Device(device_path=path)
            self.assertTrue(device.check_connect())

if __name__ == '__main__':
    unittest.main()