"""
IMU sensor data sent using local MQTT broker
Simulates accelerometer and gyroscope data
"""
import paho.mqtt.client as mqtt
import json
import time
import random
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IMUSender:
    def __init__(self, host="localhost", port=1883, topic="sensors/imu"):
        self.host = host
        self.port = port
        self.topic = topic
        
        # Initialize MQTT client
        client_id = f'imu_sender_{int(time.time())}'
        self.client = mqtt.Client(client_id=client_id)
        
        # Connect callback for logging
        self.client.on_connect = self.on_connect
        
        logger.info(f"IMU sender initialized for {host}:{port} on topic {topic}")
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback for connection logging"""
        if rc == 0:
            logger.info("Connected to local MQTT broker")
        else:
            logger.error(f"Connection failed with code {rc}")
            
    def simulate_imu_data(self):
        """
        Simulate realistic IMU data
        Returns: tuple of accelerometer and gyroscope data
        """
        # Simulate accelerometer data (in g)
        acc_x = random.gauss(-2, 2)  
        acc_y = random.gauss(-2, 2)  
        acc_z = random.gauss(-2, 2)  
        
        # Simulate gyroscope data (in degrees/second)
        gyro_x = random.gauss(-200, 200)
        gyro_y = random.gauss(-200, 200)
        gyro_z = random.gauss(-200, 200)
        
        return [acc_x, acc_y, acc_z], [gyro_x, gyro_y, gyro_z]
        
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.host, self.port, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False
            
    def send_data(self):
        """Send IMU data to broker"""
        if not self.connect():
            return
            
        try:
            while True:
                # Generate IMU data
                acc_data, gyro_data = self.simulate_imu_data()
                
                # Create message payload
                message = json.dumps([acc_data, gyro_data])
                
                # Publish data
                self.client.publish(self.topic, message)
                logger.info(f"{datetime.now()} - Sent IMU data:")
                logger.info(f"Acc (x,y,z): {acc_data}")
                logger.info(f"Gyro (x,y,z): {gyro_data}")
                
                time.sleep(0.1)  # Send at 10Hz
                
        except KeyboardInterrupt:
            logger.info("Stopping IMU sender...")
            self.client.loop_stop()
            self.client.disconnect()
        except Exception as e:
            logger.error(f"Error in sending data: {e}")
            self.client.loop_stop()
            self.client.disconnect()

if __name__ == "__main__":
    # Create and run sender
    sender = IMUSender(
        host="localhost",  # Use your Mosquitto broker address
        port=1883,        # Default MQTT port
        topic="sensors/imu"  # Topic to publish to
    )
    
    try:
        sender.send_data()
    except KeyboardInterrupt:
        print("\nStopping IMU sender...")