"""
Smart Face Detection + Auto Snapshot System
For Windows laptop built-in webcam.

Features:
    - YuNet face detection
    - Live webcam
    - Latest-frame capture to reduce buffering
    - Automatic snapshot when a face is detected
    - 5-second automatic snapshot cooldown
    - 's' = manual snapshot
    - 'q' = quit

Required model:
    models/face_detection_yunet_2023mar.onnx

Install:
    pip install opencv-python numpy
"""

import cv2
import os
import csv
import time
import threading
from datetime import datetime


# ============================================================================
# CONFIGURATION
# ============================================================================

CAMERA_INDEX = 0

# Built-in laptop camera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# YuNet
CONFIDENCE_THRESHOLD = 0.5

# Automatic snapshot cooldown
SNAPSHOT_COOLDOWN_SECONDS = 5

# Run face detection every N frames.
# 1 = every frame
# 2 = every second frame
DETECTION_INTERVAL = 1

# Files
MODEL_PATH = os.path.join(
    "models",
    "face_detection_yunet_2023mar.onnx"
)

SNAPSHOT_DIR = "snapshots"
LOG_FILE = "detection_log.csv"


# ============================================================================
# FILE SETUP
# ============================================================================

def ensure_files():
    os.makedirs(
        SNAPSHOT_DIR,
        exist_ok=True
    )

    if not os.path.exists(LOG_FILE):

        with open(
            LOG_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "faces_detected",
                "snapshot_file"
            ])


# ============================================================================
# LOGGING
# ============================================================================

def log_detection(
    timestamp,
    face_count,
    filename
):

    with open(
        LOG_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            face_count,
            filename
        ])


# ============================================================================
# SNAPSHOT
# ============================================================================

def save_snapshot(
    frame,
    face_count
):

    now = datetime.now()

    timestamp = now.strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    milliseconds = (
        now.microsecond // 1000
    )

    filename = (
        f"snapshot_"
        f"{timestamp}_"
        f"{milliseconds:03d}_"
        f"{face_count}face(s).jpg"
    )

    filepath = os.path.join(
        SNAPSHOT_DIR,
        filename
    )

    success = cv2.imwrite(
        filepath,
        frame
    )

    if not success:

        print(
            "[ERROR] Could not save snapshot."
        )

        return

    log_detection(
        timestamp,
        face_count,
        filename
    )

    print(
        f"[SNAPSHOT SAVED] {filepath}"
    )


# ============================================================================
# YUNET
# ============================================================================

def create_detector(
    width,
    height
):

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            "\nYuNet model not found.\n\n"
            f"Expected:\n{MODEL_PATH}\n\n"
            "Make sure the ONNX model is inside the "
            "'models' folder."
        )

    print(
        "[INFO] Loading YuNet..."
    )

    detector = cv2.FaceDetectorYN.create(
        model=MODEL_PATH,
        config="",
        input_size=(width, height),
        score_threshold=CONFIDENCE_THRESHOLD,
        nms_threshold=0.3,
        top_k=5000
    )

    print(
        "[INFO] YuNet loaded."
    )

    return detector


# ============================================================================
# FACE DETECTION
# ============================================================================

def detect_faces(
    detector,
    frame
):

    height, width = frame.shape[:2]

    detector.setInputSize(
        (width, height)
    )

    _, faces = detector.detect(
        frame
    )

    results = []

    if faces is None:
        return results

    for face in faces:

        x = int(face[0])
        y = int(face[1])

        w = int(face[2])
        h = int(face[3])

        confidence = float(
            face[14]
        )

        x1 = max(
            0,
            x
        )

        y1 = max(
            0,
            y
        )

        x2 = min(
            width - 1,
            x + w
        )

        y2 = min(
            height - 1,
            y + h
        )

        results.append(
            (
                x1,
                y1,
                x2,
                y2,
                confidence
            )
        )

    return results


# ============================================================================
# LATEST-FRAME CAMERA
# ============================================================================

