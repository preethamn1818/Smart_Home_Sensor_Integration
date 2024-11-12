"""
Main application entry point with real-time visualization
"""
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from services.tcp_service import TCPServer
from services.mqtt_service import IMUClient
from services.http_service import start_fastapi
from utils.data_buffer import DataBuffer
from services.database_service import DatabaseService

class SensorPlotter:
    def __init__(self, data_buffer: DataBuffer):
        self.data_buffer = data_buffer
        self.fig, self.axes = plt.subplots(3, 3, figsize=(15, 10))
        self.fig.canvas.manager.set_window_title('Matplotlib')
        self.fig.suptitle('Real time data visualization')
        
        # Define titles first
        self.titles = ['Humidity', 'Temperature', 'Gas',
                      'Acc X', 'Acc Y', 'Acc Z',
                      'Gyro X', 'Gyro Y', 'Gyro Z']
        
        # Then call setup_plots
        self.setup_plots()
        
        # Store the axis components for each subplot
        self.lines = []
        for ax in self.axes.flat:
            line, = ax.plot([], [])
            self.lines.append(line)
            
    def setup_plots(self):
        for ax, title in zip(self.axes.flat, self.titles):
            ax.set_title(title)
            ax.grid(True)
            
    def extract_component_data(self, data, index):
        try:
            return [d[index] if isinstance(d, (list, tuple)) else d for d in data]
        except (IndexError, TypeError):
            return []
            
    def update(self, frame):
        # Define data sources and their component indices
        data_configs = [
            ('humidity', None),
            ('temperature', None), 
            ('gas', None),        
            ('imu_acc', 0),       # X component
            ('imu_acc', 1),       # Y component
            ('imu_acc', 2),       # Z component
            ('imu_gyro', 0),      # X component
            ('imu_gyro', 1),      # Y component
            ('imu_gyro', 2)       # Z component
        ]
        
        for ax, line, (sensor, component_idx), title in zip(
            self.axes.flat, self.lines, data_configs, self.titles
        ):
            data = self.data_buffer.get_data(sensor)
            
            if data:
                if component_idx is not None:
                    # Extract specific component for IMU data
                    y_data = self.extract_component_data(data, component_idx)
                else:
                    # Use data directly for single-value sensors
                    y_data = data
                    
                if y_data:  # Only update if we have valid data
                    x_data = range(len(y_data))
                    line.set_data(x_data, y_data)
                    
                    # Update axis limits only if needed
                    ax.relim()
                    ax.autoscale_view()
            
            # Ensure grid and title remain
            ax.grid(True)
            ax.set_title(title)
            
        # Adjust layout to prevent overlapping
        self.fig.tight_layout()
        
        return self.lines

def main():
    # Initialize services
    data_buffer = DataBuffer()
    db_service = DatabaseService()
    
    # Initialize visualization
    plotter = SensorPlotter(data_buffer)
    
    # Start TCP servers
    temp_server = TCPServer("temperature", data_buffer, db_service)
    gas_server = TCPServer("gas", data_buffer, db_service)
    
    # Start MQTT client
    imu_client = IMUClient(data_buffer, db_service)
    
    # Create and start threads for services (excluding visualization)
    threads = [
        threading.Thread(target=temp_server.run),
        threading.Thread(target=gas_server.run),
        threading.Thread(target=imu_client.run),
        threading.Thread(target=start_fastapi, args=(data_buffer, db_service))
    ]
    
    # Start all service threads
    for thread in threads:
        thread.daemon = True
        thread.start()
    
    try:
        # Run visualization in main thread
        ani = FuncAnimation(
            plotter.fig,
            plotter.update,
            interval=100,
            cache_frame_data=False,
            save_count=None)
        plt.show()
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    main()