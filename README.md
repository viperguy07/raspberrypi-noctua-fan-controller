# Raspberry Pi Noctua Fan Controller

This project sets up a fan controller for a Raspberry Pi using a Noctua PWM fan. It uses Python scripts to control the fan speed based on the CPU temperature, and stores the fan metrics in InfluxDB. Grafana is used to visualize the data.

## Features
- Automatic fan speed control based on CPU temperature.
- Logs fan RPM, duty cycle, and temperature to InfluxDB.
- Preconfigured Grafana dashboard with gauges for RPM, duty cycle, and temperature.

## Installation

### Prerequisites
- Raspberry Pi running a Linux-based OS.
- Docker and Docker Compose installed.
- Python 3.7+.

### Quick Install

Run the following command to install everything:
```bash
curl -sSL https://raw.githubusercontent.com/viperguy07/raspberrypi-noctua-fan-controller/main/install.sh | bash
