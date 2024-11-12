"""
SQLAlchemy models for different sensor databases
"""
from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Create separate base classes for each database
HumidityBase = declarative_base()
TemperatureBase = declarative_base()
GasBase = declarative_base()
IMUBase = declarative_base()

class HumidityReading(HumidityBase):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class TemperatureReading(TemperatureBase):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class GasReading(GasBase):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class IMUReading(IMUBase):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, index=True)
    value_type = Column(String)  # 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z'
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)