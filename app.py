from flask import Flask, request, jsonify
from datetime import datetime
import json

import matplotlib
matplotlib.use('Agg')  # non-interactive backend, no display needed
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Check if the sensor data file exists, if not create it with an empty list
try:
    with open('database/sensor_data.json', 'r') as f:
        sensor_data = json.load(f)
except FileNotFoundError:
    with open('database/sensor_data.json', 'w') as f:
        json.dump([], f)
    sensor_data = []

@app.route('/')
def home():
    return 'Hello from your PC!'

@app.route('/data')
def get_data():
    # load data from a JSON file and return it as a response
    with open('database/room.json') as f:
        data = json.load(f)

    return jsonify(data)

@app.route('/sensor', methods=['POST'])
def receive():
    payload = request.get_json()
    if payload is None:
        return jsonify({"error": "no JSON received"}), 400
    
    now = datetime.now()
    payload['timestamp'] = request.args.get('timestamp', now.strftime("%Y-%m-%d %H:%M:%S"))
    sensor_data.append(payload)
    print("Received:", payload)
    
    # Store the received data in memory for later retrieval
    with open('database/sensor_data.json', 'w') as f:
        json.dump(sensor_data, f, indent=4)
        
    return jsonify({"status": "ok", "total_records": len(sensor_data)})

@app.route('/sensor/history')
def history():
    return jsonify(sensor_data)

@app.route('/sensor/plot')
def plot():
    if not sensor_data:
        return "No data available yet.", 404

    timestamps = [entry["timestamp"] for entry in sensor_data]
    temperatures = [entry["temp"] for entry in sensor_data]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(timestamps, temperatures, marker='o', color='steelblue', linewidth=2)
    ax.set_title("Temperature over Time")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Temperature (°C)")
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    from flask import send_file
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)