# Smart-Stove-Monitor
Smart Stove Monitor is a real-time safety system that uses a laptop camera and computer vision to detect if your gas stove is left on. It instantly alerts your phone with a vibration and alarm the moment you leave home — and also warns you if no one has been near the stove for more than 10 minutes.
🔥 Smart Stove Monitor
An AI-powered safety system that detects when your gas stove is left on and instantly alerts your phone when you leave home.

The whole idea is as explained in the html presentation below
https://drive.google.com/file/d/1G8CVV5JZ-a3hbrhjboBNN9XEOUwPq1QW/view?usp=share_link


📽 Demo Video
▶ Watch Demo Video
https://drive.google.com/file/d/1gC7T5MNUq8Ut_-HSXEi6wxVi_B5UxP_e/view?usp=sharing



https://github.com/user-attachments/assets/f86d1c38-81bb-4a11-b329-4b3c0163c3d7

📖 Project Description
Smart Stove Monitor is a real-time safety system that uses computer vision and GPS tracking to prevent gas stove accidents. A laptop camera continuously watches the stove. When a flame is detected AND your phone moves more than 5 meters from home, an instant alert is sent to your phone with vibration and sound. It also alerts you if no one is detected near the stove for more than 10 minutes — protecting elderly users and anyone who forgets the stove is on.

🛠 Tech Stack
Layer
Technology
Backend
Python 3, Flask
Computer Vision
OpenCV, NumPy
GPS Distance
Haversine Formula
Frontend
HTML5, CSS3, Vanilla JavaScript
Browser APIs
Geolocation API, Web Audio API, Vibration API
Tunnel (HTTPS)
Cloudflare Tunnel / ngrok
Threading
Python threading module


✨ Features
🔥 Real-time Flame Detection — OpenCV analyzes every video frame using HSV color space to detect gas flame (orange/yellow range). Triggers when more than 500 flame-colored pixels are detected.
📍 GPS Distance Tracking — Phone browser sends GPS coordinates every 5 seconds. Server calculates distance from home using the Haversine formula with meter-level accuracy.
📳 Instant Phone Alert — When flame is ON and you move more than 5 meters away, your phone vibrates, plays an alarm tone, and shows a warning on screen.
🚶 Motion Detection Alert — If no human motion is detected near the stove for more than 10 minutes while the flame is on, a second alert is triggered — protecting elderly users or anyone who steps out briefly.
📊 Live Status Dashboard — The phone browser shows live distance from home, flame status (ON/OFF), and your current GPS coordinates updating in real time.
🔒 100% Local — All processing runs on your laptop. No cloud, no subscription, no data sent to external servers.

📸 Screenshots
Add screenshots to docs/screenshots/ and update paths below.
Phone Dashboard
Flame Detected
Alert Triggered





🏗 Architecture Diagram
See https://drive.google.com/file/d/1LkyQZCSYQWb3-_Ui_zCNSuQDEddG7gwR/view?usp=sharing
[Gas Stove] → [Laptop Camera] → [OpenCV HSV Analysis]
                                        ↓
                              [Flask Server :5050]
                                        ↑↓
                        [Phone Browser Geolocation API]
                                        ↓
                           [Haversine Distance Calc]
                                        ↓
                    ┌───────────────────┴───────────────────┐
                    ↓                                       ↓
          [Flame ON + Distance > 5m]          [Flame ON + No Motion > 10min]
                    ↓                                       ↓
            [ALERT TYPE 1]                          [ALERT TYPE 2]
          "You left home!"                      "No one near stove!"
                    ↓                                       ↓
                        [Phone Vibration + Audio Alarm]


⚙️ Installation
Prerequisites
Python 3.8+
A laptop with a webcam or video file of stove
Mobile phone on the same WiFi (or use Cloudflare tunnel)
Step 1 — Clone the repository
git clone https://github.com/your-username/smart-stove-monitor.git
cd smart-stove-monitor

Step 2 — Install dependencies
pip install -r requirements.txt

Step 3 — Install Cloudflare Tunnel (for HTTPS on phone)
brew install cloudflared   # macOS
# OR
sudo apt install cloudflared  # Ubuntu/Linux


▶ Run Commands
Step 1 — Configure your home GPS coordinates
Edit src/stove_gui.py and update:
HOME_LAT = 11.6854   # Your home latitude
HOME_LON = 76.1320   # Your home longitude

Step 2 — Add your video or connect camera
VIDEO_PATH = "video.mp4"   # Or use 0 for live webcam

Step 3 — Start the server
python src/stove_gui.py

Step 4 — Create HTTPS tunnel (required for GPS on phone)
# In a new terminal:
cloudflared tunnel --url http://localhost:5050

Step 5 — Open on phone
Copy the https://xxxx.trycloudflare.com URL from the tunnel output and open it in your phone browser. Allow location permission when asked.

🔌 API Docs
GET /
Returns the monitoring web page (HTML dashboard).
Response: HTML page with live GPS + flame status display.

POST /location
Receives phone GPS coordinates and returns alert status.
Request Body:
{
  "lat": 11.68541,
  "lon": 76.13198
}

Response:
{
  "alert": true,
  "flame": true,
  "distance": 47,
  "message": "Flame detected! You are 47m away!"
}

Field
Type
Description
alert
boolean
True if flame ON and distance > 5m
flame
boolean
True if flame currently detected
distance
integer
Distance from home in meters
message
string
Human-readable status message


👥 Team Members
Name
Role
Guru Revathi B
Developer & Designer
Vijaya Lode
Developer & Designer


📄 License
This project is licensed under the MIT License — see LICENSE for details.

🤖 AI Tools Used
Claude (Anthropic) — Used for debugging Python Flask code, designing the HTML dashboard, generating the architecture flowchart, and creating project documentation.
Prompts documented in https://drive.google.com/drive/folders/1ITt26vbtWmPOIaIzqhXa2X05YfCGnD3i?usp=sharing

Made with ❤️ at TinkerHub Hackathon 2026

