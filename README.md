# insp3ctra

**Modular Packet Sniffer and Web Dashboard for Windows, built by [Nakshtra Yadav](https://www.linkedin.com/in/nakshtrayadav/)**

---

## Overview

insp3ctra is a modular and extensible packet sniffing toolkit built for Windows environments, designed with a focus on real-world usability, security analysis, and portfolio-ready software engineering. It provides both a CLI and a Flask-powered web dashboard interface for real-time network monitoring, logging, and control.

Key objectives:
- Multi-interface packet capture (Wi-Fi, Ethernet, etc.)
- Protocol-based filtering (TCP, UDP, DNS, HTTP)
- Structured CSV and JSON logging with rotation
- PCAP export for forensic analysis in Wireshark
- Live web-based control dashboard
- Built-in anomaly detection (SYN flood)
- Terminal command execution via browser
- Easily deployable as a Windows executable

---

## Core Features

| Feature                        | Description                                                   | Status       |
|-------------------------------|---------------------------------------------------------------|--------------|
| Multi-interface sniffing      | Capture packets from one or more adapters                    | Complete     |
| Protocol filtering            | TCP, UDP, DNS, HTTP filtering using Scapy                    | Complete     |
| Log rotation                  | Auto-rollover at 100MB to new CSV/JSON files                 | Complete     |
| PCAP export                   | Export captured packets to .pcap for use in Wireshark        | Complete     |
| Flask web dashboard           | Start/Stop capture, view logs, control terminal              | Complete     |
| Web-based terminal            | Run any system command from dashboard                        | Complete     |
| SYN flood detection           | Flags flood attempts using TCP flag heuristics               | Complete     |
| Interface selector UI         | Built with Choices.js, detects available adapters            | Complete     |
| Log viewer                    | In-browser filterable view for CSV/JSON logs                 | Complete     |
| Real-time anomaly alerting    | Display anomaly buffer in dashboard                          | Buggy        |
| Persistent anomaly logging    | Save anomalies to file (planned)                             | Planned      |
| setup.py packaging            | Installable via pip (planned)                                | Planned      |
| CI/CD with GitHub Actions     | Automated testing and deployment (planned)                   | Planned      |
| ML-based anomaly detection    | Optional PyOD/scikit-learn integration                       | Planned      |
| Packet replay                 | Optional replay from PCAP into dashboard                     | Planned     |

---

## Architecture

- Multi-threaded sniffing using `threading.Thread`
- Modular folder structure separating CLI, sniffer logic, dashboard, and templates
- Logs written in rotating format under `data/`
- Web interface built with Flask and vanilla JS, using Choices.js for modern UI
- PyInstaller-compatible execution with self-contained `.exe` build

---

## Technology Stack

- Language: Python 3.13
- Network engine: Scapy
- Web backend: Flask
- Frontend: HTML/CSS + Choices.js + Vanilla JS
- Logging: CSV, JSON, PCAP, rich console
- Packaging: PyInstaller for Windows executables
- Deployment target: Windows 10/11, no root required

---

## Protocol & OSI Layer Support

insp3ctra captures and analyzes packets across multiple OSI layers:

- **Layer 2 – Data Link:** Captures packets from live interfaces via Npcap  
- **Layer 3 – Network:** Inspects IP headers (IPv4/IPv6)  
- **Layer 4 – Transport:** Parses TCP/UDP protocols, flags, ports  
- **Layer 7 – Application (lightweight):** Recognizes basic HTTP and DNS patterns for logging/anomaly detection

This tool does not perform deep application-layer decoding (e.g., TLS decryption or full HTTP reconstruction), but can be extended for protocol-specific analysis.**

---

## Directory Structure

```
insp3ctra/
├── run_dashboard.py            # Entry point for Flask UI (EXE-compatible)
├── main.py                     # Optional CLI runner
│
├── sniffer/
│   ├── capture.py              # Packet capture and dispatch
│   ├── anomalies.py            # SYN flood detection
│   ├── filters.py              # Protocol filtering logic
│   ├── logger.py               # Logging to CSV/JSON with rotation
│   └── exporter.py             # PCAP export handler
│
├── dashboard/
│   ├── app.py                  # Flask routes and logic
│   ├── templates/              # HTML templates and components
│   
│
├── data/                       # Logs (created at runtime)
│   ├── packets.csv
│   ├── packets.json
│   └── insp3ctra_capture.pcap
```

---

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/NakshtraYadav/insp3ctra.git
   cd insp3ctra
   pip install -r requirements.txt
   ```

2. Launch the dashboard:
   ```bash
   python run_dashboard.py
   ```

3. Open your browser at:
   ```
   http://localhost:5000
   ```

4. Select one or more interfaces, start capture, use terminal, view logs, and export PCAP.

---

## Executable Build (Optional)

insp3ctra can be built into a portable `.exe` with PyInstaller:

```bash
pip install pyinstaller
pyinstaller run_dashboard.py --onefile --console --name insp3ctra
```

This will create a standalone Windows executable in the `dist/` directory. It opens a terminal, runs the dashboard server, and saves logs in a `data/` folder.

---

## Credits

Developed and maintained by **Nakshtra Yadav**  
[LinkedIn Profile](https://www.linkedin.com/in/nakshtrayadav/)  
[GitHub](https://github.com/NakshtraYadav)

---

## Project Screenshots
<img width="902" height="893" alt="image" src="https://github.com/user-attachments/assets/1d2c3d5b-f1f0-41a8-8dbb-123411c37f02" />


