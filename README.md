# 🪖 AI & ML Based Smart Helmet Detection and Access Control System

An AI-powered real-time helmet detection system integrated with IoT for automated access control using YOLOv8 and ESP8266 (NodeMCU).

This project detects whether a person is wearing a helmet using computer vision and grants or restricts access accordingly by controlling a relay module wirelessly.

---

## 🚀 Project Overview

This system uses:

- 🎥 OpenCV for real-time camera capture
- 🧠 YOLOv8 (Ultralytics) for helmet detection
- 📡 ESP8266 (NodeMCU) for IoT communication
- 🔌 Relay Module for speed control
- 💡 LEDs & Buzzer for visual/audio feedback

After analyzing detection results for 10 seconds, the system:

- ✅ Grants access if helmet detections ≥ threshold
- ❌ Denies access if below threshold

The result is sent wirelessly to NodeMCU via WiFi.

---

## 🏗️ System Architecture

- Camera → YOLO Model → Python → WiFi → ESP8266 → Relay → Access

---

## ⚙️ Technologies Used

- Python 3.x
- OpenCV
- Ultralytics YOLOv8
- Requests Library
- Arduino IDE
- ESP8266 (NodeMCU)

---

## 📂 Project Structure

- ├── best.pt # Trained YOLO model
- ├── helmet_detection.py # Main Python script
- ├── nodemcu_code.ino # ESP8266 Arduino code
- └── README.md

---

## 🔧 Installation (Python Side)

### 1️⃣ Install Dependencies

```bash
- pip install opencv-python
- pip install ultralytics
- pip install requests

---

### 2️⃣ Place your trained model

- Put best.pt in the project directory.

---

### 3️⃣ Update ESP IP Address

- In the Python file:

- ESP_IP = "http://YOUR_NODEMCU_IP/access"