# run_dashboard.py - part of insp3ctra
import webbrowser
import threading
import time
from dashboard.app import app

def open_browser():
    """Open the dashboard in the default web browser after a short delay."""
    time.sleep(1)
    webbrowser.open("http://localhost:5000")

def main():
    print("📡 Starting insp3ctra dashboard...")
    print("🌐 Opening http://localhost:5000 in your browser...")
    print("✅ Press Ctrl+C to stop the server.")

    # Launch browser in a separate thread
    threading.Thread(target=open_browser).start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=5000, use_reloader=False)

if __name__ == "__main__":
    main()
