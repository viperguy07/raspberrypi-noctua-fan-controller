
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
curl  -sSL  https://raw.githubusercontent.com/viperguy07/raspberrypi-noctua-fan-controller/main/install.sh | bash
```
### Manual  Install
1. Clone  the  repository:
```bash
git  clone  https://github.com/viperguy07/raspberrypi-noctua-fan-controller.git
cd  raspberrypi-noctua-fan-controller
```
2. Set  up  the  Python  environment:
```bash
python3  -m  venv  env
source  env/bin/activate
pip  install  -r  requirements.txt
```
3. Deploy  InfluxDB  and  Grafana  using  Docker  Compose:

```bash
docker-compose  up  -d
```
4. Run  the  fan  controller  script:
```bash
python  fan_controller.py
```
### Configuration
Edit  the  config.ini  file  to  change  the  InfluxDB  settings  or  fan  control  parameters.

### Ansible  Deployment

You  can  deploy  the  entire  setup  using  Ansible  by  running:
```bash
ansible-playbook  playbook.yml
```
This  playbook  installs  InfluxDB,  Grafana,  and  the  fan  controller  script,  and  sets  up  the  necessary  configurations.

### License
This  project  is  licensed  under  the  MIT  License.
