import serial
import serial.tools.list_ports
import threading
import time
import logging
from typing import Optional, Callable, List
from queue import Queue, Empty


class SerialCommunicator:
    """
    串口通信工具类
    提供串口连接、数据发送、数据接收等功能
    """
    
    def __init__(self):
        self.serial_port: Optional[serial.Serial] = None
        self.is_connected = False
        self.is_listening = False
        self.listen_thread: Optional[threading.Thread] = None
        self.receive_queue = Queue()
        self.data_callback: Optional[Callable] = None
        self.logger = logging.getLogger(__name__)

        # DEBUG
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def __repr__(self):
        return f"SerialCommunicator(is_connected={self.is_connected}, is_listening={self.is_listening}, serial_port={self.serial_port}, receive_queue_size={self.receive_queue.qsize()})"

    def get_available_ports(self) -> List[str]:
        """
        获取可用的串口列表
        
        Returns:
            List[str]: 可用串口名称列表
        """
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def connect(self, port: str, baudrate: int = 9600, timeout: float = 1.0, 
                bytesize: int = 8, parity: str = 'N', stopbits: int = 1) -> bool:
        """
        连接串口
        
        Args:
            port (str): 串口名称，如 'COM1' 或 '/dev/ttyUSB0'
            baudrate (int): 波特率，默认9600
            timeout (float): 超时时间（秒），默认1.0
            bytesize (int): 数据位，默认8
            parity (str): 校验位，'N'(无)/'E'(偶)/'O'(奇)，默认'N'
            stopbits (int): 停止位，默认1
            
        Returns:
            bool: 连接成功返回True，失败返回False
        """
        try:
            if self.is_connected:
                self.disconnect()
                
            self.serial_port = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout,
                bytesize=bytesize,
                parity=parity,
                stopbits=stopbits
            )
            
            self.is_connected = True
            self.logger.info(f"串口 {port} 连接成功，波特率: {baudrate}")
            return True
            
        except serial.SerialException as e:
            self.logger.error(f"串口连接失败: {e}")
            return False
        except Exception as e:
            self.logger.error(f"连接串口时发生未知错误: {e}")
            return False
    
    def disconnect(self):
        """
        断开串口连接
        """
        try:
            # 停止监听
            self.stop_listening()
            
            # 关闭串口
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
                
            self.is_connected = False
            self.serial_port = None
            self.logger.info("串口已断开")
            
        except Exception as e:
            self.logger.error(f"断开串口时发生错误: {e}")
    
    def send_data(self, data: str, encoding: str = 'utf-8') -> bool:
        """
        发送字符串数据
        
        Args:
            data (str): 要发送的字符串
            encoding (str): 编码方式，默认utf-8
            
        Returns:
            bool: 发送成功返回True，失败返回False
        """
        if not self.is_connected or not self.serial_port:
            self.logger.error("串口未连接")
            return False
            
        try:
            bytes_data = data.encode(encoding)
            bytes_written = self.serial_port.write(bytes_data)
            self.serial_port.flush()  # 确保数据立即发送
            self.logger.debug(f"发送数据: {data} ({bytes_written} 字节)")
            return True
            
        except Exception as e:
            self.logger.error(f"发送数据失败: {e}")
            return False
    
    def send_bytes(self, data: bytes) -> bool:
        """
        发送字节数据
        
        Args:
            data (bytes): 要发送的字节数据
            
        Returns:
            bool: 发送成功返回True，失败返回False
        """
        if not self.is_connected or not self.serial_port:
            self.logger.error("串口未连接")
            return False
            
        try:
            bytes_written = self.serial_port.write(data)
            self.serial_port.flush()
            self.logger.debug(f"发送字节数据: {data.hex()} ({bytes_written} 字节)")
            return True
            
        except Exception as e:
            self.logger.error(f"发送字节数据失败: {e}")
            return False
    
    def receive_data(self, size: int = 1024, encoding: str = 'utf-8') -> Optional[str]:
        """
        接收字符串数据（阻塞式）
        
        Args:
            size (int): 最大接收字节数，默认1024
            encoding (str): 解码方式，默认utf-8
            
        Returns:
            Optional[str]: 接收到的字符串，失败返回None
        """
        if not self.is_connected or not self.serial_port:
            self.logger.error("串口未连接")
            return None
            
        try:
            data = self.serial_port.read(size)
            if data:
                decoded_data = data.decode(encoding, errors='ignore').strip()
                self.logger.debug(f"接收数据: {decoded_data}")
                return decoded_data
            return None
            
        except Exception as e:
            self.logger.error(f"接收数据失败: {e}")
            return None
    
    def receive_bytes(self, size: int = 1024) -> Optional[bytes]:
        """
        接收字节数据（阻塞式）
        
        Args:
            size (int): 最大接收字节数，默认1024
            
        Returns:
            Optional[bytes]: 接收到的字节数据，失败返回None
        """
        if not self.is_connected or not self.serial_port:
            self.logger.error("串口未连接")
            return None
            
        try:
            data = self.serial_port.read(size)
            if data:
                self.logger.debug(f"接收字节数据: {data.hex()}")
                return data
            return None
            
        except Exception as e:
            self.logger.error(f"接收字节数据失败: {e}")
            return None
    
    def start_listening(self, callback: Optional[Callable] = None):
        """
        开始异步监听串口数据
        
        Args:
            callback (Optional[Callable]): 数据接收回调函数，参数为接收到的字符串
        """
        if not self.is_connected:
            self.logger.error("串口未连接，无法开始监听")
            return
            
        if self.is_listening:
            self.logger.warning("已在监听中")
            return
            
        self.data_callback = callback
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        self.logger.info("开始监听串口数据")
    
    def stop_listening(self):
        """
        停止监听串口数据
        """
        if not self.is_listening:
            return
            
        self.is_listening = False
        if self.listen_thread and self.listen_thread.is_alive():
            self.listen_thread.join(timeout=2.0)
        self.logger.info("停止监听串口数据")
    
    def _listen_loop(self):
        """
        监听循环（内部方法）
        """
        while self.is_listening and self.is_connected:
            try:
                if self.serial_port and self.serial_port.in_waiting > 0:
                    data = self.serial_port.read(self.serial_port.in_waiting)
                    if data:
                        # print(f"接收到原始数据: {data.hex()}")
                        if self.data_callback:
                            try:
                                self.data_callback(data)
                            except Exception as e:
                                self.logger.error(f"回调函数执行错误: {e}")
                
                time.sleep(0.01)  # 避免过度占用CPU
                
            except Exception as e:
                self.logger.error(f"监听过程中发生错误: {e}")
                break
    
    def get_received_data(self, timeout: float = 0.1) -> Optional[str]:
        """
        从接收队列中获取数据（非阻塞）
        
        Args:
            timeout (float): 超时时间，默认0.1秒
            
        Returns:
            Optional[str]: 接收到的数据，无数据返回None
        """
        try:
            return self.receive_queue.get(timeout=timeout)
        except Empty:
            return None
    
    def clear_receive_buffer(self):
        """
        清空接收缓冲区
        """
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.reset_input_buffer()
        
        # 清空接收队列
        while not self.receive_queue.empty():
            try:
                self.receive_queue.get_nowait()
            except Empty:
                break
    
    def get_port_info(self) -> dict:
        """
        获取当前串口信息
        
        Returns:
            dict: 串口信息字典
        """
        if not self.serial_port:
            return {}
            
        return {
            'port': self.serial_port.port,
            'baudrate': self.serial_port.baudrate,
            'bytesize': self.serial_port.bytesize,
            'parity': self.serial_port.parity,
            'stopbits': self.serial_port.stopbits,
            'timeout': self.serial_port.timeout,
            'is_open': self.serial_port.is_open,
            'in_waiting': self.serial_port.in_waiting if self.serial_port.is_open else 0
        }
    
    def __del__(self):
        """
        析构函数，确保资源正确释放
        """
        self.disconnect()


