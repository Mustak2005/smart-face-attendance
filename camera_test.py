import cv2
import time

CAMERA_INDEX = 0

WIDTH = 640
HEIGHT = 480
FPS = 30


print("Starting camera test...")
print("Press Q to quit.")

# ============================================================
# Open camera
# ============================================================

cap = cv2.VideoCapture(
    CAMERA_INDEX,
    cv2.CAP_DSHOW
)

if not cap.isOpened():
    print("ERROR: Could not open camera.")
    exit()


# ============================================================
# Force MJPG
# ============================================================

print("Setting MJPG...")

cap.set(
    cv2.CAP_PROP_FOURCC,
    cv2.VideoWriter_fourcc(*"MJPG")
)

cap.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    WIDTH
)

cap.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    HEIGHT
)

cap.set(
    cv2.CAP_PROP_FPS,
    FPS
)

cap.set(
    cv2.CAP_PROP_BUFFERSIZE,
    1
)


# ============================================================
# Print what camera actually accepted
# ============================================================

actual_width = cap.get(
    cv2.CAP_PROP_FRAME_WIDTH
)

actual_height = cap.get(
    cv2.CAP_PROP_FRAME_HEIGHT
)

actual_fps = cap.get(
    cv2.CAP_PROP_FPS
)

fourcc = int(
    cap.get(cv2.CAP_PROP_FOURCC)
)

fourcc_string = "".join(
    [
        chr((fourcc >> 0) & 0xFF),
        chr((fourcc >> 8) & 0xFF),
        chr((fourcc >> 16) & 0xFF),
        chr((fourcc >> 24) & 0xFF),
    ]
)


print()
print("================================")
print("CAMERA CONFIGURATION")
print("================================")
print(
    f"Resolution : {actual_width} x {actual_height}"
)
print(
    f"FPS        : {actual_fps}"
)
print(
    f"FOURCC     : {fourcc_string}"
)
print("================================")
print()


# ============================================================
# Warm up camera
# ============================================================

for i in range(20):

    ret, frame = cap.read()

    if not ret:
        print("Warmup frame failed.")

    time.sleep(0.03)


# ============================================================
# Camera loop
# ============================================================

while True:

    ret, frame = cap.read()

    if not ret or frame is None:

        print("ERROR: Failed to read frame.")

        continue


    # --------------------------------------------------------
    # Display actual camera frame
    # --------------------------------------------------------

    cv2.imshow(
        "RAW CAMERA TEST",
        frame
    )


    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# ============================================================
# Cleanup
# ============================================================

cap.release()

cv2.destroyAllWindows()

print("Camera test finished.")