from flask import Flask, request, jsonify, render_template_string
import cv2
import numpy as np
import math
import threading
import time

app = Flask(__name__)

# -----------------------------
# CONFIGURATION
# -----------------------------
HOME_LAT = 11.6854
HOME_LON = 76.1320
DISTANCE_LIMIT = 5   # meters
VIDEO_PATH = "video.mp4"

flame_detected = False
flame_lock = threading.Lock()

# -----------------------------
# Distance Calculation
# -----------------------------
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# -----------------------------
# FLAME DETECTION THREAD
# -----------------------------
def detect_flame_video():
    global flame_detected
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([10, 100, 100])
        upper = np.array([35, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        flame_pixels = cv2.countNonZero(mask)

        with flame_lock:
            flame_detected = flame_pixels > 500

        time.sleep(0.03)

# -----------------------------
# WEB PAGE
# -----------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Stove Monitor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 30px; background: #f5f5f5; }
        h2 { color: #333; }
        .card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin: 12px auto;
            max-width: 340px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .label { font-size: 0.85em; color: #888; margin-bottom: 4px; }
        .value { font-size: 2.5em; font-weight: bold; color: #333; }
        .unit  { font-size: 0.9em; color: #888; }
        #flame-card .value { color: #e74c3c; }
        #flame-card.safe .value { color: #27ae60; }
        #dist-card .value  { color: #2980b9; }
        .alert-box {
            background: #ffe0e0;
            border: 2px solid #e74c3c;
            border-radius: 12px;
            padding: 14px;
            margin: 12px auto;
            max-width: 340px;
            color: #c0392b;
            font-weight: bold;
            display: none;
        }
        .safe-box {
            background: #e0ffe0;
            border: 2px solid #27ae60;
            border-radius: 12px;
            padding: 14px;
            margin: 12px auto;
            max-width: 340px;
            color: #1e8449;
            font-weight: bold;
            display: none;
        }
        #coords { font-size: 0.75em; color: #aaa; margin-top: 8px; }
    </style>
</head>
<body>
    <h2>Smart Stove Safety System</h2>

    <div class="card" id="dist-card">
        <div class="label">Distance from Home</div>
        <div class="value" id="distance-val">--</div>
        <div class="unit">meters</div>
        <div style="font-size:0.8em; color:#aaa; margin-top:6px;">Alert threshold: 5 m</div>
    </div>

    <div class="card" id="flame-card">
        <div class="label">Flame Status</div>
        <div class="value" id="flame-val">--</div>
    </div>

    <div class="alert-box" id="alert-box">WARNING: Stove is ON and you left home!</div>
    <div class="safe-box"  id="safe-box">All clear!</div>

    <div id="coords">Waiting for GPS...</div>

    <script>
        function sendLocation(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            document.getElementById("coords").innerHTML =
                "Your GPS: " + lat.toFixed(5) + ", " + lon.toFixed(5);

            fetch('/location', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ lat: lat, lon: lon })
            })
            .then(response => response.json())
            .then(data => {
                // Update distance card
                document.getElementById("distance-val").innerHTML = data.distance;

                // Update flame card
                const flameEl   = document.getElementById("flame-val");
                const flameCard = document.getElementById("flame-card");
                if (data.flame) {
                    flameEl.innerHTML = "ON";
                    flameCard.classList.remove("safe");
                } else {
                    flameEl.innerHTML = "OFF";
                    flameCard.classList.add("safe");
                }

                // Show alert or safe box
                const alertBox = document.getElementById("alert-box");
                const safeBox  = document.getElementById("safe-box");
                if (data.alert) {
                    alertBox.style.display = "block";
                    safeBox.style.display  = "none";
                    if (navigator.vibrate) navigator.vibrate([500, 200, 500, 200, 500]);
                    try {
                        var ctx = new AudioContext();
                        var osc = ctx.createOscillator();
                        osc.connect(ctx.destination);
                        osc.frequency.value = 880;
                        osc.start();
                        setTimeout(() => osc.stop(), 1000);
                    } catch(e) {}
                } else {
                    alertBox.style.display = "none";
                    safeBox.style.display  = "block";
                }
            })
            .catch(err => {
                document.getElementById("coords").innerHTML = "Connection error: " + err;
            });
        }

        function errorHandler(err) {
            document.getElementById("coords").innerHTML = "Location error: " + err.message;
        }

        if (navigator.geolocation) {
            navigator.geolocation.watchPosition(sendLocation, errorHandler, {
                enableHighAccuracy: true,
                maximumAge: 5000,
                timeout: 10000
            });
        } else {
            document.getElementById("coords").innerHTML = "Geolocation not supported.";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/location', methods=['POST'])
def location():
    data = request.get_json()
    if not data or 'lat' not in data or 'lon' not in data:
        return jsonify({"alert": False, "message": "Invalid data"}), 400

    lat = data['lat']
    lon = data['lon']
    distance = calculate_distance(HOME_LAT, HOME_LON, lat, lon)

    with flame_lock:
        is_flame = flame_detected

    is_alert = is_flame and distance > DISTANCE_LIMIT

    return jsonify({
        "alert":    is_alert,
        "flame":    is_flame,
        "distance": int(distance),
        "message":  "Flame detected! You are " + str(int(distance)) + "m away!" if is_alert
                    else "Safe. Flame: " + ("YES" if is_flame else "NO") + " | Distance: " + str(int(distance)) + "m"
    })

if __name__ == '__main__':
    threading.Thread(target=detect_flame_video, daemon=True).start()
    app.run(host='0.0.0.0', port=5050, debug=False, ssl_context='adhoc')