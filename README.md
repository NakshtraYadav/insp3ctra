# 🛡️ insp3ctra: A Modular Packet Sniffer & Web Dashboard

---

## 📌 Overview

- **Name**: `insp3ctra`
- **Type**: Modular Packet Sniffer & Security Toolkit for Windows
- **Users**: Cybersecurity learners, sysadmins, penetration testers, portfolio builders
- **Main Objectives**:
  - Real-time multi-interface packet capture
  - Structured logging (CSV, JSON)
  - PCAP export for offline analysis
  - Dashboard-based control via Flask UI
  - Basic anomaly detection (e.g., SYN flood)
  - Extensible, cross-platform, scriptable



## 🚀 Features

| Feature                         | Purpose                                      | Status        | Tech Stack                        |
|---------------------------------|----------------------------------------------|----------------|------------------------------------|
| Multi-interface sniffing        | Capture traffic on one or more adapters     | ✅ Completed    | Scapy, threading, psutil           |
| Protocol filtering              | Filter by TCP, UDP, DNS, HTTP               | ✅ Completed    | Scapy layers                       |
| CSV + JSON Logging              | Persistent structured logs                   | ✅ Completed    | `csv`, `json`                      |
| PCAP export                     | Offline forensic analysis                   | ✅ Completed    | `wrpcap()`                         |
| Flask Dashboard                 | Web-based control interface                 | ✅ Completed    | Flask, Jinja2                      |
| Clear logs button               | Reset log files easily                      | ✅ Completed    | Flask POST                         |
| Terminal command runner         | Run `ping`, `curl`, etc. via UI             | ✅ Completed    | subprocess                         |
| Interface selector (Choices.js) | UI-enhanced network selector                | ✅ Completed    | JS + psutil                        |
| Anomaly detection (SYN flood)   | Detect flood attacks                        | ✅ Completed    | TCP flags heuristic                |
| Real-time alert streaming       | Show anomalies in UI                        | 🔁 Buggy        | polling `/anomaly_log`             |
| Anomaly log file persistence    | Write alerts to disk                        | ⏳ Planned      | `anomalies.txt` or `json`          |
| ML anomaly detection            | Smarter detection via clustering            | 💤 Optional     | PyOD, scikit-learn                 |
| Packet inspector view           | Expand/collapse packet content              | 💤 Optional     | HTML/JS                            |
| Log Viewer                      | Visual explorer for CSV/JSON logs           | ✅ Completed    | JS + Flask API                     |
| CI/CD integration               | Lint/test on GitHub push                    | ⏳ Planned      | GitHub Actions                     |
| `setup.py` packaging            | Make insp3ctra pip-installable              | ⏳ Planned      | setuptools                         |



## 🧱 Architecture

- **Threaded sniffing**: `threading.Thread` per interface, 1s timeout loops
- **Shared capture flag**: Global dict `sniffing_flag` used for Start/Stop
- **Log rotation**: New `packets2.csv/json` created at 100MB max per file
- **Frontend modularity**: Templates split under `dashboard/templates/components`
- **JS polling**: Dashboard polls `/status` and `/anomaly_log` (optional)
- **Removed complexity**: Realtime charts and GeoIP support were deprecated



## 🧰 Dependencies

- **Language**: Python 3.13
- **Core Libraries**: scapy, Flask, threading, psutil, csv, json, subprocess
- **Frontend**: Choices.js, vanilla JS
- **CI/CD**: GitHub Actions (Planned)
- **Logging**: CSV, JSON, PCAP (binary), console output via `rich.console`



## 📁 Directory Structure

```
insp3ctra/
├── run_dashboard.py            # Entry point for Flask UI
├── main.py                     # Optional CLI
│
├── sniffer/
│   ├── capture.py              # Sniff logic (multi-threaded)
│   ├── anomalies.py            # SYN flood detection + memory buffer
│   ├── filters.py              # Packet filter logic
│   ├── logger.py               # CSV/JSON file logging with rotation
│   └── exporter.py             # Export to PCAP file
│
├── dashboard/
│   ├── app.py                  # Flask routes
│   ├── templates/
│   │   ├── layout.html         # HTML shell
│   │   ├── index.html          # Dashboard page
│   │   ├── log_viewer.html     # Log viewer with filters
│   │   └── components/
│   │       ├── control_buttons.html
│   │       ├── interface_selector.html
│   │       ├── status_panel.html
│   │       └── terminal_block.html
│
├── data/
│   ├── packets.csv             # Rotating logs (CSV)
│   ├── packets.json            # Rotating logs (JSON)
│   └── insp3ctra_capture.pcap  # Exported packets
```



## 🔍 Code Modules

- `capture.py`: Runs sniffing loop and routes packets to log + detect
- `anomalies.py`: Monitors SYN flags, pushes alerts to memory (`anomaly_log`)
- `exporter.py`: Writes PCAP from all captured packets
- `app.py`: Flask web interface, routes for `/start`, `/stop`, `/export_pcap`
- `logger.py`: Rotation-aware logging to `data/` directory



## 🐞 Known Issues

| Issue                                         | Status        |
|----------------------------------------------|---------------|
| Anomaly polling breaks Start/Stop behavior   | 🐞 Known issue |
| Choices.js requires explicit re-init         | 🧩 Solved once |
| `/anomaly_log` only works in-memory          | 📌 Known       |
| PCAP exports no progress for huge captures   | 💤 Optional UX |
| No persistent alert log on disk              | ⏳ Planned     |
| JS `window.onload` conflicts in dashboard    | 🧼 Fixed via layout.html rework |
| No CI/CD or tests yet                        | ⏳ Planned     |



## 🧭 Design Principles

- ✅ Windows 11-friendly (no root required)
- ✅ Modular Python code per concern (capture, detect, log)
- ✅ Clean HTML + inline JS; minimal frameworks
- ✅ Supports CLI or dashboard control
- ✅ Uses `Choices.js` for dropdown enhancement
- ✅ Logging designed to support future JSON ingestion
- 🔧 Developed by [Nakshtra Yadav](https://github.com/NakshtraYadav)



## 🛣️ Roadmap

### Core
- [x] Multi-interface capture
- [x] CSV/JSON log rotation
- [x] Protocol filter (TCP/UDP/HTTP/DNS)
- [x] Dashboard: Start/Stop, Terminal, Log Viewer
- [x] PCAP export

### Upcoming
- [ ] Fix anomaly polling bug without breaking dashboard
- [ ] Add persistent anomaly log file
- [ ] Enable `setup.py` packaging
- [ ] Add CI with GitHub Actions

### Optional
- [ ] ML detection (PyOD)
- [ ] Packet replay from PCAP
- [ ] Toasts/audio on anomalies
- [ ] Log viewer: pagination or export
---

## 📦 Installation

```bash
git clone https://github.com/nakshtrayadav/insp3ctra.git
cd insp3ctra
pip install -r requirements.txt
python run_dashboard.py
```

> Make sure you are on **Windows 10/11** with Python 3.10+ and have appropriate network adapter access.

---

## 🖥️ Usage

- Launch the dashboard: `python run_dashboard.py`
- Access it in your browser: `http://localhost:5000`
- Use the dropdown to select interfaces, then start capture
- Use the built-in terminal, export logs, view alerts and more
