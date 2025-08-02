from flask import Flask, jsonify, render_template, request
from threading import Thread
from sniffer.capture import start_sniffing, stop_sniffing, reset_sniffing_flag
import subprocess
import os
import psutil
import csv
import json
from flask import send_file
from sniffer.exporter import export_pcap
from sniffer.anomalies import anomaly_log

app = Flask(__name__)
sniff_thread = None
sniffing = False
selected_interfaces = []

filters = {
    "tcp": True,
    "udp": True,
    "dns": True,
    "http": True
}

def sniff_runner():
    global sniffing
    sniffing = True
    try:
        if selected_interfaces:
            start_sniffing(interfaces=selected_interfaces, filters=filters)
        else:
            start_sniffing(filters=filters)
    finally:
        sniffing = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_capture():
    global sniff_thread, sniffing, selected_interfaces
    if not sniffing:
        reset_sniffing_flag()
        data = request.get_json()
        selected_interfaces = data.get("interfaces", [])
        sniff_thread = Thread(target=sniff_runner, daemon=True)
        sniff_thread.start()
        return jsonify({"status": "started", "interfaces": selected_interfaces})
    else:
        return jsonify({"status": "already running"})

@app.route("/stop", methods=["POST"])
def stop_capture():
    global sniffing
    if sniffing:
        stop_sniffing()
        return jsonify({"status": "stopping"})
    return jsonify({"status": "not running"})

@app.route("/status")
def get_status():
    return jsonify({"sniffing": sniffing})

@app.route("/clear_logs", methods=["POST"])
def clear_logs():
    try:
        open("data/packets.json", "w").close()
        open("data/packets.csv", "w").close()
        return jsonify({"status": "cleared"})
    except Exception as e:
        return jsonify({"status": f"error: {str(e)}"})

@app.route("/run_command", methods=["POST"])
def run_command():
<<<<<<< HEAD
    cmd = request.json.get("command", "").strip()

    if not cmd:
        return jsonify({"output": "❌ No command provided", "error": True})

    try:
        # 🛡️ VERY LIGHT SANITIZATION (optional: expand later if needed)
        if any(bad in cmd.lower() for bad in ["rm ", "del ", ":>", "shutdown", "format", "mkfs", "reg delete"]):
            return jsonify({"output": "❌ Dangerous command blocked", "error": True})

        result = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT,
            shell=True, timeout=15,
            universal_newlines=True,
            encoding="utf-8"
        )
        return jsonify({"output": result, "error": False})
    except subprocess.TimeoutExpired:
        return jsonify({"output": f"⏳ Command '{cmd}' timed out after 15s", "error": True})
    except subprocess.CalledProcessError as e:
        return jsonify({"output": e.output or str(e), "error": True})
    except Exception as e:
        return jsonify({"output": f"🔥 {str(e)}", "error": True})

=======
    cmd = request.json.get("command", "")
    try:
        allowed_cmds = ["ping", "nslookup", "curl", "tracert", "whois"]
        if not any(cmd.startswith(a) for a in allowed_cmds):
            return jsonify({"output": "❌ Command not allowed", "error": True})

        if cmd.startswith("ping") and "-n" not in cmd:
            cmd += " -n 1"

        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, timeout=10, universal_newlines=True)
        return jsonify({"output": result, "error": False})
    except subprocess.TimeoutExpired:
        return jsonify({"output": f"❌ Command '{cmd}' timed out after 10 seconds", "error": True})
    except subprocess.CalledProcessError as e:
        return jsonify({"output": e.output, "error": True})
    except Exception as e:
        return jsonify({"output": str(e), "error": True})
>>>>>>> 188f5349327b4bfbaa7beda3029d6fa2b9e7c9d9

@app.route("/interfaces")
def get_interfaces():
    interfaces = []
    for name, addrs in psutil.net_if_addrs().items():
        label = name
        for addr in addrs:
            if addr.family.name == 'AF_LINK':
                label += " (MAC: " + addr.address + ")"
            elif addr.family.name.startswith("AF_INET"):
                label += " / " + addr.address
        interfaces.append({"value": name, "label": label})
    return jsonify({"interfaces": interfaces})

@app.route("/log_viewer")
def log_viewer():
    return render_template("log_viewer.html")

@app.route("/get_log_data")
def get_log_data():
    log_type = request.args.get("type", "csv")
    data = []

    try:
        path = "data/packets.csv" if log_type == "csv" else "data/packets.json"
        with open(path, "r", encoding="utf-8") as f:
            if log_type == "csv":
                reader = csv.DictReader(f)
                data = [row for row in reader]
            else:
                data = [json.loads(line) for line in f if line.strip()]
    except Exception as e:
        print("Error loading log:", e)

    return jsonify(data)

@app.route("/export_pcap", methods=["GET"])
def download_pcap():
    success, result = export_pcap()
    if success and os.path.isfile(result):
        return send_file(result, as_attachment=True)
    return {"error": "❌ No packets captured or file not created"}, 404

@app.route("/anomaly_log")
def get_anomalies():
    return {"log": anomaly_log}