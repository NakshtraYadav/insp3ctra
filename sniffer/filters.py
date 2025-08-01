"""
filters.py – Protocol-based filters for insp3ctra
"""
from scapy.layers.inet import TCP, UDP
from scapy.layers.dns import DNS
from scapy.layers.http import HTTP

def apply_filters(packet, filters: dict):
    """Filter packets based on selected protocols"""
    if not filters or not any(filters.values()):
        return True  # No active filters = log all

    if filters.get("tcp") and packet.haslayer(TCP):
        return True
    if filters.get("udp") and packet.haslayer(UDP):
        return True
    if filters.get("dns") and packet.haslayer(DNS):
        return True
    if filters.get("http") and packet.haslayer(HTTP):
        return True

    return False

