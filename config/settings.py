"""
Configuration settings for the sensor system
"""
class Settings:
    # Database URLs for different sensors
    DATABASES = {
        'humidity': {
            'url': "postgresql://postgres:Asdf%401234@localhost:5432/humidity_db",
            'name': "humidity_db"
        },
        'temperature': {
            'url': "postgresql://postgres:Asdf%401234@localhost:5432/temperature_db",
            'name': "temperature_db"
        },
        'imu': {
            'url': "postgresql://postgres:Asdf%401234@localhost:5432/imu_db",
            'name': "imu_db"
        },
        'gas': {
            'url': "postgresql://postgres:Asdf%401234@localhost:5432/gas_db",
            'name': "gas_db"
        }
    }
    
    # MQTT Settings for local Mosquitto broker
    MQTT_HOST = "localhost"
    MQTT_PORT = 1883
    MQTT_TOPIC = "sensors/imu"  # Based on your publisher/subscriber example
    # Remove Adafruit-specific credentials as they're not needed for local setup
    MQTT_USERNAME = None
    MQTT_PASSWORD = None
    
    # TCP Settings
    TCP_HOST = "192.168.0.162" # your ip4v address
    TEMPERATURE_PORT = 5005
    GAS_PORT = 5010
    
    # HTTP Settings
    HTTP_HOST = "192.168.0.162" # your ip4v address
    HTTP_PORT = 8000
    
    # Buffer Settings
    BUFFER_SIZE = 100