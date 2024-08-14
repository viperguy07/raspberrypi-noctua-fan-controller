import os
import logging
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
import configparser
from datetime import datetime
import time

# Initialize logging with INFO level (or ERROR if you prefer)
logging.basicConfig(level=logging.ERROR)

# Load InfluxDB connection settings from config
config = configparser.ConfigParser()
config.read('config.ini')

# Get the API token from the environment variable
token = os.getenv('INFLUXDB_TOKEN')
if not token:
    raise ValueError("InfluxDB API token not found in environment variables.")

# Connect to InfluxDB 2.x with API token from environment
client = InfluxDBClient(
    url=config['INFLUXDB']['url'],
    token=token,
    org=config['INFLUXDB']['org']
)

# Correctly initialize the write_api with WriteOptions
write_api = client.write_api(write_options=WriteOptions(batch_size=1, flush_interval=1000))

def write_to_influxdb(current_time, current_temp, current_rpm, duty_cycle):
    try:
        point = Point("fan_metrics") \
            .tag("host", "raspberrypi") \
            .field("temperature", int(current_temp)) \
            .field("rpm", int(current_rpm)) \
            .field("duty_cycle", int(duty_cycle)) \
            .time(current_time, WritePrecision.NS)
        
        write_api.write(bucket=config['INFLUXDB']['bucket'], record=point)
        logging.info(f"Data written to InfluxDB: Time={current_time}, Temp={current_temp}, RPM={current_rpm}, Duty Cycle={duty_cycle}")

    except Exception as e:
        logging.error(f"Error writing to InfluxDB: {e}")

# Close the client when done
def close_influxdb_client():
    try:
        write_api.flush()  # Ensure all writes are flushed before closing
        time.sleep(2)  # Delay to ensure all futures complete
    finally:
        client.close()

# Example usage
if __name__ == "__main__":
    # Test data
    current_time = datetime.utcnow()
    current_temp = 45  # Ensure these are integers
    current_rpm = 2569  # Ensure these are integers
    duty_cycle = 169  # Ensure these are integers
    
    # Write test data
    write_to_influxdb(current_time, current_temp, current_rpm, duty_cycle)
    close_influxdb_client()
