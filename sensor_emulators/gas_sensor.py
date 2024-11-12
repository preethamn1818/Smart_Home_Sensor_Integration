"""
Gas sensor data through TCP
"""
import socket
import time
import struct
import random
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GasSender:
    def __init__(self, host="192.168.0.162", port=5010):
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
            
    def simulate_gas_reading(self):
        """
        Simulate realistic gas sensor data (PPM)
        Returns gas concentration in PPM
        """
        # Simulate normal air quality with occasional spikes
        base_level = 400.0  # Base CO2 level in PPM
        if random.random() < 0.1:  # 10% chance of a spike
            variation = random.uniform(0, 200.0)  # Larger variation for spikes
        else:
            variation = random.uniform(-20.0, 20.0)  # Normal variation
        return max(0, base_level + variation)
        
    def send_data(self):
        """Send gas sensor data to server"""
        while True:
            try:
                if not self.connected:
                    self.connect()
                    time.sleep(1)
                    continue
                
                gas_level = self.simulate_gas_reading()
                # Pack float to bytes
                data = struct.pack('f', gas_level)
                self.sock.sendall(data)
                
                logger.info(f"{datetime.now()} - Sent gas level: {gas_level:.2f} PPM")
                time.sleep(0.01)  # 100 hz
                
            except Exception as e:
                logger.error(f"Error sending data: {e}")
                self.connected = False
                if self.sock:
                    self.sock.close()
                time.sleep(2)  # Wait before reconnecting