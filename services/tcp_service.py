"""
TCP server implementation for temperature and gas sensors
"""
import socket
from struct import unpack
import time
from config.settings import Settings
import logging

logger = logging.getLogger(__name__)

class TCPServer:
    def __init__(self, sensor_type: str, data_buffer, db_service):
        """
        Initialize TCP server for a specific sensor type
        
        Args:
            sensor_type (str): Either "temperature" or "gas"
            data_buffer: DataBuffer instance for storing readings
            db_service: DatabaseService instance for persistence
        """
        self.sensor_type = sensor_type
        self.data_buffer = data_buffer
        self.db_service = db_service
        self.running = True
        
        # Set up TCP socket
        self.port = (Settings.TEMPERATURE_PORT if sensor_type == "temperature" 
                    else Settings.GAS_PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((Settings.TCP_HOST, self.port))
        self.sock.listen(1)
        self.sock.setblocking(False)
        
        self.connections = []
        self.partial_data = {}
        
        logger.info(f"TCP Server initialized for {sensor_type} on port {self.port}")

    def handle_new_connection(self):
        """Accept and set up new connections"""
        try:
            conn, addr = self.sock.accept()
            logger.info(f"New {self.sensor_type} connection from {addr}")
            conn.setblocking(False)
            self.connections.append(conn)
            self.partial_data[conn] = b""
        except BlockingIOError:
            pass
        except Exception as e:
            logger.error(f"Error accepting connection: {e}")

    def process_data(self, data: bytes) -> bool:
        """
        Process received sensor data
        
        Args:
            data (bytes): 4 bytes representing a float value
        """
        try:
            value = unpack("f", data)[0]
            
            # Store in buffer
            self.data_buffer.add_data(self.sensor_type, value)
            
            # Save to database
            self.db_service.save_sensor_data(
                sensor_type=self.sensor_type,
                value_type="value",
                value=value
            )
            
            logger.debug(f"Received {self.sensor_type} value: {value}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing {self.sensor_type} data: {e}")
            return False

    def run(self):
        """Main server loop"""
        logger.info(f"Starting {self.sensor_type} TCP server")
        
        while self.running:
            try:
                self.handle_new_connection()
                
                # Check all existing connections
                for conn in self.connections[:]:
                    try:
                        data = conn.recv(4)  # Expecting 4 bytes for float
                        if data:
                            self.process_data(data)
                        else:
                            # Connection closed by client
                            self.connections.remove(conn)
                            conn.close()
                            logger.info(f"{self.sensor_type} connection closed")
                            
                    except BlockingIOError:
                        continue
                    except Exception as e:
                        logger.error(f"Error handling connection: {e}")
                        self.connections.remove(conn)
                        conn.close()
                        
            except Exception as e:
                logger.error(f"Error in main server loop: {e}")
                
            time.sleep(0.01)  # Prevent CPU overload