# 🪖 Intelligent Helmet Detection with Automated Vehicle Control

An AI-powered real-time helmet detection system using **YOLOv8** (trained model) for intelligent computer vision-based automated vehicle control. The system detects helmet usage and automatically controls vehicle ignition via serial communication or logs telemetry data to **ThingSpeak IoT Cloud** for remote monitoring and fleet analytics.

---

## 🚀 Project Overview

The project provides an automated safety layer for vehicles (such as motorbikes or industrial machinery) by enforcing helmet wearing. It is designed to work in two operation modes:

1. **Local Real-Time Enforcement (Serial / Option 1)**:
   - Uses a dashboard-mounted camera to monitor the driver.
   - Detects the presence of a person. Once a person is detected, a **10-second timer** starts.
   - If a helmet is detected at any point within the 10 seconds, the vehicle ignition is immediately **enabled** (sends `1` to Arduino/NodeMCU over Serial) and the script exits.
   - If the timer expires without detecting a helmet, the vehicle is **disabled** (sends `0` to Arduino/NodeMCU over Serial) and the script exits.
   
2. **Cloud Logging & Compliance Analytics (ThingSpeak / Option 2)**:
   - Performs a stable voting system over a **10-second window**.
   - Calculates the ratio of frames in which a helmet was detected.
   - If a person is present and the helmet detection ratio exceeds **50%**, the compliance is marked as successful (`field1 = 1`, `field2 = 0`).
   - If not, it is marked as non-compliant (`field1 = 0`, `field2 = 1`).
   - The compliance result is automatically sent to the **ThingSpeak IoT Cloud** channel for fleet monitoring, remote audits, and safety analytics.

---

## 🏗️ System Architecture

```text
Dashboard Camera → YOLOv8 Inference (Python) 
                          │
         ┌────────────────┴────────────────┐
         ▼ (Option 1: Serial)              ▼ (Option 2: Cloud API)
   PySerial Link                     ThingSpeak IoT Cloud
         │                                 │
         ▼ (USB/Serial Rx)                 ▼ (WiFi Client Poll)
  ESP8266 / Arduino ────────────────► ESP8266 (NodeMCU)
         │
         ▼
    Relay Module ──► Vehicle Ignition Control (ON/OFF)
         │
    Buzzer / LEDs ──► Driver Alerts
```

---

## 📂 Project Structure

