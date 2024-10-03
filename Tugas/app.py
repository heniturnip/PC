from flask import Flask, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate("private-key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pc-ho1-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Referensi ke node 'usage_data' di Firebase
usage_ref = db.reference('usage_data')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    usage_snapshot = usage_ref.order_by_key().limit_to_last(10).get()  # Ambil 10 data terakhir
    
    data = []
    for key, value in usage_snapshot.items():
        data.append({
            'cpu': value['cpu'],
            'memory': value['memory'],
            'disk': value['disk'],
            'battery': value['battery'],
            'battery_plugged': value.get('battery_plugged', None),
            'timestamp': value['timestamp']
        })
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
