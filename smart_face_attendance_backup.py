"""
SMART FACE RECOGNITION ATTENDANCE SYSTEM
Uses:
- YuNet for face detection
- SFace for face recognition
- Camera registration (no manual photo copying)
- Daily duplicate-attendance prevention
- CSV attendance file
"""

import cv2
import os
import csv
import json
import time
import threading
import numpy as np
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

CONFIDENCE_THRESHOLD = 0.5
DETECTION_INTERVAL = 1

# SFace cosine similarity threshold.
# Higher = stricter matching.
RECOGNITION_THRESHOLD = 0.363

# Number of camera samples used during registration.
REGISTRATION_SAMPLES = 5

MODEL_PATH = os.path.join(
    BASE_DIR, "models", "face_detection_yunet_2023mar.onnx"
)

RECOGNITION_MODEL_PATH = os.path.join(
    BASE_DIR, "models", "face_recognition_sface_2021dec.onnx"
)

DATA_DIR = os.path.join(BASE_DIR, "data")
REGISTRATION_FILE = os.path.join(DATA_DIR, "registered_faces.json")
ATTENDANCE_FILE = os.path.join(BASE_DIR, "attendance.csv")


# ============================================================
# FILE SETUP
# ============================================================

def ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(REGISTRATION_FILE):
        with open(REGISTRATION_FILE, "w", encoding="utf-8") as file:
            json.dump({"people": []}, file, indent=4)

    if not os.path.exists(ATTENDANCE_FILE):
        with open(
            ATTENDANCE_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow([
                "Student ID",
                "Name",
                "Date",
                "Time",
                "Status"
            ])


# ============================================================
# REGISTRATION DATA
# ============================================================

def load_registered_people():
    ensure_files()

    try:
        with open(REGISTRATION_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        people = data.get("people", [])

        # Convert saved feature lists back to NumPy arrays.
        for person in people:
            person["feature"] = np.array(
                person["feature"],
                dtype=np.float32
            ).reshape(1, -1)

        return people

    except (json.JSONDecodeError, KeyError, ValueError):
        print("[ERROR] registered_faces.json is invalid.")
        return []


def save_registered_people(people):
    os.makedirs(DATA_DIR, exist_ok=True)

    clean_people = []

    for person in people:
        feature = person["feature"]

        clean_people.append({
            "student_id": person["student_id"],
            "name": person["name"],
            "feature": feature.flatten().astype(float).tolist()
        })

    with open(
        REGISTRATION_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            {"people": clean_people},
            file,
            indent=4
        )


# ============================================================
# MODELS
# ============================================================

def create_detector(width, height):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"YuNet model not found:\n{MODEL_PATH}"
        )

    print("[INFO] Loading YuNet...")

    detector = cv2.FaceDetectorYN.create(
        model=MODEL_PATH,
        config="",
        input_size=(width, height),
        score_threshold=CONFIDENCE_THRESHOLD,
        nms_threshold=0.3,
        top_k=5000
    )

    print("[INFO] YuNet loaded.")
    return detector


def create_recognizer():
    if not os.path.exists(RECOGNITION_MODEL_PATH):
        raise FileNotFoundError(
            "SFace model not found:\n"
            f"{RECOGNITION_MODEL_PATH}\n\n"
            "Make sure face_recognition_sface_2021dec.onnx "
            "is inside the models folder."
        )

    print("[INFO] Loading SFace...")

    recognizer = cv2.FaceRecognizerSF.create(
        RECOGNITION_MODEL_PATH,
        ""
    )

    print("[INFO] SFace loaded.")
    return recognizer


# ============================================================
# FACE DETECTION
# ============================================================

def detect_faces(detector, frame):
    height, width = frame.shape[:2]

    detector.setInputSize((width, height))

    _, faces = detector.detect(frame)

    results = []

    if faces is None:
        return results

    for face in faces:
        x = int(face[0])
        y = int(face[1])
        w = int(face[2])
        h = int(face[3])
        confidence = float(face[14])

        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(width - 1, x + w)
        y2 = min(height - 1, y + h)

        results.append({
            "box": (x1, y1, x2, y2),
            "confidence": confidence,
            "raw": face
        })

    return results


# ============================================================
# CAMERA
# ============================================================

class LaptopCamera:

    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.latest_frame = None
        self.lock = threading.Lock()
        self.running = False
        self.thread = None

    def start(self):
        print("[INFO] Opening built-in laptop camera...")

        self.cap = cv2.VideoCapture(
            self.camera_index,
            cv2.CAP_MSMF
        )

        if not self.cap.isOpened():
            print("[ERROR] Could not open laptop camera.")
            return False

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            CAMERA_WIDTH
        )
        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            CAMERA_HEIGHT
        )
        self.cap.set(
            cv2.CAP_PROP_FPS,
            CAMERA_FPS
        )
        self.cap.set(
            cv2.CAP_PROP_BUFFERSIZE,
            1
        )

        actual_width = int(
            self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        )
        actual_height = int(
            self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )
        actual_fps = self.cap.get(cv2.CAP_PROP_FPS)

        print()
        print("==========================================")
        print(" LAPTOP CAMERA")
        print("==========================================")
        print(f"Resolution : {actual_width} x {actual_height}")
        print(f"Camera FPS : {actual_fps:.1f}")
        print("Backend    : Media Foundation")
        print("==========================================")
        print()

        self.running = True

        self.thread = threading.Thread(
            target=self.capture_loop,
            daemon=True
        )
        self.thread.start()

        return True

    def capture_loop(self):
        while self.running:
            ret, frame = self.cap.read()

            if not ret:
                time.sleep(0.005)
                continue

            with self.lock:
                self.latest_frame = frame

    def get_frame(self):
        with self.lock:
            if self.latest_frame is None:
                return None

            return self.latest_frame.copy()

    def stop(self):
        self.running = False

        if self.thread is not None:
            self.thread.join(timeout=1)

        if self.cap is not None:
            self.cap.release()

        print("[INFO] Camera released.")


