from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import Settings
from models.database import (
    HumidityBase, TemperatureBase, GasBase, IMUBase,
    HumidityReading, TemperatureReading, GasReading, IMUReading
)
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.engines = {}
        self.sessions = {}
        self.models = {
            'humidity': (HumidityBase, HumidityReading),
            'temperature': (TemperatureBase, TemperatureReading),
            'gas': (GasBase, GasReading),
            'imu': (IMUBase, IMUReading)
        }
        
        # Initialize databases
        for sensor_type, db_config in Settings.DATABASES.items():
            try:
                engine = create_engine(db_config['url'])
                SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
                
                self.engines[sensor_type] = engine
                self.sessions[sensor_type] = SessionLocal
                
                # Create tables using appropriate base
                base, _ = self.models[sensor_type]
                base.metadata.create_all(bind=engine)
                
                logger.info(f"Connected to {sensor_type} database")
            except Exception as e:
                logger.error(f"Error connecting to {sensor_type} database: {e}")

    def save_sensor_data(self, sensor_type: str, value: float, value_type: str = None):
        """
        Save sensor reading to appropriate database
        
        Args:
            sensor_type (str): Type of sensor ('humidity', 'temperature', 'gas', 'imu')
            value (float): The sensor reading value
            value_type (str, optional): Type of value for IMU ('acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z')
        """
        # Handle IMU sensor types by mapping them to base 'imu' type
        db_sensor_type = 'imu' if sensor_type.startswith('imu_') else sensor_type
        
        # Get the session maker and model
        session = self.sessions[db_sensor_type]()
        try:
            # Get the model class from the tuple (Base, Model)
            _, model_class = self.models[db_sensor_type]
            
            # Create the appropriate reading object
            if db_sensor_type == 'imu':
                if value_type is None:
                    raise ValueError(f"value_type is required for {sensor_type}")
                reading = model_class(value_type=value_type, value=value)
            else:
                reading = model_class(value=value)
            
            session.add(reading)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving {sensor_type} data: {e}")
            return False
        finally:
            session.close()

    def get_sensor_data(self, sensor_type: str, limit: int = 100):
        # Retrieve sensor readings from appropriate database 
        session = self.sessions[sensor_type]()
        try:
            _, model = self.models[sensor_type]
            readings = session.query(model).order_by(model.timestamp.desc()).limit(limit).all()
            return readings
        finally:
            session.close()