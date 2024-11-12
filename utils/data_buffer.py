"""
Data buffer management using thread-safe deque
"""
from collections import deque
from threading import Lock
from config.settings import Settings

class DataBuffer:
    def __init__(self):
        self.buffer_size = Settings.BUFFER_SIZE
        self.buffers = {
            'humidity': deque(maxlen=self.buffer_size),
            'temperature': deque(maxlen=self.buffer_size),
            'gas': deque(maxlen=self.buffer_size),
            'imu_acc': deque(maxlen=self.buffer_size),
            'imu_gyro': deque(maxlen=self.buffer_size)
        }
        self.locks = {key: Lock() for key in self.buffers.keys()}
    
    def add_data(self, sensor_type: str, data):
        with self.locks[sensor_type]:
            self.buffers[sensor_type].append(data)
    
    def get_data(self, sensor_type: str):
        with self.locks[sensor_type]:
            return list(self.buffers[sensor_type])