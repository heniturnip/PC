import firebase_admin
from firebase_admin import credentials, db
import psutil
import time

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate("private-key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pc-ho1-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Referensi ke root node di Firebase
usage_ref = db.reference('usage_data')

# Fungsi untuk mengirim data ke Firebase
def push_data():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else None
        battery_plugged = battery.power_plugged if battery else None

        timestamp = time.time()

        # Gabungkan semua data dalam satu node dengan timestamp
        usage_data = {
            'cpu': cpu_percent,
            'memory': memory_percent,
            'disk': disk_percent,
            'battery': battery_percent,
            'battery_plugged': battery_plugged,
            'timestamp': timestamp
        }

        # Push ke node 'usage_data' di Firebase
        usage_ref.push(usage_data)

        print(f"Data pushed: CPU={cpu_percent}, Memory={memory_percent}, Disk={disk_percent}, Battery={battery_percent}")
        time.sleep(30)  # Mengirim data setiap 1 menit

if __name__ == "__main__":
    push_data()