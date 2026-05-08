# 🪖 INTELLIGENT HELMET DETECTION WITH AUTOMATED VEHICLE CONTROL USING COMPUTER VISION

An AI-powered real-time helmet detection system using YOLOv8 for intelligent computer vision-based automated vehicle control. The system detects helmet usage and automatically controls vehicle ignition and motor functions via IoT-enabled ESP8266 (NodeMCU).

This project enables vehicle automation by detecting whether a driver is wearing a helmet, and automatically grants or denies vehicle operation accordingly by controlling the vehicle's ignition system through a relay module wirelessly.

---

## 🚀 Project Overview

This intelligent system uses:

- 🎥 **OpenCV** for real-time driver camera capture
- 🧠 **YOLOv8** (Ultralytics) for helmet detection and classification
- 📡 **ESP8266 (NodeMCU)** for IoT-based vehicle control communication
- ⚡ **Relay Module** for vehicle ignition and motor control
- 💡 **LEDs & Buzzer** for visual/audio feedback and alerts
- ☁️ **ThingSpeak** for IoT data logging and fleet monitoring

After analyzing detection results for 10 seconds, the system:

- ✅ **Enables vehicle** if helmet detection ≥ threshold (driver is protected)
- ❌ **Disables vehicle** if below threshold (safety not confirmed)
- 🚗 **Controls ignition** via relay to prevent unauthorized operation
- 📊 **Logs results** to ThingSpeak for fleet monitoring and analytics

---

## 🏗️ System Architecture

```
Driver Camera → YOLO Helmet Detection → Python Script → WiFi → ESP8266 → Relay → Vehicle Ignition Control
                                              ↓
                                      ThingSpeak API → Cloud Fleet Monitoring & Analytics
```

**Flow:**
1. Camera captures real-time video of driver
2. YOLOv8 detects helmet presence/absence
3. Python analyzes detection confidence over time window
4. Decision sent via WiFi to ESP8266
5. ESP8266 controls vehicle relay (ignition ON/OFF)
6. Telemetry logged to ThingSpeak cloud platform

---

## ⚙️ Technologies Used

- **Python 3.x** - Main application
- **OpenCV** - Real-time video processing
- **Ultralytics YOLOv8** - Deep learning object detection
- **Requests Library** - HTTP communication
- **PySerial** - Serial communication with Arduino
- **ESP8266 (NodeMCU)** - WiFi-enabled microcontroller
- **Arduino IDE** - Microcontroller programming
- **ThingSpeak** - IoT data cloud platform

---

## 📂 Project Structure

```
INTELLIGENT HELMET DETECTION WITH AUTOMATED VEHICLE CONTROL USING COMPUTER VISION/
├── best.pt                  # Trained YOLOv8 model
├── main.py                  # Main detection script (Serial/ESP8266)
├── thingspeak.py            # Detection script with ThingSpeak logging
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── .gitignore              # Git ignore patterns
├── helmet_env/             # Python virtual environment
└── [Additional files]
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Automotive-grade camera or USB camera module (mounted on vehicle dashboard)
- ESP8266 (NodeMCU) board with WiFi capability
- 12V Relay module for vehicle ignition control
- Vehicle power supply (12V DC from vehicle battery)
- Electronic components (resistors, capacitors, diodes)
- Vehicle control circuit and wiring harness
- Arduino IDE for ESP8266 programming

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-ML-BASED-HELMET-DETECTION-SYSTEM
   ```

2. **Create virtual environment**
   ```bash
   python -m venv helmet_env
   ```

