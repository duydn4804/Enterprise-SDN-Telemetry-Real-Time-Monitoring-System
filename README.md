# Enterprise SDN Telemetry & ChatOps Lab 🚀

## 📌 Project Overview
This project focuses on automating network observability and alerting within a Software-Defined Networking (SDN) infrastructure. By integrating **Python**, **Docker**, and the **Telegram API**, the lab demonstrates a modern **NetDevOps** approach to monitor bandwidth in real-time and automatically alert administrators of network congestion without manual CLI intervention.

## 🖼 Network Topology
<img width="1221" height="759" alt="Topology" src="https://github.com/user-attachments/assets/8ced0685-ffc0-40e5-bbdd-e6c995a3d19e" />

## ✨ Core Features
* **Real-time Telemetry (Python):** Developed Python scripts (`sdn_grafana.py`) interacting with OpenDaylight's REST API to continuously extract port statistics (Tx/Rx bytes) and calculate live bandwidth without impacting network performance.
* **Automated ChatOps Alerting (Python):** Implemented a Telegram bot agent (`sdn_monitor.py`) to automatically detect traffic spikes (>100 Mbps) and push instant alert notifications to administrators.
* **Centralized Dashboard (Docker):** Deployed a containerized observability stack using **Prometheus** (time-series database) and **Grafana** (visualization) to render live traffic charts.

## 🛠 Tech Stack
* **Network & Controller:** Mininet, Open vSwitch (OVS), OpenDaylight (ODL), OpenFlow 1.3.
* **Automation & Scripting:** Python (Requests, Prometheus-client).
* **Observability:** Docker, Docker Compose, Prometheus, Grafana.
* **Alerting:** Telegram Bot API.

## 📂 Project Structure

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
