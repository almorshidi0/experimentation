"""
Camera Module
====================

This module provides a simple interface to capture images using OpenCV (`cv2` library).

Classes:
--------
- CameraController: A class to manage the OpenCV camera initialization and image capture.

Example Usage:
--------------
To use this module, create an instance of `CameraController` and call its methods.

    from camera_module import CameraController

    camera_controller = CameraController()
    camera_controller.init_camera()
    camera_controller.get_img("example_image")

To test this module, you can run it directly as a script. It will initialize the camera and capture 10 images named 'test_0.jpg' to 'test_9.jpg'.

    $ python opencv_camera_module.py

Dependencies:
-------------
- cv2: Ensure that the `cv2` library is installed and properly configured on your system.

Note:
-----
This script is intended to run on a system where OpenCV (`cv2`) is installed and a compatible camera is available.
"""

import cv2

class CameraController:
    def __init__(self):
        """
        Initialize the CameraController class.
        """
        self.camera = None

    def init_camera(self):
        """
        Initialize the camera.

        This method sets up the camera attribute and starts the camera.

        Args:
        None

        Returns:
        None
        """
        self.camera = cv2.VideoCapture(0)

    def get_img(self, file_name, size=None):
        """
        Capture an image and optionally save it with the provided file name.

        Args:
        file_name (str): The name to save the image file as, without file extension.
        size (tuple): Optional tuple specifying the desired width and height of the image (width, height).
        return_image (bool): Optional flag to return the captured image as an array instead of saving it.

        Returns:
        None or np.ndarray: If `return_image` is True, returns the captured image as a NumPy array.
        """
        ret, frame = self.camera.read()
        if size is not None:
            frame = cv2.resize(frame, size)
        cv2.imwrite(f"{file_name}.jpg", frame)

        return frame

    def release_camera(self):
        """
        Release the camera resource.

        Args:
        None

        Returns:
        None
        """
        self.camera.release()

def main():
    """
    Main function for module testing.

    This function creates an instance of `CameraController`, initializes the camera, and
    then captures 10 images sequentially, saving them as 'test_0.jpg' to 'test_9.jpg'.

    This function is intended for testing purposes and should not be used
    when the module is imported elsewhere.

    Args:
    None

    Returns:
    None
    """
    camera_controller = CameraController()
    camera_controller.init_camera()
    count = 0 
    while count < 10:
        camera_controller.get_img(f"test_{count}", size=[240, 120])
        count += 1
    camera_controller.release_camera()

if __name__ == '__main__':
    main()
