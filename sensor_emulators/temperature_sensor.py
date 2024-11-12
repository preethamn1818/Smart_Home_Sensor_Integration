"""
Temperature sensor data sender using TCP
"""
import socket
import time
import struct
import random
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TemperatureSender:
    def __init__(self, host="192.168.0.162", port=5005):
        self.host = host
        self.port = port
        self.sock = None
        self.connected = False
        
    def connect(self):
        """Establish TCP connection with server"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.connected = True
            logger.info(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.connected = False
            
    def simulate_temperature(self):
        """
        Simulate realistic temperature data
        Returns temperature in Celsius
        """
        # Simulate room temperature with small variations
        base_temp = 23.0  # Base room temperature
        variation = random.uniform(-1.0, 1.0)  # Random variation
        return base_temp + variation
        
    def send_data(self):
        """Send temperature data to server"""
        while True:
            try:
                if not self.connected:
                    self.connect()
                    time.sleep(1)
                    continue
                
                temperature = self.simulate_temperature()
                # Pack float to bytes
                data = struct.pack('f', temperature)
                self.sock.sendall(data)
                
                logger.info(f"{datetime.now()} - Sent temperature: {temperature:.2f}°C")
                time.sleep(0.01)  # 100 hz
                
            except Exception as e:
                logger.error(f"Error sending data: {e}")
                self.connected = False
                if self.sock:
                    self.sock.close()
                time.sleep(2)  # Wait before reconnecting