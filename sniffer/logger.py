"""
logger.py – Logging module for insp3ctra
Logs packets to CSV and JSON formats with rotation.
"""

import json
import csv
import os
<<<<<<< HEAD
import sys
=======
>>>>>>> 188f5349327b4bfbaa7beda3029d6fa2b9e7c9d9
from scapy.packet import Packet
from scapy.layers.inet import IP
from scapy.layers.inet6 import IPv6

<<<<<<< HEAD
# ========== 🧠 Runtime-safe data directory resolution ==========
def get_base_path():
    """Handle both PyInstaller .exe and normal Python execution"""
    if getattr(sys, 'frozen', False):
        # Running in a bundle (PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # Running in normal Python
        return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()
DATA_DIR = os.path.join(BASE_PATH, "data")  # Always create alongside script or .exe

# ========== 🗃️ Logging config ==========
=======
# Config
DATA_DIR = "data"
>>>>>>> 188f5349327b4bfbaa7beda3029d6fa2b9e7c9d9
MAX_LOG_SIZE_MB = 100
BASE_CSV_NAME = "packets"
BASE_JSON_NAME = "packets"
CSV_FIELDS = ["src", "dst", "proto", "summary"]

<<<<<<< HEAD
# ========== 🔄 Rotation-safe file naming ==========
=======
>>>>>>> 188f5349327b4bfbaa7beda3029d6fa2b9e7c9d9
def _get_rotated_filename(base_name: str, extension: str) -> str:
    """Return filename like packets.csv / packets2.csv if > 100MB."""
    i = 1
    candidate = os.path.join(DATA_DIR, f"{base_name}.{extension}")
    while os.path.exists(candidate) and os.path.getsize(candidate) >= MAX_LOG_SIZE_MB * 1024 * 1024:
        i += 1
        candidate = os.path.join(DATA_DIR, f"{base_name}{i}.{extension}")
    return candidate

<<<<<<< HEAD
# ========== 🧠 Packet information extractor ==========
=======
>>>>>>> 188f5349327b4bfbaa7beda3029d6fa2b9e7c9d9
def extract_info(packet: Packet) -> dict:
    """Extract IP addresses and protocol summary."""
    src_ip, dst_ip = "N/A", "N/A"

    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
    elif IPv6 in packet:
        src_ip = packet[IPv6].src
        dst_ip = packet[IPv6].dst
    elif hasattr(packet, 'src') and hasattr(packet, 'dst'):
        src_ip = packet.src
        dst_ip = packet.dst
    elif hasattr(packet[0], 'src') and hasattr(packet[0], 'dst'):
        src_ip = packet[0].src
        dst_ip = packet[0].dst

<<<<<<< HEAD
    if packet.haslayer("TCP"):
        proto = "TCP"
    elif packet.haslayer("UDP"):
        proto = "UDP"
    elif packet.haslayer("DNS"):
        proto = "DNS"
    elif packet.haslayer("HTTP"):
        proto = "HTTP"
    elif packet.haslayer("ICMP"):
        proto = "ICMP"
    else:
        proto = packet[0].name  # fallback (e.g. Ethernet)

=======
    proto = packet[0].name
>>>>>>> 188f5349327b4bfbaa7beda3029d6fa2b9e7c9d9
    summary = packet.summary()

    return {
        "src": src_ip,
        "dst": dst_ip,
        "proto": proto,
        "summary": summary
    }

<<<<<<< HEAD
# ========== 📦 Write to disk ==========
=======
>>>>>>> 188f5349327b4bfbaa7beda3029d6fa2b9e7c9d9
def write_packet_to_logs(packet_data: dict):
    """Write a single packet to rotated CSV and JSON logs."""
    os.makedirs(DATA_DIR, exist_ok=True)

    # JSON
    json_file = _get_rotated_filename(BASE_JSON_NAME, "json")
    with open(json_file, "a", encoding="utf-8") as jf:
        jf.write(json.dumps(packet_data) + "\n")

    # CSV
    csv_file = _get_rotated_filename(BASE_CSV_NAME, "csv")
    file_exists = os.path.exists(csv_file)
    with open(csv_file, "a", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=CSV_FIELDS, extrasaction='ignore')
        if not file_exists or os.path.getsize(csv_file) == 0:
            writer.writeheader()
        writer.writerow(packet_data)

<<<<<<< HEAD
# ========== 📍 Entry Point ==========
=======
>>>>>>> 188f5349327b4bfbaa7beda3029d6fa2b9e7c9d9
def log_packet(packet: Packet):
    """Main entry point: extract and log a packet with rotation."""
    pkt_info = extract_info(packet)
    if pkt_info:
        write_packet_to_logs(pkt_info)
