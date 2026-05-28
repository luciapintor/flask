from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# In-memory storage for received sensor data
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
    with open('database/sensor_data.json', 'a') as f:
        json.dump(sensor_data, f, indent=4)
        
    return jsonify({"status": "ok", "total_records": len(sensor_data)})

@app.route('/sensor/history')
def history():
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True)