# Smart Home Monitoring System

A comprehensive IoT solution for monitoring and visualizing data from multiple sensors using different communication protocols. The system handles motion, temperature, humidity, and gas sensors in real-time.

## System Architecture

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐     ┌─────────────┐
│   Sensors   │────>      │  Middleware  │────>    │  Backend   │────>  │ Visualization│
└─────────────┘     └──────────────┘     └────────────┘     └─────────────┘
```

## Features

- Multi-protocol sensor data collection (MQTT, TCP Socket, HTTP)
- Real-time data processing at 100Hz
- Efficient middleware for concurrent sensor handling
- Scalable database storage
- Real-time visualization dashboard

## Prerequisites

- Python 3.8+
- PostgreSQL
- MQTT Broker (Mosquitto)

## Installation


1. Create and activate virtual environment:
```bash
python -m venv env
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```


## Usage

1. Run main:
```bash
python main.py
```

2. Launch sensor emulators:
```bash
cd sensor_emulators
python run_all.py
```

### Sensor Configuration
```yaml
# config/sensors.yaml
motion_sensor:
  protocol: mqtt
  topic: "sensors/imu"
  frequency: 100

temperature_sensor:
  protocol: tcp
  port: 5005
  frequency: 100

humidity_sensor:
  protocol: http
  port: 8000
  frequency: 100


gas/smoke_sensor:
  protocol: tcp
  port: 5010
  frequency: 100

```

 
### Database Configuration
```yaml
host: localhost
port: 5432
user: postgres
```


## Performance Considerations

- The system is designed to handle 100Hz data streams from multiple sensors
- Middleware uses threading operations for optimal performance
- Database indexing optimized for time-series data

## Troubleshooting

Sensor Connection Issues
   - Verify MQTT broker is running
   - Check network connectivity
   - Validate port configurations

