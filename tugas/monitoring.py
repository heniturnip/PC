import firebase_admin
from firebase_admin import credentials, db
import psutil
import time

# Path to your service account key JSON file
cred = credentials.Certificate("private-key.json")

# Initialize Firebase app
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pc-ho1-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Reference to the 'monitoring_usage' node in Firebase
ref = db.reference('monitoring_usage')

# Function to push CPU data to Firebase
def push_monitoring_data():
    while True:
        # Get current CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)

        # Prepare data with timestamp
        battery = psutil.sensors_battery()
        battery_info = f"{battery.percent}% (Plugged in: {battery.power_plugged})" if battery else "No battery"

        data = {
            "CPU Usage": psutil.cpu_percent(interval=1),
            "Memory Usage": psutil.virtual_memory().percent,
            "Disk Usage": psutil.disk_usage('/').percent,
            "Battery": battery_info,
            "timestamp": time.time()  # Add timestamp for tracking
        }

        # Push data to Firebase
        ref.push(data)

        print(f"Data sent to Firebase: {data}")

        # Send data every 5 seconds
        time.sleep(5)

if __name__ == "__main__":
    push_monitoring_data()