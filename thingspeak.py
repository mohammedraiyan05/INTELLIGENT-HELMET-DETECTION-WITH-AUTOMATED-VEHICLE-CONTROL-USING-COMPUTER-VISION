import cv2
import time
import requests
from ultralytics import YOLO

# -------------------------------
# 1. Load Model
# -------------------------------
model = YOLO('best.pt')

# -------------------------------
# 2. ThingSpeak Configuration
# -------------------------------
THINGSPEAK_API_KEY = "HCKTNDH0JXJOLPGP"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# -------------------------------
# 3. Class IDs
# -------------------------------
SAFE_IDS = [0, 1, 2, 3, 4, 8, 11, 12]
PERSON_ID = 9

# -------------------------------
# 4. Config
# -------------------------------
VOTE_WINDOW = 10

# -------------------------------
# 5. Camera Start
# -------------------------------
cap = cv2.VideoCapture(0)

print("\n--- SYSTEM STARTED (STABLE MODE) ---")

# -------------------------------
# RUN ONLY ONCE
# -------------------------------
start_time = time.time()
helmet_detections = 0
frame_count = 0
person_seen = False

while True:
    ret, frame = cap.read()

    if not ret:
        continue

    frame_count += 1

    # YOLO Detection
    results = model.predict(frame, conf=0.25, verbose=False)
    detected_ids = results[0].boxes.cls.tolist()

    # Person detection
    if PERSON_ID in detected_ids or any(hid in detected_ids for hid in SAFE_IDS):
        person_seen = True

    # Helmet detection
    if any(hid in detected_ids for hid in SAFE_IDS):
        helmet_detections += 1

    elapsed = time.time() - start_time
    remaining = int(VOTE_WINDOW - elapsed)

    # Display
    annotated_frame = results[0].plot()
    cv2.putText(annotated_frame,
                f"Time: {max(0, remaining)}s | Helmet Count: {helmet_detections}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 165, 255),
                2)

    cv2.imshow("Helmet Detection", annotated_frame)

    # 🔥 Stop after 10 sec
    if elapsed >= VOTE_WINDOW:
        print("\n--- 10 Seconds Completed ---")

        # Calculate ratio
        if frame_count > 0:
            helmet_ratio = helmet_detections / frame_count
        else:
            helmet_ratio = 0

        print("Helmet Ratio:", round(helmet_ratio, 2))

        # -------------------------------
        # FINAL DECISION (STABLE)
        # -------------------------------
        if person_seen and helmet_ratio > 0.5:
            print("FINAL: HELMET DETECTED ✅")

            field1 = 1
            field2 = 0

        else:
            print("FINAL: NO HELMET ❌")

            field1 = 0
            field2 = 1

        # -------------------------------
        # SEND TO THINGSPEAK
        # -------------------------------
        try:
            requests.get(
                THINGSPEAK_URL,
                params={
                    "api_key": THINGSPEAK_API_KEY,
                    "field1": field1,
                    "field2": field2
                },
                timeout=5
            )

            print("Data sent to ThingSpeak ✅")

        except Exception as e:
            print("⚠ Error:", e)

        break

    # Quit manually
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.03)

# -------------------------------
# CLEAN EXIT
# -------------------------------
cap.release()
cv2.destroyAllWindows()

print("\n--- PROGRAM ENDED ---")