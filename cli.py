# cli.py - part of insp3ctra
import argparse
from sniffer.capture import start_sniffing, export_to_pcap

def main():
    parser = argparse.ArgumentParser(description="Nakshtra Yadav's Packet Sniffer – insp3ctra")

    parser.add_argument('--capture-all', action='store_true', help='Capture all packets (ignore filters)')
    parser.add_argument('--export-pcap', action='store_true', help='Export captured packets to PCAP file')
    parser.add_argument('--iface', type=str, help='Interface to sniff on', default=None)
    parser.add_argument('--count', type=int, help='Number of packets to capture', default=0)
    parser.add_argument('--tcp', action='store_true', help='Capture TCP packets')
    parser.add_argument('--udp', action='store_true', help='Capture UDP packets')
    parser.add_argument('--http', action='store_true', help='Capture HTTP packets')
    parser.add_argument('--dns', action='store_true', help='Capture DNS packets')

    args = parser.parse_args()

    # Decide filter behavior
    if args.capture_all:
        filters = None
    else:
        filters = {
            "tcp": args.tcp,
            "udp": args.udp,
            "http": args.http,
            "dns": args.dns
        }

    start_sniffing(iface=args.iface, count=args.count, filters=filters)

    if args.export_pcap:
        export_to_pcap()

if __name__ == "__main__":
    main()