class LaptopCamera:

    def __init__(
        self,
        camera_index=0
    ):

        self.camera_index = camera_index

        self.cap = None

        self.latest_frame = None

        self.lock = threading.Lock()

        self.running = False

        self.thread = None

    # ------------------------------------------------------------------------
    # START
    # ------------------------------------------------------------------------

    def start(self):

        print(
            "[INFO] Opening built-in laptop camera..."
        )

        # IMPORTANT:
        # Use Microsoft Media Foundation.
        #
        # We deliberately DO NOT force MJPG or YUY2.
        # The built-in camera/Windows driver chooses
        # its native supported format.

        self.cap = cv2.VideoCapture(
            self.camera_index,
            cv2.CAP_MSMF
        )

        if not self.cap.isOpened():

            print(
                "[ERROR] Could not open laptop camera."
            )

            return False

        # ---------------------------------------------------------------
        # Request resolution
        # ---------------------------------------------------------------

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

        # Ask for minimal buffering.
        # MSMF may ignore this; that's okay because
        # our capture thread also prevents old frames
        # from accumulating.
        self.cap.set(
            cv2.CAP_PROP_BUFFERSIZE,
            1
        )

        # ---------------------------------------------------------------
        # Read actual settings
        # ---------------------------------------------------------------

        actual_width = int(
            self.cap.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        actual_height = int(
            self.cap.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        actual_fps = self.cap.get(
            cv2.CAP_PROP_FPS
        )

        print()
        print(
            "=========================================="
        )
        print(
            " LAPTOP CAMERA"
        )
        print(
            "=========================================="
        )

        print(
            f"Resolution : "
            f"{actual_width} x {actual_height}"
        )

        print(
            f"Camera FPS : "
            f"{actual_fps:.1f}"
        )

        print(
            "Backend    : Media Foundation"
        )

        print(
            "Format     : Camera native"
        )

        print(
            "=========================================="
        )
        print()

        # ---------------------------------------------------------------
        # Start capture thread
        # ---------------------------------------------------------------

        self.running = True

        self.thread = threading.Thread(
            target=self.capture_loop,
            daemon=True
        )

        self.thread.start()

        return True

    # ------------------------------------------------------------------------
    # CAPTURE LOOP
    # ------------------------------------------------------------------------

    def capture_loop(self):

        while self.running:

            ret, frame = self.cap.read()

            if not ret:

                time.sleep(
                    0.005
                )

                continue

            # IMPORTANT:
            #
            # Never queue frames.
            #
            # Always replace the old frame with
            # the newest frame.

            with self.lock:

                self.latest_frame = frame

    # ------------------------------------------------------------------------
    # GET LATEST FRAME
    # ------------------------------------------------------------------------

    def get_frame(self):

        with self.lock:

            if self.latest_frame is None:

                return None

            return self.latest_frame.copy()

    # ------------------------------------------------------------------------
    # STOP
    # ------------------------------------------------------------------------

    def stop(self):

        self.running = False

        if self.thread is not None:

            self.thread.join(
                timeout=1
            )

        if self.cap is not None:

            self.cap.release()

        print(
            "[INFO] Camera released."
        )


# ============================================================================
# MAIN
# ============================================================================

def main():

    ensure_files()

    print()
    print(
        "=================================================="
    )
    print(
        " SMART FACE DETECTION"
    )
    print(
        "=================================================="
    )
    print(
        "Camera       : Built-in laptop camera"
    )
    print(
        "Backend      : Media Foundation"
    )
    print(
        "Resolution   : 640x480"
    )
    print(
        "FPS          : 30 requested"
    )
    print()
    print(
        "Controls:"
    )
    print(
        "  q = Quit"
    )
    print(
        "  s = Manual snapshot"
    )
    print(
        "=================================================="
    )
    print()

    # ------------------------------------------------------------------------
    # Camera
    # ------------------------------------------------------------------------

    camera = LaptopCamera(
        CAMERA_INDEX
    )

    if not camera.start():

        print()
        print(
            "Camera could not be opened."
        )

        print(
            "Try CAMERA_INDEX = 1 if necessary."
        )

        return

    # ------------------------------------------------------------------------
    # Wait for first frame
    # ------------------------------------------------------------------------

    print(
        "[INFO] Waiting for first frame..."
    )

    first_frame = None

    for _ in range(100):

        first_frame = camera.get_frame()

        if first_frame is not None:

            break

        time.sleep(
            0.01
        )

    if first_frame is None:

        print(
            "[ERROR] No camera frames received."
        )

        camera.stop()

        return

    # ------------------------------------------------------------------------
    # Actual frame size
    # ------------------------------------------------------------------------

    frame_height, frame_width = (
        first_frame.shape[:2]
    )

    print(
        f"[INFO] Actual image size: "
        f"{frame_width}x{frame_height}"
    )

    # ------------------------------------------------------------------------
    # YuNet
    # ------------------------------------------------------------------------

    try:

        detector = create_detector(
            frame_width,
            frame_height
        )

    except Exception as error:

        print(
            "[ERROR] YuNet could not be loaded."
        )

        print(error)

        camera.stop()

        return

    # ------------------------------------------------------------------------
    # Window
    # ------------------------------------------------------------------------

    window_name = (
        "Smart Face Detection - Laptop Camera"
    )

    cv2.namedWindow(
        window_name,
        cv2.WINDOW_NORMAL
    )

    cv2.resizeWindow(
        window_name,
        960,
        720
    )

    # ------------------------------------------------------------------------
    # Variables
    # ------------------------------------------------------------------------

    frame_number = 0

    last_boxes = []

    last_snapshot_time = 0

    fps_counter = 0

    fps_start = time.time()

    display_fps = 0

    # ------------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------------

    try:

        while True:

            # ---------------------------------------------------------------
            # Get newest frame
            # ---------------------------------------------------------------

            frame = camera.get_frame()

            if frame is None:

                time.sleep(
                    0.005
                )

                continue

            # Keep clean frame for snapshot
            original_frame = frame.copy()

            frame_number += 1

            # ---------------------------------------------------------------
            # Face detection
            # ---------------------------------------------------------------

            if (
                frame_number
                % DETECTION_INTERVAL
                == 0
            ):

                try:

                    last_boxes = detect_faces(
                        detector,
                        frame
                    )

                except cv2.error as error:

                    print(
                        "[WARNING] YuNet error:"
                    )

                    print(error)

                    last_boxes = []

            boxes = last_boxes

            face_count = len(boxes)

            # ---------------------------------------------------------------
            # Display frame
            # ---------------------------------------------------------------

            display_frame = frame.copy()

            # ---------------------------------------------------------------
            # Draw face boxes
            # ---------------------------------------------------------------

            for (
                x1,
                y1,
                x2,
                y2,
                confidence
            ) in boxes:

                cv2.rectangle(
                    display_frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                text = (
                    f"{confidence * 100:.1f}%"
                )

                cv2.putText(
                    display_frame,
                    text,
                    (
                        x1,
                        max(
                            20,
                            y1 - 10
                        )
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

            # ---------------------------------------------------------------
            # Face count
            # ---------------------------------------------------------------

            cv2.putText(
                display_frame,
                f"Faces: {face_count}",
                (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 0),
                2
            )

            # ---------------------------------------------------------------
            # FPS
            # ---------------------------------------------------------------

            fps_counter += 1

            elapsed = (
                time.time()
                - fps_start
            )

            if elapsed >= 1:

                display_fps = (
                    fps_counter
                    / elapsed
                )

                fps_counter = 0

                fps_start = time.time()

            cv2.putText(
                display_frame,
                f"Processing FPS: {display_fps:.1f}",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 255, 255),
                2
            )

            # ---------------------------------------------------------------
            # Face status
            # ---------------------------------------------------------------

            if face_count > 0:

                status = "FACE DETECTED"

                color = (
                    0,
                    255,
                    0
                )

            else:

                status = "NO FACE"

                color = (
                    0,
                    0,
                    255
                )

            cv2.putText(
                display_frame,
                status,
                (10, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                color,
                2
            )

            # ---------------------------------------------------------------
            # Automatic snapshot
            # ---------------------------------------------------------------

            current_time = time.time()

            if (
                face_count > 0
                and
                current_time
                - last_snapshot_time
                >= SNAPSHOT_COOLDOWN_SECONDS
            ):

                print(
                    f"[INFO] Detected "
                    f"{face_count} face(s)."
                )

                save_snapshot(
                    original_frame,
                    face_count
                )

                last_snapshot_time = (
                    current_time
                )

            # ---------------------------------------------------------------
            # Display
            # ---------------------------------------------------------------

            cv2.imshow(
                window_name,
                display_frame
            )

            # ---------------------------------------------------------------
            # Keyboard
            # ---------------------------------------------------------------

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):

                print(
                    "[INFO] Quit."
                )

                break

            elif key == ord("s"):

                print(
                    "[INFO] Manual snapshot."
                )

                save_snapshot(
                    original_frame,
                    face_count
                )

                last_snapshot_time = (
                    current_time
                )

    except KeyboardInterrupt:

        print(
            "[INFO] Program interrupted."
        )

    finally:

        camera.stop()

        cv2.destroyAllWindows()

        print(
            "[INFO] Program finished."
        )


# ============================================================================
# START PROGRAM
# ============================================================================

if __name__ == "__main__":
    main()