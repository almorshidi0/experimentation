"""
PiCamera Module
===============

This module provides a simple interface to initialize the PiCamera and capture images using the `picamera2` library.

Classes:
--------
- PiCameraController: A class to manage the PiCamera initialization and image capture.

Example Usage:
--------------
To use this module, create an instance of `PiCameraController` and call its methods.

    from picamera_module import PiCameraController

    camera_controller = PiCameraController()
    camera_controller.pi_cam_init()
    camera_controller.get_img("example_image")

To test this module, you can run it directly as a script. It will initialize the camera and capture 10 images named 'test_0.jpg' to 'test_9.jpg'.

    $ python3 picamera_module.py

Dependencies:
-------------
- picamera2: Ensure that the `picamera2` library is installed and properly configured on your system.

Note:
-----
This script is intended to run on a Raspberry Pi with a connected camera module.
"""

from picamera2 import Picamera2

class PiCameraController:
    def __init__(self):
        """
        Initialize the PiCameraController class.
        """
        self.pi_cam = None

    def pi_cam_init(self):
        """
        Initialize and start the PiCamera.

        This method sets up the `pi_cam` attribute and starts the camera.
        
        Args:
        None
        
        Returns:
        None
        """
        self.pi_cam = Picamera2()
        self.pi_cam.start()

    def get_img(self, file_name):
        """
        Capture an image and save it with the provided file name.

        Args:
        file_name (str): The name to save the image file as, without file extension.
        
        Returns:
        None
        """
        self.pi_cam.capture_file(f"{file_name}.jpg")

def main():
    """
    Main function for module testing.

    This function creates an instance of `PiCameraController`, initializes the camera, and
    then captures 10 images sequentially, saving them as 'test_0.jpg' to 'test_9.jpg'.
    
    This function is intended for testing purposes and should not be used
    when the module is imported elsewhere.
    
    Args:
    None
    
    Returns:
    None
    """
    camera_controller = PiCameraController()
    camera_controller.pi_cam_init()
    count = 0 
    while count < 10:
        camera_controller.get_img(f"test_{count}")
        count += 1

if __name__ == '__main__':
    main()
