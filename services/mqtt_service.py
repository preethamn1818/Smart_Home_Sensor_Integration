"""
MQTT client implementation for IMU sensor
"""
import paho.mqtt.client as mqtt
import json
import time
from config.settings import Settings
import logging

logger = logging.getLogger(__name__)

class IMUClient:
    def __init__(self, data_buffer, db_service):
        """
        Initialize MQTT client for IMU sensor
        
        Args:
            data_buffer: DataBuffer instance for storing readings
            db_service: DatabaseService instance for persistence
        """
        self.data_buffer = data_buffer
        self.db_service = db_service
        
        # Initialize MQTT client
        client_id = f'imu_client_{time.time()}'
        self.client = mqtt.Client(client_id=client_id)
        
        # Only set username/password if they are provided in settings
        if Settings.MQTT_USERNAME and Settings.MQTT_PASSWORD:
            self.client.username_pw_set(Settings.MQTT_USERNAME, Settings.MQTT_PASSWORD)
        
        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        logger.info("IMU MQTT client initialized")

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects to the broker"""
        if rc == 0:
            logger.info("Connected to local MQTT broker")
            client.subscribe(Settings.MQTT_TOPIC)
            logger.info(f"Subscribed to topic: {Settings.MQTT_TOPIC}")
        else:
            logger.error(f"Connection to local broker failed with code {rc}")

    def on_message(self, client, userdata, msg):
        """Callback for when a message is received"""
        try:
            # Decode and parse the message
            received_data = msg.payload.decode()
            values = json.loads(received_data)
            
            # Check if the message contains IMU data
            if isinstance(values, list) and len(values) == 2:
                acc = list(values[0])
                gyro = list(values[1])
                
                # Store accelerometer data
                for i, value in enumerate(['x', 'y', 'z']):
                    self.data_buffer.add_data(f'imu_acc', acc[i])
                    self.db_service.save_sensor_data(
                        sensor_type='imu_accelerometer',
                        value_type=f'acc_{value}',
                        value=acc[i]
                    )
                
                # Store gyroscope data
                for i, value in enumerate(['x', 'y', 'z']):
                    self.data_buffer.add_data(f'imu_gyro', gyro[i])
                    self.db_service.save_sensor_data(
                        sensor_type='imu_gyroscope',
                        value_type=f'gyro_{value}',
                        value=gyro[i]
                    )

                logger.debug(f"Processed IMU data - Acc: {acc}, Gyro: {gyro}")
            else:
                logger.warning(f"Received unexpected data format: {received_data}")
            
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON message: {e}")
        except Exception as e:
            logger.error(f"Error processing IMU message: {e}")

    def on_disconnect(self, client, userdata, rc):
        """Callback for when client disconnects"""
        logger.warning(f"Disconnected from local broker with code: {rc}")
        if rc != 0:
            logger.info("Attempting to reconnect to local broker...")

    def run(self):
        """Main client loop"""
        while True:
            try:
                logger.info(f"Connecting to local MQTT broker at {Settings.MQTT_HOST}:{Settings.MQTT_PORT}")
                self.client.connect(Settings.MQTT_HOST, Settings.MQTT_PORT, 60)
                self.client.loop_forever()
            except Exception as e:
                logger.error(f"Local MQTT connection error: {e}")
                logger.info("Retrying in 5 seconds...")
                time.sleep(5)  # Wait before retrying