# Enterprise SDN Telemetry & ChatOps Lab 

## Project Overview
This project focuses on automating network observability and alerting within a Software-Defined Networking (SDN) infrastructure. By integrating **Python**, **Docker**, and the **Telegram API**, the lab demonstrates a modern **NetDevOps** approach to monitor bandwidth in real-time and automatically alert administrators of network congestion without manual CLI intervention.

## Network Topology
<img width="1221" height="759" alt="Topology" src="https://github.com/user-attachments/assets/8ced0685-ffc0-40e5-bbdd-e6c995a3d19e" />

## Core Features
* **Real-time Telemetry (Python):** Developed Python scripts (`sdn_grafana.py`) interacting with OpenDaylight's REST API to continuously extract port statistics (Tx/Rx bytes) and calculate live bandwidth without impacting network performance.
* **Automated ChatOps Alerting (Python):** Implemented a Telegram bot agent (`sdn_monitor.py`) to automatically detect traffic spikes (>100 Mbps) and push instant alert notifications to administrators.
* **Centralized Dashboard (Docker):** Deployed a containerized observability stack using **Prometheus** (time-series database) and **Grafana** (visualization) to render live traffic charts.

## Tech Stack
* **Network & Controller:** Mininet, Open vSwitch (OVS), OpenDaylight (ODL), OpenFlow 1.3.
* **Automation & Scripting:** Python (Requests, Prometheus-client).
* **Observability:** Docker, Docker Compose, Prometheus, Grafana.
* **Alerting:** Telegram Bot API.

## Project Structure

```text
├── Topology/           # Network diagram
│   └── Topology.png
├── mininet/            # Infrastructure configuration
│   └── topology.py     # Mininet custom 3-tier topology
├── monitoring/         # Dockerized observability stack
│   ├── docker-compose.yml
│   └── prometheus.yml
├── python/             # Python automation agents
│   ├── sdn_grafana.py  # Push metrics to Prometheus
│   └── sdn_monitor.py  # Telegram alert agent
└── README.md           # Project documentation

Quick Start
1. Clone the repository:
git clone [https://github.com/duydn4804/Enterprise-SDN-Telemetry-Real-Time-Monitoring-System](https://github.com/duydn4804/Enterprise-SDN-Telemetry-Real-Time-Monitoring-System)
cd SDN-Telemetry-ChatOps-Lab

2. Provision the SDN Controller & Network: (Ensure OpenDaylight Controller is running locally on port 8181 before starting the topology)
sudo python3 mininet/topology.py

3. Deploy the Observability Stack (Prometheus & Grafana):
cd monitoring
docker-compose up -d

4. Run Python Telemetry Agent (Push data to Grafana):
pip install requests prometheus-client
python3 python/sdn_grafana.py

5. Run ChatOps Alert Agent (Telegram Bot):
python3 python/sdn_monitor.py