# ============================================================
# CAMERA START HELPER
# ============================================================

def start_camera_and_models():
    camera = LaptopCamera(CAMERA_INDEX)

    if not camera.start():
        print("Camera could not be opened.")
        print("Try CAMERA_INDEX = 1 if necessary.")
        return None, None, None

    print("[INFO] Waiting for first camera frame...")

    first_frame = None

    for _ in range(100):
        first_frame = camera.get_frame()

        if first_frame is not None:
            break

        time.sleep(0.01)

    if first_frame is None:
        print("[ERROR] No camera frames received.")
        camera.stop()
        return None, None, None

    height, width = first_frame.shape[:2]

    try:
        detector = create_detector(width, height)
        recognizer = create_recognizer()
    except Exception as error:
        print("[ERROR] Could not load models.")
        print(error)
        camera.stop()
        return None, None, None

    return camera, detector, recognizer


# ============================================================
# FEATURE EXTRACTION
# ============================================================

def extract_feature(recognizer, frame, face):
    try:
        aligned = recognizer.alignCrop(
            frame,
            face["raw"]
        )

        feature = recognizer.feature(aligned)

        if feature is None:
            return None

        feature = np.asarray(
            feature,
            dtype=np.float32
        ).reshape(1, -1)

        return feature

    except cv2.error:
        return None


def average_features(features):
    if not features:
        return None

    combined = np.vstack(features)

    average = np.mean(
        combined,
        axis=0,
        keepdims=True
    ).astype(np.float32)

    # Normalize the average feature.
    norm = np.linalg.norm(average)

    if norm > 0:
        average = average / norm

    return average


# ============================================================
# REGISTER NEW PERSON
# ============================================================

