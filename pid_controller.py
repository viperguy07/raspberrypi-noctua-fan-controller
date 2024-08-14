
# pid_controller.py
import time
import configparser

# Load PID constants from configuration
config = configparser.ConfigParser()
config.read('config.ini')
Kp = float(config['PID']['Kp'])
Ki = float(config['PID']['Ki'])
Kd = float(config['PID']['Kd'])
MAX_DUTY_CYCLE = int(config['FAN']['MAX_DUTY_CYCLE'])

# Initialize control variables
integral = 0
last_error = 0
last_time = None

def adjust_fan_speed(current_rpm, target_rpm, last_duty_cycle):
    global integral, last_error, last_time

    if target_rpm is None:  # If temperature is 70°C or higher
        return MAX_DUTY_CYCLE

    if last_time is None:
        last_time = time.time()

    error = target_rpm - current_rpm
    current_time = time.time()
    delta_time = current_time - last_time
    delta_error = error - last_error

    # Proportional term
    proportional = Kp * error

    # Integral term with anti-windup
    integral += Ki * error * delta_time
    if integral > MAX_DUTY_CYCLE:
        integral = MAX_DUTY_CYCLE
    elif integral < 0:
        integral = 0

    # Derivative term
    derivative = Kd * delta_error / delta_time

    # Compute new duty cycle
    duty_cycle_change = proportional + integral + derivative
    new_duty_cycle = last_duty_cycle + duty_cycle_change
    new_duty_cycle = max(0, min(MAX_DUTY_CYCLE, new_duty_cycle))  # Ensure within bounds

    # Update control variables
    last_error = error
    last_time = current_time

    return new_duty_cycle
