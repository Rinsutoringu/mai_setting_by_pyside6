import sys
import os
from utils.debuglog import debug_log
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from utils.package_receive import package_receive

class TestPackageReceive(unittest.TestCase):
    def setUp(self):
        self.package_receiver = package_receive()

    def test_receive_byte(self):
        # 测试接收包开始标志
        self.package_receiver.receive_byte(0x53)
        print(debug_log("尝试输入0x53, 流处理标志当前状态为", self.package_receiver.state))
        self.assertEqual(self.package_receiver.state, self.package_receiver.IN_PACKET)
        
        # 测试接收数据
        self.package_receiver.receive_byte(0x01)
        print(debug_log("当前缓冲区内容", self.package_receiver.buffer))

        self.package_receiver.receive_byte(0x02)
        print(debug_log("当前缓冲区内容", self.package_receiver.buffer))

        self.assertEqual(len(self.package_receiver.buffer), 3)

    def test_full_pack(self):
        # 测试标准数据包
        test_data = bytearray([0x53, 0x10, 0x01, 0x03, 0x50, 0x83, 0x33])
        true_result = bytearray([0x53, 0x10, 0x01, 0x03, 0x50, 0x83, 0x33])
        for byte in test_data:
            result = self.package_receiver.receive_byte(byte)
            if result:
                print(debug_log("接收到完整包", result.hex()))
                self.assertEqual(result, true_result)
                print(debug_log("PASS"))

        # 测试长度为0的包
        test_data = bytearray([0x53, 0x10, 0x01, 0x00, 0x50, 0x83, 0x33])
        true_result = bytearray([0x53, 0x10, 0x01, 0x00])
        for byte in test_data:
            result = self.package_receiver.receive_byte(byte)
            if result:
                print(debug_log("接收到完整包", result.hex()))
                self.assertEqual(result, true_result)
                print(debug_log("PASS"))

        # 测试带有转义字符的数据包
        test_data = bytearray([0x53, 0x10, 0x01, 0x03, 0x7c, 0x50, 0x83, 0x33])
        true_result = bytearray([0x53, 0x10, 0x01, 0x03, 0x50, 0x83, 0x33])
        for byte in test_data:
            result = self.package_receiver.receive_byte(byte)
            if result:
                print(debug_log("接收到完整包", result.hex()))
                self.assertEqual(result, true_result)
                print(debug_log("PASS"))

        # 测试带有转义字符的数据包
        test_data = bytearray([0x53, 0x10, 0x01, 0x04, 0x7c, 0x7c, 0x50, 0x83, 0x33])
        true_result = bytearray([0x53, 0x10, 0x01, 0x04, 0x7c, 0x50, 0x83, 0x33])
        for byte in test_data:
            result = self.package_receiver.receive_byte(byte)
            if result:
                print(debug_log("接收到完整包", result.hex()))
                self.assertEqual(result, true_result)
                print(debug_log("PASS"))

        result = self.package_receiver.isFinish()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()