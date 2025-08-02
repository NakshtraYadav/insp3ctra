from scapy.layers.inet import IP, TCP

# Keeps track of how many SYN packets each IP sends
syn_counter = {}
THRESHOLD = 50

# Stores the 100 most recent anomaly messages for UI
anomaly_log = []

def record_anomaly_event(msg):
    pass  # Placeholder for metrics or alert hooks (e.g., database, webhook)

def log_anomaly(message):
    print(message)
    anomaly_log.append(message)
    if len(anomaly_log) > 100:
        anomaly_log.pop(0)

def detect_anomaly(packet):
    if packet.haslayer(TCP) and packet[TCP].flags == "S":
        src_ip = packet[IP].src
        syn_counter[src_ip] = syn_counter.get(src_ip, 0) + 1

        syn_count = syn_counter[src_ip]  # ✅ Now defined correctly
        if syn_count > THRESHOLD:
            msg = f"[!] 🚨 Potential SYN flood from {src_ip} – {syn_count} SYN packets"
            log_anomaly(msg)
            record_anomaly_event(msg)
