from scapy.utils import wrpcap
from sniffer.capture import captured_packets
import os

def export_pcap(filename="insp3ctra_capture.pcap"):
    folder = os.path.abspath("data")
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)

    if captured_packets:
        wrpcap(full_path, captured_packets)
        return True, full_path
    return False, "No packets to export."