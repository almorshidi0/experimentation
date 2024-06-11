import cv2

def test_camera():
    camera = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Using V4L2 backend
    if not camera.isOpened():
        raise RuntimeError("Error: Camera could not be opened.")
    print("Camera successfully initialized.")

    ret, frame = camera.read()
    if not ret:
        raise RuntimeError("Error: Could not read frame from camera.")
    if frame is None or frame.size == 0:
        raise RuntimeError("Error: Captured frame is empty.")

    cv2.imwrite("test_image.jpg", frame)
    print("Image saved as test_image.jpg")

    camera.release()
    print("Camera released.")

if __name__ == "__main__":
    try:
        test_camera()
    except RuntimeError as e:
        print(e)