- **[main.py](file:///c:/Users/Raiyan/Downloads/INTELLIGENT-HELMET-DETECTION-WITH-AUTOMATED-VEHICLE-CONTROL-USING-COMPUTER-VISION/main.py)**: Real-time helmet detection script with serial communication for direct microcontroller relay control.
- **[thingspeak.py](file:///c:/Users/Raiyan/Downloads/INTELLIGENT-HELMET-DETECTION-WITH-AUTOMATED-VEHICLE-CONTROL-USING-COMPUTER-VISION/thingspeak.py)**: Stable-vote helmet detection script with automated ThingSpeak cloud logging.
- **[best.pt](file:///c:/Users/Raiyan/Downloads/INTELLIGENT-HELMET-DETECTION-WITH-AUTOMATED-VEHICLE-CONTROL-USING-COMPUTER-VISION/best.pt)**: The custom-trained YOLOv8 model weights optimized for detecting helmets, persons, and related objects.
- **[Helmet_Detection_using_Yolo.ipynb](file:///c:/Users/Raiyan/Downloads/INTELLIGENT-HELMET-DETECTION-WITH-AUTOMATED-VEHICLE-CONTROL-USING-COMPUTER-VISION/Helmet_Detection_using_Yolo.ipynb)**: Google Colab Jupyter Notebook used for downloading the custom dataset from Roboflow, and training the YOLO model for 50 epochs on a Tesla T4 GPU.
- **[requirements.txt](file:///c:/Users/Raiyan/Downloads/INTELLIGENT-HELMET-DETECTION-WITH-AUTOMATED-VEHICLE-CONTROL-USING-COMPUTER-VISION/requirements.txt)**: List of required Python packages (`opencv-python`, `ultralytics`, `pyserial`, `requests`, etc.).
- **[.gitignore](file:///c:/Users/Raiyan/Downloads/INTELLIGENT-HELMET-DETECTION-WITH-AUTOMATED-VEHICLE-CONTROL-USING-COMPUTER-VISION/.gitignore)**: Files and directories to be ignored by Git (such as virtual environments).

---

## 🎯 Model & Classes

The model (`best.pt`) was trained on a custom dataset containing **13 classes**. The classes map as follows:

| Class ID | Class Name | Category | Action in System |
|---|---|---|---|
| **0** | Cycling Helmet | Helmet / Safe | `SAFE_IDS` (Passes Safety Check) |
| **1** | half face | Helmet / Safe | `SAFE_IDS` (Passes Safety Check) |
| **2** | hard hat | Helmet / Safe | `SAFE_IDS` (Passes Safety Check) |
| **3** | helmet | Helmet / Safe | `SAFE_IDS` (Passes Safety Check) |
| **4** | modular helmet | Helmet / Safe | `SAFE_IDS` (Passes Safety Check) |
| **5** | motorbike | Vehicle | Ignored (Contextual) |
| **6** | motorcyclist | Person on Bike | Ignored (Contextual) |
| **7** | without-helmet / no-helmet | Violator | Triggers Non-compliance / Violator |
| **8** | nutshell | Helmet / Safe | `SAFE_IDS` (Passes Safety Check) |
| **9** | person | Driver | `PERSON_ID` (Triggers detection window) |
| **10** | plate | License Plate | Ignored (Contextual) |
| **11** | quarter face helmet | Helmet / Safe | `SAFE_IDS` (Passes Safety Check) |
| **12** | sports helmet | Helmet / Safe | `SAFE_IDS` (Passes Safety Check) |

---

## 🛠️ Installation & Setup

### Python Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd INTELLIGENT-HELMET-DETECTION-WITH-AUTOMATED-VEHICLE-CONTROL-USING-COMPUTER-VISION
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv helmet_env
   ```

3. **Activate the virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     .\helmet_env\Scripts\Activate.ps1
     ```
   - **Windows (CMD):**
     ```cmd
     helmet_env\Scripts\activate.bat
     ```
   - **macOS/Linux:**
     ```bash
     source helmet_env/bin/activate
     ```

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔌 Hardware Setup

### Wiring Diagram (Typical NodeMCU / Arduino)

```text
NodeMCU ESP8266         Relay Module
┌─────────────┐        ┌────────────┐
│         3V3 ├────────► VCC        │
│         GND ├────────► GND        │
│          D1 ├────────► IN         │
└─────────────┘        └────────────┘
                         │   ┌──────┐
                         └───┤ NO   ├────► Ignition Circuit Line 1
                             │ COM  ├────► Ignition Circuit Line 2 (12V DC)
                             └──────┘

NodeMCU ESP8266         Active Buzzer
┌─────────────┐        ┌────────────┐
│          D2 ├────────► POSITIVE   │
│         GND ├────────► NEGATIVE   │
└─────────────┘        └────────────┘
```

---

## 🤖 Microcontroller Code (Arduino IDE)

Since the microcontroller (ESP8266 / Arduino) acts as the physical receiver, you can use either of the following two implementation sketches based on your chosen option.

### Sketch 1: Direct Serial Receiver (For `main.py`)
This code reads command characters directly from the USB serial port. Upload this to your NodeMCU/Arduino:

```cpp
// Serial Control for Vehicle Ignition
const int relayPin = D1;  // GPIO5 (Pin D1 on NodeMCU)
const int buzzerPin = D2; // GPIO4 (Pin D2 on NodeMCU)

void setup() {
  Serial.begin(9600);
  pinMode(relayPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  
  // Start with the relay open (Vehicle disabled)
  digitalWrite(relayPin, LOW);
  digitalWrite(buzzerPin, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    char signal = Serial.read();
    
    if (signal == '1') {
      // Helmet Detected -> Enable vehicle ignition
      digitalWrite(relayPin, HIGH);
      
      // Happy confirmation beep
      digitalWrite(buzzerPin, HIGH);
      delay(400);
      digitalWrite(buzzerPin, LOW);
      
      Serial.println("Ignition ENABLED");
    } 
    else if (signal == '0') {
      // No Helmet -> Keep vehicle disabled / alarm
      digitalWrite(relayPin, LOW);
      
      // Rapid alert beeps
      for (int i = 0; i < 4; i++) {
        digitalWrite(buzzerPin, HIGH);
        delay(150);
        digitalWrite(buzzerPin, LOW);
        delay(150);
      }
      
      Serial.println("Ignition DISABLED");
    }
  }
}
```

### Sketch 2: ThingSpeak Polling Subscriber (For `thingspeak.py`)
This sketch connects the NodeMCU to WiFi and polls the ThingSpeak channel to read the latest safety status and actuate the relay.

```cpp
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

// WiFi Configuration
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// ThingSpeak Configuration
const char* channelID = "YOUR_CHANNEL_ID"; // e.g. "2489812"
const char* readAPIKey = "YOUR_READ_API_KEY"; // Optional if channel is public

// Hardware Pins
const int relayPin = D1;
const int buzzerPin = D2;

// Polling interval (ThingSpeak updates have limits, 15 seconds recommended)
unsigned long lastTime = 0;
const unsigned long timerDelay = 15000;

void setup() {
  Serial.begin(115200);
  pinMode(relayPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(relayPin, LOW);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");
}

void loop() {
  if ((millis() - lastTime) > timerDelay) {
    if (WiFi.status() == WL_CONNECTED) {
      WiFiClient client;
      HTTPClient http;

      // URL to get the last value of Field 1 (Helmet detection state)
      String url = "http://api.thingspeak.com/channels/" + String(channelID) + "/fields/1/last.txt";
      
      http.begin(client, url);
      int httpResponseCode = http.GET();
      
      if (httpResponseCode > 0) {
        String payload = http.getString();
        payload.trim();
        Serial.print("ThingSpeak Field 1 Value: ");
        Serial.println(payload);
        
        if (payload == "1") {
          // Helmet worn -> Enable ignition
          digitalWrite(relayPin, HIGH);
          Serial.println("Compliance OK: Relay ON");
        } else if (payload == "0") {
          // Helmet not worn -> Disable ignition
          digitalWrite(relayPin, LOW);
          Serial.println("Safety Alert: Relay OFF");
        }
      } else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      http.end();
    } else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}
```

---

## ⚙️ Running the Applications

### Direct Control Mode (PySerial Integration)

1. Connect the ESP8266 or Arduino to your computer via USB.
2. Check your device's COM port (e.g., `COM6` on Windows, `/dev/ttyUSB0` on Linux).
3. Open `main.py` and modify line 14:
   ```python
   arduino = serial.Serial('COM6', 9600)  # Put your COM port here
   ```
4. Run the script:
   ```bash
   python main.py
   ```
5. Position yourself in front of the camera. The script will start scanning. Once a person is detected, it will track for 10 seconds. If you put on a helmet, it sends `1` and starts the vehicle. If you do not, it sends `0` and exits.

### Cloud Reporting Mode (ThingSpeak Log)

1. Create a channel on [ThingSpeak](https://thingspeak.com/).
2. Enable **Field 1** (Helmet compliance: 1 = wear, 0 = no wear) and **Field 2** (Non-compliance: 1 = no wear, 0 = wear).
3. Copy your **Write API Key**.
4. Open `thingspeak.py` and update line 14:
   ```python
   THINGSPEAK_API_KEY = "YOUR_WRITE_API_KEY"
   ```
5. Run the script:
   ```bash
   python thingspeak.py
   ```
6. The window runs for 10 seconds, calculates your compliance ratio, prints it, and updates your ThingSpeak dashboard in real-time.

---

## 🚨 Troubleshooting

| Problem | Cause | Solution |
|---|---|---|
| `SerialException: could not open port` | Wrong COM port configured, or port is occupied by another program (e.g. Arduino Serial Monitor). | Verify COM port in Device Manager/Arduino IDE. Close Serial Monitor before running the script. |
| `YOLO best.pt file not found` | The trained model is not in the workspace root folder. | Ensure `best.pt` file exists in the main directory. |
| `cv2.error: OpenCV(4.x.x) ...` | Camera permissions blocked or wrong camera index. | Verify webcam connections. If using an external USB camera, change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` or `2`. |
| Connection timeouts to ThingSpeak | No internet connection or blocked firewall. | Ensure the computer running the python script has an active internet connection. Check the Write API key. |
| Relay does not trigger | Incorrect GPIO wiring or voltage mismatch. | Make sure NodeMCU pin matches your sketch pin (e.g. `D1`). Ensure the relay module gets stable power (5V or 3.3V as specified). |

---

## 🔒 Security & Failsafe Guidelines

- **Hardware Bypass Override**: Always design a physical override switch on the vehicle dashboard that can bypass the relay circuit in case of system malfunction or emergency situations.
- **Credential Safety**: Avoid committing API keys to Git. Consider utilizing Python's `python-dotenv` package to load keys from a `.env` file.
- **Safety Standard Conformity**: This system is a prototype. Integration into actual vehicle ignition lines should follow automotive electrical and functional safety guidelines (e.g., ISO 26262).

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository, make changes in a feature branch, and submit a Pull Request.

---

## 📝 License

This project is licensed under the **MIT License**.