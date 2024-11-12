"""
Humidity sensor data through HTTP
"""
import requests
import time
import random
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HumiditySender:
    def __init__(self, host="192.168.0.162", port=8000):
        self.url = f"http://{host}:{port}/humidity"
        
    def simulate_humidity(self):
        # Simulate indoor humidity with gradual changes
        base_humidity = 45.0  # Base humidity level
        variation = random.uniform(-5.0, 5.0)  # Random variation
        return max(min(base_humidity + variation, 100.0), 0.0)  # Clamp between 0-100%
        
    def send_data(self):
        # Sending humidity data to server
        while True:
            try:
                humidity = self.simulate_humidity()
                response = requests.post(
                    self.url,
                    json={"humidity": humidity}
                )
                
                if response.status_code == 200:
                    logger.info(f"{datetime.now()} - Sent humidity: {humidity:.2f}%")
                else:
                    logger.error(f"Server error: {response.status_code} - {response.text}")
                    
                time.sleep(0.01)  # 100 hz
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error sending data: {e}")
                time.sleep(2)  # Wait before retrying