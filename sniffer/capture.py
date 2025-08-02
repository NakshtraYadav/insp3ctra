import os
import threading
from scapy.all import sniff, get_if_list
from scapy.utils import wrpcap
from sniffer.anomalies import detect_anomaly
from sniffer.logger import log_packet, extract_info
from sniffer.filters import apply_filters
from rich.console import Console

sniffing_flag = {"active": True}
console = Console()
captured_packets = []

<<<<<<< HEAD
def packet_handler(packet, filters, iface_name):
=======
def packet_handler(packet, filters):
>>>>>>> 188f5349327b4bfbaa7beda3029d6fa2b9e7c9d9
    if apply_filters(packet, filters):
        log_packet(packet)
        detect_anomaly(packet)
        captured_packets.append(packet)
        info = extract_info(packet)
        console.print(
<<<<<<< HEAD
            f"[green]Captured:[/] {info['src']} → {info['dst']} :: {info['proto']} on [bold cyan]{iface_name}[/]"
=======
            f"[green]Captured:[/] {info['src']} → {info['dst']} :: {info['proto']}"
>>>>>>> 188f5349327b4bfbaa7beda3029d6fa2b9e7c9d9
        )

def sniff_on_interface(iface, filters, count): 
    try:
        console.print(f"[cyan]Sniffing on:[/] {iface}")
        packet_limit = count if count > 0 else float("inf")
        captured = 0
        while sniffing_flag["active"] and captured < packet_limit:
            sniffed = sniff(
                iface=iface,
<<<<<<< HEAD
                prn=lambda pkt: packet_handler(pkt, filters, iface),
=======
                prn=lambda pkt: packet_handler(pkt, filters),
>>>>>>> 188f5349327b4bfbaa7beda3029d6fa2b9e7c9d9
                store=False,
                timeout=1
            )
            captured += len(sniffed)
    except PermissionError:
        console.print(f"[red]Permission denied on {iface}[/]")
    except Exception as e:
        console.print(f"[red]Error on {iface}: {e}[/]")

def start_sniffing(interfaces=None, count=0, filters=None):
    if interfaces:
        console.print(f"[blue]Sniffing on interfaces: {', '.join(interfaces)}[/]")
        threads = []
        for iface in interfaces:
            t = threading.Thread(target=sniff_on_interface, args=(iface, filters, count), daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    else:
        console.print("[blue]insp3ctra sniffing on ALL interfaces...[/]")
        threads = []
        for i in get_if_list():
            t = threading.Thread(target=sniff_on_interface, args=(i, filters, count), daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

def export_to_pcap(filename="data/insp3ctra_capture.pcap"):
    if captured_packets:
        os.makedirs("data", exist_ok=True)
        wrpcap(filename, captured_packets)
        console.print(f"[yellow]Exported {len(captured_packets)} packets to {filename}[/]")
    else:
        console.print("[red]No packets captured to export[/]")

def stop_sniffing():
    sniffing_flag["active"] = False

def reset_sniffing_flag():
    sniffing_flag["active"] = True
