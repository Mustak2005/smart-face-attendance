# Smart Face Detection and Auto Snapshot System

A Python project that uses a pre-trained deep learning model (via OpenCV's
DNN module) to detect human faces from a live webcam feed and automatically
save timestamped snapshots when a face is detected.

## How it works

1. Each webcam frame is passed through **YuNet**, OpenCV's official
   pre-trained deep learning face detector (ONNX format, run via
   `cv2.FaceDetectorYN`).
2. The model outputs bounding boxes with confidence scores for any detected
   faces.
3. If a face is detected and the cooldown period has passed (default: 5
   seconds), the system automatically saves a snapshot to the `snapshots/`
   folder and logs the event (timestamp, number of faces, filename) to
   `detection_log.csv`.
4. You can also press `s` at any time to force a manual snapshot.

## Why a DNN model instead of Haar Cascades?

Haar Cascades (the classic OpenCV method) are fast but struggle with side
angles, poor lighting, and partial occlusion. YuNet is a genuine deep
learning model, is significantly more accurate, and still runs smoothly in
real time on a normal laptop CPU (no GPU required).

> **Note on OpenCV versions:** OpenCV released a major version 5.0 in June
> 2026 that removed support for loading the older Caffe-format DNN models
> from the `dnn` module. This project uses YuNet (ONNX format), which
> works on both OpenCV 4.x and 5.x, so you don't need to worry about which
> version `pip` installs for you.

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download the pre-trained model file (one-time step):**
   ```bash
   python download_models.py
   ```
   This creates a `models/` folder with:
   - `face_detection_yunet_2023mar.onnx`

   If the automatic download fails (e.g. blocked network), download the
   file manually from the URL printed by the script and place it in
   the `models/` folder.

3. **Run the main program:**
   ```bash
   python smart_face_detection.py
   ```

4. **Controls:**
   - `q` — quit
   - `s` — take a manual snapshot immediately

## Output

- `snapshots/` — folder containing saved JPG images, named like
  `snapshot_2026-08-07_14-32-05_1face(s).jpg`
- `detection_log.csv` — a log of every snapshot event with timestamp and
  face count (useful for a report, or to plug into an attendance sheet)

## Possible Extensions (for a stronger project / viva)

- **Face Recognition:** add the `face_recognition` library to identify
  *who* was detected (not just that a face was present) — great for
  turning this into an attendance system.
- **Email/SMS Alerts:** trigger a notification when an unknown face is
  detected (security use case).
- **GUI Dashboard:** build a simple Tkinter or Streamlit interface to view
  snapshots and logs without touching the terminal.
- **Multi-camera support:** loop over multiple `CAMERA_INDEX` values.

## Project Structure

```
smart_face_project/
├── smart_face_detection.py   # main program
├── download_models.py        # one-time model downloader
├── requirements.txt
├── README.md
├── models/                   # created after running download_models.py
│   └── face_detection_yunet_2023mar.onnx
├── snapshots/                # auto-created; stores captured images
└── detection_log.csv         # auto-created; log of detections
```
