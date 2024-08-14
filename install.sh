#!/bin/bash

# Install Docker if not installed
if ! [ -x "$(command -v docker)" ]; then
  echo "Docker not found, installing..."
  curl -fsSL https://get.docker.com -o get-docker.sh
  sh get-docker.sh
fi

# Install Docker Compose if not installed
if ! [ -x "$(command -v docker-compose)" ]; then
  echo "Docker Compose not found, installing..."
  sudo apt-get install -y docker-compose
fi

# Clone the repository
git clone https://github.com/viperguy07/raspberrypi-noctua-fan-controller.git
cd raspberrypi-noctua-fan-controller

# Set up the Python environment
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Deploy InfluxDB and Grafana using Docker Compose
docker-compose up -d

# Run the fan controller script
python fan_controller.py
