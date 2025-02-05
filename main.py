import subprocess
import time

# Run Flask server
flask_process = subprocess.Popen(["python", "server/app.py"])

# Give Flask some time to start
time.sleep(5)

# Run PyQt UI
ui_process = subprocess.Popen(["python", "ui/ui.py"])

# Keep the main script running
try:
    flask_process.wait()
    ui_process.wait()
except KeyboardInterrupt:
    print("Shutting down...")
    flask_process.terminate()
    ui_process.terminate()
