"""
download_models.py
-------------------
One-time setup script. Downloads the pre-trained YuNet face detection
model (ONNX format) from the official OpenCV Model Zoo.

Run this ONCE before running smart_face_detection.py:
    python download_models.py

This will create a 'models' folder containing:
    - face_detection_yunet_2023mar.onnx   (trained weights, ~340 KB)

Note: as of OpenCV 5.0 (June 2026), the old Caffe-based face detector
model can no longer be loaded (OpenCV dropped its Caffe/Darknet loaders
in favor of ONNX). YuNet is OpenCV's current recommended DNN face
detector and is both smaller and more accurate than the old model.
"""

import os
import urllib.request

MODEL_DIR = "models"

FILES = {
    "face_detection_yunet_2023mar.onnx": (
        "https://github.com/opencv/opencv_zoo/raw/main/models/"
        "face_detection_yunet/face_detection_yunet_2023mar.onnx"
    ),
}


def download():
    os.makedirs(MODEL_DIR, exist_ok=True)

    for filename, url in FILES.items():
        dest_path = os.path.join(MODEL_DIR, filename)

        if os.path.exists(dest_path):
            print(f"[SKIP] {filename} already exists.")
            continue

        print(f"[DOWNLOADING] {filename} ...")
        try:
            urllib.request.urlretrieve(url, dest_path)
            print(f"[DONE] Saved to {dest_path}")
        except Exception as e:
            print(f"[ERROR] Could not download {filename}: {e}")
            print("        Please download it manually from the URL above "
                  "and place it inside the 'models' folder.")

    print("\nSetup check complete. If both files show [DONE] or [SKIP], "
          "you're ready to run smart_face_detection.py")


if __name__ == "__main__":
    download()
