#!/usr/bin/env python3
import time
import pigpio
from datetime import datetime
from temperature import get_cpu_temperature, smooth_temperature
from pid_controller import adjust_fan_speed
from influxdb_writer import write_to_influxdb, close_influxdb_client

# Load constants from configuration
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

PWM_FREQ = int(config['FAN']['PWM_FREQ'])
MAX_DUTY_CYCLE = int(config['FAN']['MAX_DUTY_CYCLE'])
CRITICAL_TEMP = int(config['TEMPERATURE']['CRITICAL_TEMP'])

FAN_PIN = 18  # GPIO pin for PWM fan control
RPM_PIN = 24  # GPIO pin for RPM signal

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpio daemon.")
    exit(1)

# Setup RPM measurement
pulse_count = 0
def rpm_callback(gpio, level, tick):
    global pulse_count
    pulse_count += 1

# Register callback for RPM signal
cb = pi.callback(RPM_PIN, pigpio.RISING_EDGE, rpm_callback)

# Main control loop
current_duty_cycle = 70  # Start somewhere in the middle
last_temp = get_cpu_temperature()
try:
    while True:
        # Wait for 1 second to count pulses and then calculate RPM
        time.sleep(1)
        current_rpm = (pulse_count / 2) * 60
        pulse_count = 0  # Reset pulse count for the next interval

        current_temp = get_cpu_temperature()
        smoothed_temp = smooth_temperature(current_temp, last_temp)
        last_temp = smoothed_temp  # Update the last temperature

        if smoothed_temp < 45:
            # Turn off the fan if the temperature is below 45°C
            current_duty_cycle = 0
            pi.set_PWM_dutycycle(FAN_PIN, 0)
            target_rpm = 0
        elif smoothed_temp >= 70:
            # Max out fan speed if temperature is 70°C or higher
            current_duty_cycle = MAX_DUTY_CYCLE
            pi.set_PWM_dutycycle(FAN_PIN, MAX_DUTY_CYCLE)
            target_rpm = 5000  # Assuming max RPM corresponds to max duty cycle
        else:
            # Map temperature to target RPM for temperatures between 45°C and 69°C
            target_rpm = max(1500, min(5000, 1500 + (smoothed_temp - 45) * (3500 / 24)))

            # Adjust fan speed using PID control
            current_duty_cycle = adjust_fan_speed(current_rpm, target_rpm, current_duty_cycle)

            # Set PWM duty cycle for fan control
            pi.set_PWM_frequency(FAN_PIN, PWM_FREQ)
            pi.set_PWM_dutycycle(FAN_PIN, int(current_duty_cycle))

        # Safety cut-off at critical temperature
        if current_temp >= CRITICAL_TEMP:
            pi.set_PWM_dutycycle(FAN_PIN, MAX_DUTY_CYCLE)  # Max out fan speed
            print("Critical temperature! Maxing out fan speed.")

        # Log the data to InfluxDB
        current_time = datetime.utcnow()
        write_to_influxdb(current_time, current_temp, current_rpm, current_duty_cycle)

        # Output for debugging and monitoring
        print(f"{current_time} - Temp: {int(current_temp)}°C, Smoothed Temp: {int(smoothed_temp)}°C, Target RPM: {target_rpm if target_rpm else 'OFF'}, Current RPM: {int(current_rpm)}, Duty Cycle: {int(current_duty_cycle)}")

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Clean up
    pi.set_PWM_dutycycle(FAN_PIN, 0)
    cb.cancel()
    pi.stop()
    close_influxdb_client()