def register_person():
    print()
    print("==========================================")
    print(" REGISTER NEW PERSON")
    print("==========================================")

    student_id = input("Enter Student ID: ").strip()

    if not student_id:
        print("[ERROR] Student ID cannot be empty.")
        return

    name = input("Enter Name: ").strip()

    if not name:
        print("[ERROR] Name cannot be empty.")
        return

    people = load_registered_people()

    for person in people:
        if person["student_id"].lower() == student_id.lower():
            print("[ERROR] This Student ID is already registered.")
            return

    print()
    print("Camera registration instructions:")
    print("1. Sit in front of the camera.")
    print("2. Keep only ONE face visible.")
    print("3. Look toward the camera.")
    print("4. Move your head slightly between samples.")
    print("5. Press Q to cancel.")
    print()
    input("Press ENTER to open the camera...")

    camera, detector, recognizer = start_camera_and_models()

    if camera is None:
        return

    window_name = "Register New Person - Smart Attendance"

    cv2.namedWindow(
        window_name,
        cv2.WINDOW_NORMAL
    )
    cv2.resizeWindow(
        window_name,
        960,
        720
    )

    features = []
    last_capture_time = 0
    capture_delay = 0.6
    frame_number = 0

    try:
        while len(features) < REGISTRATION_SAMPLES:
            frame = camera.get_frame()

            if frame is None:
                continue

            frame_number += 1

            try:
                faces = detect_faces(
                    detector,
                    frame
                )
            except cv2.error:
                faces = []

            display = frame.copy()

            for face in faces:
                x1, y1, x2, y2 = face["box"]

                cv2.rectangle(
                    display,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    display,
                    f"{face['confidence'] * 100:.1f}%",
                    (x1, max(20, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

            cv2.putText(
                display,
                f"Samples: {len(features)}/{REGISTRATION_SAMPLES}",
                (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            if len(faces) == 0:
                message = "Show your face to the camera"
            elif len(faces) > 1:
                message = "Only ONE face should be visible"
            else:
                message = "Face detected - hold still"

                now = time.time()

                if now - last_capture_time >= capture_delay:
                    feature = extract_feature(
                        recognizer,
                        frame,
                        faces[0]
                    )

                    if feature is not None:
                        features.append(feature)
                        last_capture_time = now

                        print(
                            f"[INFO] Captured sample "
                            f"{len(features)}/{REGISTRATION_SAMPLES}"
                        )

            cv2.putText(
                display,
                message,
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 255, 255),
                2
            )

            cv2.putText(
                display,
                "Q = Cancel",
                (10, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            cv2.imshow(
                window_name,
                display
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                print("[INFO] Registration cancelled.")
                return

        final_feature = average_features(features)

        if final_feature is None:
            print("[ERROR] Could not create face feature.")
            return

        people.append({
            "student_id": student_id,
            "name": name,
            "feature": final_feature
        })

        save_registered_people(people)

        print()
        print("==========================================")
        print(" REGISTRATION SUCCESSFUL")
        print("==========================================")
        print(f"Student ID : {student_id}")
        print(f"Name       : {name}")
        print("Face data  : Saved as feature data")
        print("Photo      : NOT required")
        print("==========================================")

    finally:
        camera.stop()
        cv2.destroyAllWindows()


# ============================================================
# FACE RECOGNITION
# ============================================================

def recognize_face(recognizer, feature, people):
    if feature is None or not people:
        return None, 0.0

    best_person = None
    best_score = -1.0

    for person in people:
        stored_feature = person["feature"]

        try:
            score = float(
                recognizer.match(
                    feature,
                    stored_feature,
                    cv2.FaceRecognizerSF_FR_COSINE
                )
            )
        except cv2.error:
            continue

        if score > best_score:
            best_score = score
            best_person = person

    if best_person is not None and best_score >= RECOGNITION_THRESHOLD:
        return best_person, best_score

    return None, best_score


# ============================================================
# ATTENDANCE
# ============================================================

def already_marked_today(student_id):
    today = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(ATTENDANCE_FILE):
        return False

    with open(
        ATTENDANCE_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if (
                row.get("Student ID", "").strip().lower()
                == student_id.strip().lower()
                and row.get("Date", "").strip() == today
            ):
                return True

    return False


def mark_attendance(person):
    student_id = person["student_id"]
    name = person["name"]

    if already_marked_today(student_id):
        return False

    now = datetime.now()

    with open(
        ATTENDANCE_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            student_id,
            name,
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            "Present"
        ])

    print(
        f"[ATTENDANCE] {student_id} - {name} marked PRESENT."
    )

    return True


# ============================================================
# START ATTENDANCE
# ============================================================

def start_attendance():
    people = load_registered_people()

    if not people:
        print()
        print("[INFO] No registered people found.")
        print("Please choose option 1 and register a person first.")
        return

    print()
    print("==========================================")
    print(" START ATTENDANCE")
    print("==========================================")
    print(f"Registered people: {len(people)}")
    print("Press Q to stop attendance.")
    print()

    camera, detector, recognizer = start_camera_and_models()

    if camera is None:
        return

    window_name = "Smart Face Recognition Attendance"

    cv2.namedWindow(
        window_name,
        cv2.WINDOW_NORMAL
    )
    cv2.resizeWindow(
        window_name,
        960,
        720
    )

    frame_number = 0
    last_faces = []

    # Prevent the same person from being processed continuously.
    last_recognition_time = {}

    try:
        while True:
            frame = camera.get_frame()

            if frame is None:
                time.sleep(0.005)
                continue

            frame_number += 1

            if frame_number % DETECTION_INTERVAL == 0:
                try:
                    last_faces = detect_faces(
                        detector,
                        frame
                    )
                except cv2.error:
                    last_faces = []

            display = frame.copy()

            for face in last_faces:
                x1, y1, x2, y2 = face["box"]

                feature = extract_feature(
                    recognizer,
                    frame,
                    face
                )

                person, score = recognize_face(
                    recognizer,
                    feature,
                    people
                )

                if person is not None:
                    student_id = person["student_id"]
                    name = person["name"]

                    current_time = time.time()

                    # Try marking only once every 2 seconds
                    # for the same recognized person.
                    previous_time = last_recognition_time.get(
                        student_id,
                        0
                    )

                    if current_time - previous_time >= 2:
                        mark_attendance(person)
                        last_recognition_time[student_id] = current_time

                    box_color = (0, 255, 0)

                    label = (
                        f"{name} | {student_id}"
                    )

                    score_text = (
                        f"Match: {score:.2f}"
                    )

                else:
                    box_color = (0, 0, 255)

                    label = "Unknown Person"

                    score_text = (
                        f"Match: {score:.2f}"
                        if score >= 0
                        else "No match"
                    )

                cv2.rectangle(
                    display,
                    (x1, y1),
                    (x2, y2),
                    box_color,
                    2
                )

                cv2.putText(
                    display,
                    label,
                    (x1, max(25, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    box_color,
                    2
                )

                cv2.putText(
                    display,
                    score_text,
                    (x1, min(display.shape[0] - 10, y2 + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    box_color,
                    2
                )

            cv2.putText(
                display,
                f"Faces detected: {len(last_faces)}",
                (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                2
            )

            cv2.putText(
                display,
                "Smart Attendance | Q = Quit",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

            cv2.imshow(
                window_name,
                display
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    except KeyboardInterrupt:
        print("[INFO] Attendance interrupted.")

    finally:
        camera.stop()
        cv2.destroyAllWindows()
        print("[INFO] Attendance session finished.")


# ============================================================
# VIEW TODAY'S ATTENDANCE
# ============================================================

def view_today_attendance():
    today = datetime.now().strftime("%Y-%m-%d")

    print()
    print("==========================================")
    print(f" TODAY'S ATTENDANCE - {today}")
    print("==========================================")

    if not os.path.exists(ATTENDANCE_FILE):
        print("No attendance records found.")
        return

    records = []

    with open(
        ATTENDANCE_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row.get("Date", "").strip() == today:
                records.append(row)

    if not records:
        print("No attendance marked today.")
        return

    print(
        f"{'Student ID':<15}"
        f"{'Name':<25}"
        f"{'Time':<12}"
        f"Status"
    )
    print("-" * 65)

    for row in records:
        print(
            f"{row.get('Student ID', ''):<15}"
            f"{row.get('Name', ''):<25}"
            f"{row.get('Time', ''):<12}"
            f"{row.get('Status', '')}"
        )

    print()
    print(f"Total Present: {len(records)}")


# ============================================================
# MAIN MENU
# ============================================================

def show_menu():
    while True:
        print()
        print("==================================================")
        print("       SMART FACE RECOGNITION ATTENDANCE")
        print("==================================================")
        print("1. Register New Person")
        print("2. Start Attendance")
        print("3. View Today's Attendance")
        print("4. Exit")
        print("==================================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_person()

        elif choice == "2":
            start_attendance()

        elif choice == "3":
            view_today_attendance()

        elif choice == "4":
            print("[INFO] Exiting program.")
            break

        else:
            print("[ERROR] Invalid choice. Enter 1, 2, 3 or 4.")


# ============================================================
# START PROGRAM
# ============================================================

def main():
    ensure_files()

    print()
    print("==================================================")
    print(" SMART FACE RECOGNITION ATTENDANCE SYSTEM")
    print("==================================================")
    print("YuNet  : Face Detection")
    print("SFace  : Face Recognition")
    print("Storage: JSON feature data + CSV attendance")
    print("==================================================")

    show_menu()


if __name__ == "__main__":
    main()