3. **Activate virtual environment**
   - **Windows:**
     ```bash
     helmet_env\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source helmet_env/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎯 Usage

### Option 1: Serial Communication with ESP8266

Run the main detection script that communicates via serial:

```bash
python main.py
```

**Configuration:**
- Edit the serial port in `main.py`:
  ```python
  arduino = serial.Serial('COM6', 9600)  # Change COM6 to your port
  ```

### Option 2: ThingSpeak Cloud Logging

Run the detection script with ThingSpeak integration:

```bash
python thingspeak.py
```

**Configuration:**
- Update your ThingSpeak API key in `thingspeak.py`:
  ```python
  THINGSPEAK_API_KEY = "YOUR_API_KEY"
  ```

---

## ⚙️ Configuration

### Detection Parameters

Edit the following in the Python scripts:

```python
NO_HELMET_WAIT = 10          # Time window for helmet detection (seconds)
VOTE_WINDOW = 10             # Voting window size
DETECTION_THRESHOLD = 0.25   # YOLOv8 confidence threshold
```

### Class IDs

The model recognizes multiple helmet types:
```python
SAFE_IDS = [0, 1, 2, 3, 4, 8, 11, 12]  # Helmet class IDs
PERSON_ID = 9                            # Person class ID
```

---

## 🔌 Hardware Setup

### Vehicle-ESP8266 Integration

1. **Relay Module Configuration**
   - Connect relay IN pin to ESP8266 GPIO pin (D1-D8)
   - Connect relay NO (Normally Open) to vehicle ignition circuit
   - Connect relay COM to vehicle power supply
   
2. **Camera Installation**
   - Mount camera on vehicle dashboard/interior
   - Ensure clear view of driver's head area
   - Connect camera to on-board computer or Raspberry Pi

3. **Power Management**
   - Supply 12V DC from vehicle battery to relay module
   - Use voltage regulator (12V to 5V) for ESP8266
   - Implement fuses for circuit protection

4. **ESP8266 WiFi Programming**
   - Program using Arduino IDE with WiFi credentials
   - Set up local network or hotspot connectivity
   - Configure ThingSpeak API integration

5. **Safety Systems**
   - Connect LED indicators (green/red) for driver feedback
   - Connect buzzer for audio alerts
   - Implement manual override switch for emergencies

### Serial Connection

- Connect ESP8266 to main computer via USB/Serial for configuration
- Default baud rate: 9600

---

## 🚨 Error Handling

Common issues and solutions:

| Issue | Solution |
|-------|----------|
| Serial port not found | Check COM port in Device Manager or device connection |
| Model file not found | Ensure `best.pt` is in project root directory |
| Camera not detected | Check camera permissions, USB connection, or camera index in code |
| WiFi disconnection | Verify ESP8266 WiFi credentials and network signal strength |
| Vehicle relay not responding | Check ESP8266 GPIO pin configuration and relay wiring |
| False helmet detections | Adjust `DETECTION_THRESHOLD` parameter or retrain model |
| Helmet detection lag | Increase `NO_HELMET_WAIT` or optimize Python script performance |

---

## 📊 Monitoring & Analytics

Access ThingSpeak dashboard to monitor:
- **Real-time helmet detection status** per vehicle
- **Vehicle start attempt history** with helmet compliance
- **Driver safety compliance statistics** and trends
- **Fleet-wide helmet detection analytics**
- **Alert logs** for safety violations

**ThingSpeak Dashboard Features:**
- Multi-channel monitoring for fleet vehicles
- Custom alert triggers for non-compliance
- Historical data export for safety audits
- Real-time notifications via email/SMS

ThingSpeak URL: `https://thingspeak.com/`

---

## 🔒 Security & Safety Notes

- **Never compromise safety**: Implement hardware failsafes to prevent vehicle control bypass
- Store API keys in environment variables (use `.env` file)
- Never commit sensitive credentials to version control
- Use HTTPS for all cloud communications
- Implement proper authentication on ESP8266
- Protect vehicle ignition circuit with fuses and relays
- Regular testing of helmet detection accuracy
- Compliance with vehicle safety standards (ISO 26262)
- Maintain detailed logs for legal/insurance purposes

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

Created as an intelligent AI & ML-based vehicle safety system for automated helmet detection and vehicle control. Designed to enhance rider/driver safety compliance through computer vision technology and IoT automation.

---

## 📧 Support

For issues or questions, please open an issue in the repository or contact the development team.

### 3️⃣ Update ESP IP Address

- In the Python file:

- ESP_IP = "http://YOUR_NODEMCU_IP/access"