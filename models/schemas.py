"""
Pydantic models for data validation across different sensors
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Base schema for all sensor readings
class ReadingBase(BaseModel):
    value: float
    timestamp: Optional[datetime] = None

# Humidity Schemas
class HumidityReading(ReadingBase):
    value_type: str = "humidity"

class HumidityData(BaseModel):
    humidity: float

# Temperature Schemas
class TemperatureReading(ReadingBase):
    value_type: str = "temperature"

class TemperatureData(BaseModel):
    temperature: float

# Gas Schemas
class GasReading(ReadingBase):
    value_type: str = "gas"

class GasData(BaseModel):
    gas: float

# IMU Schemas
class IMUValue(BaseModel):
    x: float
    y: float
    z: float

class IMUReading(BaseModel):
    accelerometer: IMUValue
    gyroscope: IMUValue
    timestamp: Optional[datetime] = None

# Response Schemas
class SensorResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None