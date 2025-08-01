"""
logger.py – Logging module for insp3ctra
Logs packets to CSV and JSON formats with rotation.
"""

import json
import csv
import os
from scapy.packet import Packet
from scapy.layers.inet import IP
from scapy.layers.inet6 import IPv6

# Config
DATA_DIR = "data"
MAX_LOG_SIZE_MB = 100
BASE_CSV_NAME = "packets"
BASE_JSON_NAME = "packets"
CSV_FIELDS = ["src", "dst", "proto", "summary"]

def _get_rotated_filename(base_name: str, extension: str) -> str:
    """Return filename like packets.csv / packets2.csv if > 100MB."""
    i = 1
    candidate = os.path.join(DATA_DIR, f"{base_name}.{extension}")
    while os.path.exists(candidate) and os.path.getsize(candidate) >= MAX_LOG_SIZE_MB * 1024 * 1024:
        i += 1
        candidate = os.path.join(DATA_DIR, f"{base_name}{i}.{extension}")
    return candidate

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

    proto = packet[0].name
    summary = packet.summary()

    return {
        "src": src_ip,
        "dst": dst_ip,
        "proto": proto,
        "summary": summary
    }

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

def log_packet(packet: Packet):
    """Main entry point: extract and log a packet with rotation."""
    pkt_info = extract_info(packet)
    if pkt_info:
        write_packet_to_logs(pkt_info)