# 使用示例函数
def example_usage():
    """
    串口通信使用示例
    """
    # 创建串口通信对象
    serial_comm = SerialCommunicator()
    
    # 获取可用串口
    ports = serial_comm.get_available_ports()
    print(f"可用串口: {ports}")
    
    if not ports:
        print("没有找到可用串口")
        return
    
    # 连接串口（使用第一个可用串口）
    port = ports[0]  # 或者指定具体串口如 'COM3'
    if serial_comm.connect(port, baudrate=9600):
        print(f"成功连接到串口 {port}")
        
        # 定义数据接收回调函数
        def on_data_received(data):
            print(f"接收到数据: {data}")
        
        # 开始异步监听
        serial_comm.start_listening(callback=on_data_received)
        
        # 发送数据
        serial_comm.send_data("Hello, Serial!")
        serial_comm.send_data("AT\r\n")  # AT命令示例
        
        # 发送字节数据
        serial_comm.send_bytes(b'\x01\x02\x03\x04')
        
        # 等待一段时间让数据传输
        time.sleep(2)
        
        # 从队列获取接收到的数据
        while True:
            received = serial_comm.get_received_data()
            if received is None:
                break
            print(f"队列中的数据: {received}")
        
        # 同步接收数据示例
        print("等待同步接收数据...")
        sync_data = serial_comm.receive_data()
        if sync_data:
            print(f"同步接收到: {sync_data}")
        
        # 获取串口信息
        info = serial_comm.get_port_info()
        print(f"串口信息: {info}")
        
        # 断开连接
        serial_comm.disconnect()
        print("串口已断开")
    else:
        print(f"连接串口 {port} 失败")


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 运行示例
    example_usage()