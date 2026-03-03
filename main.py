import cv2
import time
import requests
from ultralytics import YOLO

# -------------------------------
# 1. Load Model
# -------------------------------
model = YOLO('best.pt')

# -------------------------------
# 2. ESP8266 IP ADDRESS
# (Replace with IP shown in Serial Monitor)
# -------------------------------
ESP_IP = "http://192.168.43.128/access"   # <<< CHANGE THIS

# -------------------------------
# 3. Class IDs from your model
# -------------------------------
SAFE_IDS = [0, 1, 2, 3, 4, 8, 11, 12] 
PERSON_ID = 9   

# -------------------------------
# 4. Configuration
# -------------------------------
VOTE_WINDOW = 10     
HELMET_THRESHOLD = 5 

# -------------------------------
# 5. State variables
# -------------------------------
start_time = None
helmet_detections = 0
decision_sent = False   # To avoid multiple requests

cap = cv2.VideoCapture(0)
print("\n--- SYSTEM READY: STAND IN FRONT OF CAMERA ---")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection
    results = model.predict(frame, conf=0.25, verbose=False)
    detected_ids = results[0].boxes.cls.tolist()

    # Check if person or helmet present
    person_in_frame = PERSON_ID in detected_ids or any(hid in detected_ids for hid in SAFE_IDS)

    if person_in_frame:

        if start_time is None:
            start_time = time.time()
            helmet_detections = 0
            print("Person detected. Starting 10-second analysis...")

        elapsed = time.time() - start_time

        # Count helmet detections
        if any(hid in detected_ids for hid in SAFE_IDS):
            helmet_detections += 1
            print(f"Helmet Count: {helmet_detections}")

        if elapsed < VOTE_WINDOW:
            remaining = int(VOTE_WINDOW - elapsed)
            status_msg = f"ANALYZING: {remaining}s | Count: {helmet_detections}"

            annotated_frame = results[0].plot()
            cv2.putText(annotated_frame, status_msg, (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 165, 0), 2)
            cv2.imshow("Helmet Access Control", annotated_frame)

        else:
            print("\n" + "="*50)
            print(f"FINAL TALLY: {helmet_detections} helmet detections.")

            try:
                if helmet_detections >= HELMET_THRESHOLD:
                    print("STATUS: HELMET WEAR - FULL ACCESS")
                    response = requests.get(ESP_IP + "?status=1", timeout=3)
                else:
                    print("STATUS: HELMET NOT WEAR - RESTRICTED ACCESS")
                    response = requests.get(ESP_IP + "?status=0", timeout=3)

                print("ESP Response:", response.text)

            except requests.exceptions.RequestException as e:
                print("⚠ ERROR: Unable to send request to ESP8266")
                print("Check WiFi connection and IP address.")
                print("Error Details:", e)

            print("="*50)
            break

    else:
        cv2.putText(frame, "SCANNING...", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.imshow("Helmet Access Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -------------------------------
# SHUTDOWN
# -------------------------------
print("\nReleasing Camera Resources. Goodbye.")
cap.release()
cv2.destroyAllWindows()