"""
FastAPI server implementation for humidity sensor
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import logging
from config.settings import Settings

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Pydantic model for humidity data
class HumidityData(BaseModel):
    humidity: float

class HumidityService:
    def __init__(self, data_buffer, db_service):
        """
        Initialize humidity service
        
        Args:
            data_buffer: DataBuffer instance for storing readings
            db_service: DatabaseService instance for persistence
        """
        self.data_buffer = data_buffer
        self.db_service = db_service
        self.setup_routes()
        
        logger.info("Humidity HTTP service initialized")

    def setup_routes(self):
        """Set up FastAPI routes"""
        
        @app.post("/humidity")
        async def receive_humidity(humidity_data: HumidityData):
            try:
                # Store in buffer
                self.data_buffer.add_data('humidity', humidity_data.humidity)
                
                # Save to database
                self.db_service.save_sensor_data(
                    sensor_type='humidity',
                    value_type='value',
                    value=humidity_data.humidity
                )
                
                logger.debug(f"Received humidity: {humidity_data.humidity}%")
                
                return {
                    "status": "success",
                    "message": f"Humidity received: {humidity_data.humidity}%"
                }
                
            except Exception as e:
                logger.error(f"Error processing humidity data: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Error processing humidity data"
                )

def start_fastapi(data_buffer, db_service):
    """
    Start the FastAPI server
    
    Args:
        data_buffer: DataBuffer instance for storing readings
        db_service: DatabaseService instance for persistence
    """
    humidity_service = HumidityService(data_buffer, db_service)
    
    config = uvicorn.Config(
        app,
        host=Settings.HTTP_HOST,
        port=Settings.HTTP_PORT,
        log_level="info"
    )
    
    server = uvicorn.Server(config)
    server.run()