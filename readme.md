# Flask Demo — Local HTTP Server

A minimal Flask application that demonstrates how to use your PC as a local HTTP server. 

# How HTTP works (quick intro)
When your browser opens a webpage, it sends a request to a server and receives a response. This exchange follows a protocol called HTTP.
Every request has a method that describes the intention:

- GET asks the server to return some data. It is the default method used by browsers when you type a URL.
- POST sends data to the server, for example the reading from a sensor.

The server processes the request and replies with a status code and, usually, some content. Common codes: 200 means success, 404 means the requested resource was not found.
In this project, your PC acts as the server. The address http://127.0.0.1:5000 refers to your own machine: 127.0.0.1 is a standard address that always points to the local computer (also called localhost), and 5000 is the port Flask uses by default.

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

This command will show you the following text "Hello from your PC!". 

You can obtain the same result by copying the link [http://127.0.0.1:5000/](http://127.0.0.1:5000/) on your browser.

### `GET /data`
Returns a static JSON payload simulating a sensor reading.

```bash
curl http://127.0.0.1:5000/data
```

This command will show you the following response:
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

The full response is a JSON array. Above is an excerpt of the first element.

You can obtain the same result by copying the link [http://127.0.0.1:5000/data](http://127.0.0.1:5000/data) on your browser.

### `POST /sensor`
Receives a JSON payload from a client or simulated sensor. Stores it in memory and returns a confirmation with the total number of records received.


**Windows Command Prompt:**
```cmd
curl -X POST http://127.0.0.1:5000/sensor -H "Content-Type: application/json" -d "{\"temp\": 22.5}"
```

**Linux/Mac:**
```bash
curl -X POST http://127.0.0.1:5000/sensor -H "Content-Type: application/json" -d '{"temp": 22.5}'
```

**Python script (any OS):**
```python
import requests
response = requests.post("http://127.0.0.1:5000/sensor", json={"temp": 22.5})
print(response.json())
```

In this case we are using a POST method because browsers cannot send POST requests directly from the address bar, so you need a terminal or a script.

After running the command or the script, you'll receive the following message:
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

You can obtain the same result by copying the link [http://127.0.0.1:5000/sensor/history](http://127.0.0.1:5000/sensor/history) on your browser.
 
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