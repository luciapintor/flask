# Flask Demo — Local HTTP Server

A minimal Flask application that demonstrates how to use your PC as a local HTTP server. 

## Project Structure

```
flask_demo/
├── app.py
└── readme.md
└── requirements.txt
└── database
    └── room.json
    └── sensor_data.json
```

## Setup

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Run the server**

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000`.

---

## Endpoints

### `GET /`
Basic health check. Confirms the server is running.

```bash
curl http://127.0.0.1:5000/
```

### `GET /data`
Returns a static JSON payload simulating a sensor reading.

```bash
curl http://127.0.0.1:5000/data
```

Response:
```json
{
    "time": "09:00",
    "artwork": "Mona Lisa",
    "visitors": 45,
    "selfies": 18,
    "posts": 10,
    "avg_likes": 120
  },
  ...
```

### `POST /sensor`
Receives a JSON payload from a client or simulated sensor. Stores it in memory and returns a confirmation with the total number of records received.

**Linux/Mac:**
```bash
curl -X POST http://127.0.0.1:5000/sensor \
  -H "Content-Type: application/json" \
  -d '{"temp": 22.5}'
```

**Windows Command Prompt:**
```cmd
curl -X POST http://127.0.0.1:5000/sensor -H "Content-Type: application/json" -d "{\"temp\": 22.5}"
```

**Python (any OS):**
```python
import requests
response = requests.post("http://127.0.0.1:5000/sensor", json={"temp": 22.5})
print(response.json())
```

Response:
```json
{"status": "ok", "total_records": 1}
```

### `GET /sensor/history`
Returns all data received with POST requests.

```bash
curl http://127.0.0.1:5000/sensor/history
```

Response:
```json
[{"timestamp": "2026-07-18 09:00:00", "temp": 22.5}]
```
 
### `GET /sensor/plot`
Returns a PNG chart of temperature over time, rendered from all data received in the current session. Open directly in the browser.
 
```
http://127.0.0.1:5000/sensor/plot
```
 
Returns a `404` with a plain text message if no data has been posted yet.
 
> Data is stored in memory and resets every time the server restarts.
 
---
 
## Requirements
 
- Python 3.7+
- Flask
- Matplotlib