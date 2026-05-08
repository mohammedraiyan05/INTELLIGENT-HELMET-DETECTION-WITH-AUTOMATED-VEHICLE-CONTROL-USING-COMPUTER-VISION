import cv2
import time
import serial
from ultralytics import YOLO

# -------------------------------
# 1. Load Model
# -------------------------------
model = YOLO('best.pt')

# -------------------------------
# 2. Arduino Serial Connection
# -------------------------------
arduino = serial.Serial('COM6', 9600)   # Change if needed
time.sleep(2)

# -------------------------------
# 3. Class IDs
# -------------------------------
SAFE_IDS = [0, 1, 2, 3, 4, 8, 11, 12]
PERSON_ID = 9

# -------------------------------
# 4. Config
# -------------------------------
NO_HELMET_WAIT = 10  # seconds

# -------------------------------
# 5. Camera Start
# -------------------------------
cap = cv2.VideoCapture(0)

print("\n--- SYSTEM READY ---")

start_time = None
timer_started = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(frame, conf=0.25, verbose=False)
    detected_ids = results[0].boxes.cls.tolist()

    person_in_frame = PERSON_ID in detected_ids
    helmet_detected = any(hid in detected_ids for hid in SAFE_IDS)

    # 🟢 Start timer ONLY ONCE
    if person_in_frame and not timer_started:
        start_time = time.time()
        timer_started = True
        print("Person detected → Timer started (10s)")

    if timer_started:
        elapsed = time.time() - start_time
        remaining = max(0, int(NO_HELMET_WAIT - elapsed))

        # ✅ Helmet detected anytime → send immediately
        if helmet_detected:
            print("HELMET DETECTED ✅")
            arduino.write(b'1')

            annotated = results[0].plot()
            cv2.putText(annotated, "HELMET DETECTED",
                        (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0), 3)

            cv2.imshow("Helmet Detection", annotated)
            time.sleep(2)
            break

        # ⏱ Timer display (even if person temporarily lost)
        annotated = results[0].plot()
        cv2.putText(annotated,
                    f"NO HELMET - {remaining}s",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255), 2)

        cv2.imshow("Helmet Detection", annotated)

        # ❌ If time finished → send NO helmet
        if elapsed >= NO_HELMET_WAIT:
            print("FINAL: NO HELMET ❌")
            arduino.write(b'0')
            time.sleep(2)
            break

    else:
        # Before detection starts
        cv2.putText(frame, "SCANNING...",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255), 2)

        cv2.imshow("Helmet Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -------------------------------
# CLEAN EXIT
# -------------------------------
cap.release()
cv2.destroyAllWindows()
arduino.close()

print("\n--- PROGRAM ENDED ---")