"""
Script to run all sensor senders
"""
import threading
from temperature_sensor import TemperatureSender
from gas_sensor import GasSender
from humidity_sensor import HumiditySender
from imu_sensor import IMUSender
import time

def main():
    # Initialize senders
    temp_sender = TemperatureSender()
    gas_sender = GasSender()
    humidity_sender = HumiditySender()
    imu_sender = IMUSender()


    # Create threads for each sender
    threads = [
        threading.Thread(target=temp_sender.send_data),
        threading.Thread(target=gas_sender.send_data),
        threading.Thread(target=imu_sender.send_data),
        threading.Thread(target=humidity_sender.send_data)
    ]
    
    # Start all threads
    for thread in threads:
        thread.daemon = True
        thread.start()
        
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down sensor senders...")

if __name__ == "__main__":
    main()