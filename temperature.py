
# temperature.py

# Function to get CPU temperature
def get_cpu_temperature():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read().strip()) / 1000.0  # Convert to Celsius
        return temp
    except FileNotFoundError:
        print("CPU temperature file not found.")
        return 0  # Return default value in case of error

# Smoothing the temperature readings
def smooth_temperature(current_temp, last_temp, alpha=0.1):
    return alpha * current_temp + (1 - alpha) * last_temp
