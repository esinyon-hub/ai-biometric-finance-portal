import cv2
import os
import numpy as np
import time

DATA_DIR = "portal/face_data"
os.makedirs(DATA_DIR, exist_ok=True)

# --- CAPTURE FACE ---
def capture_face(username):
    cap = cv2.VideoCapture(0)
    print("Position your face... capturing automatically for 5 seconds.")

    start_time = time.time()
    captured_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        captured_frame = frame.copy()

        # countdown overlay
        elapsed = time.time() - start_time
        remaining = max(0, 5 - int(elapsed))
        status_text = f"Capturing your face... {remaining}s left"
        cv2.putText(frame, status_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Capture Face", frame)

        if elapsed > 5:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if captured_frame is not None:
        path = os.path.join(DATA_DIR, f"{username}.png")
        cv2.imwrite(path, captured_frame)
        print(f"Face saved ✅ at {path}")
        return path
    else:
        print("Failed to capture face!")
        return None


# --- COMPARE FACES ---
def compare_faces(username):
    known_path = os.path.join(DATA_DIR, f"{username}.png")
    if not os.path.exists(known_path):
        print("No registered face found!")
        return False

    known_img = cv2.imread(known_path, 0)
    known_img = cv2.resize(known_img, (200, 200))

    cap = cv2.VideoCapture(0)
    print("Scanning live face for 5 seconds...")

    motion_counter = 0
    prev_frame = None
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        small = cv2.resize(gray, (200, 200))

        # face match by simple difference
        diff = np.mean(cv2.absdiff(known_img, small))
        matched = diff < 3000  # threshold — tune this

        # basic liveness: head movement
        if prev_frame is not None:
            motion = np.mean(np.abs(prev_frame - gray))
            if motion > 500:
                motion_counter += 1
        prev_frame = gray.copy()

        # countdown overlay
        elapsed = time.time() - start_time
        remaining = max(0, 5 - int(elapsed))
        status_text = f"Scanning... {remaining}s left"
        if matched:
            status_text += " | Face looks similar"
        cv2.putText(frame, status_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Login - scanning...", frame)

        if elapsed > 5:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print(f"Face matched: {matched}, Motion detected: {motion_counter}")
    return matched and motion_counter > 5