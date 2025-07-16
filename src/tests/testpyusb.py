import sys
import os
import usb.util
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest

class TestPyUSB(unittest.TestCase):
    def test_device_connect(self):
        usb_devices = usb.core.find(find_all=True)
        for i in usb_devices:
            print(f"Total USB devices found: {i}")

if __name__ == '__main__':
    unittest.main()