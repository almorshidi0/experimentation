"""
Autonomous Car Controller
=========================

This script controls an autonomous car's movement using a pre-trained model to predict speed and steering angle from camera input.

It initializes modules for controlling the DC motors and the camera module for image capture.
The script continuously captures images, processes them, and uses a machine learning model to predict the speed and steering angle to control the car's movement.

Modules:
--------
- dc_motors_module: Controls the car's DC motors for movement.
- camera_module: Provides an interface for capturing images.

Global Variables:
-----------------
- motor: Instance of DcMotorController to control the motors.
- camera: Instance of CameraController to capture images.
- model: Pre-trained machine learning model for speed and angle prediction.

Functions:
----------
- preProcess(img): Preprocess the captured image for the model.
- main(): Main function to capture images, predict speed and angle, and control the car's movement.

Example Usage:
--------------
To run the script, ensure the required modules (dc_motors_module, camera_module) are imported and available in the environment.

    $ python autonomous_car_controller.py

Dependencies:
-------------
- dc_motors_module: Ensure that the `dc_motors_module` module is properly implemented and available.
- camera_module: Ensure that the `camera_module` module is properly implemented and available.

Note:
-----
This script is designed to control an autonomous car system and requires proper hardware setup and configuration.
"""

# Importing necessary modules
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from dc_motors_module import DcMotorController
from camera_module import CameraController

# Initializing modules
motor = DcMotorController(17, 27, 22, 25, 23, 24)  # Pin Numbers
camera = CameraController()

model = load_model('/home/pi/Desktop/My Files/RpiRobot/model_V1.h5')

def preProcess(img):
    """
    Preprocess the captured image for the model.

    Args:
        img (numpy.ndarray): The input image.

    Returns:
        numpy.ndarray: Preprocessed image.
    """
    img = img[54:120, :, :]  # Crop the image
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)  # Convert to YUV color space
    img = cv2.GaussianBlur(img, (3, 3), 0)  # Apply Gaussian blur
    img = cv2.resize(img, (200, 66))  # Resize the image
    img = img / 255.0  # Normalize the image
    return img

def main():
    """
    Main function to capture images, predict speed and angle, and control the car's movement.

    This function continuously captures images, processes them, and uses a pre-trained model to predict the speed and steering angle to control the car's movement.
    """
    camera.init_camera()  # Initialize the camera
    while True:
        img = camera.get_img("road_image", size=[240, 120])  # Capture image
        img = np.asarray(img)  # Convert to numpy array
        img = preProcess(img)  # Preprocess the image
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        prediction = model.predict(img)  # Predict angle and speed
        speed = float(prediction[0][0])  # Extract speed
        angle = float(prediction[0][1])  # Extract angle

        print(f"Speed: {speed}, Angle: {angle}")  # Print values
        motor.move_forward(speed, angle)  # Control motors
        cv2.waitKey(1)  # Wait for 1 ms

if __name__ == "__main__":
    main()
