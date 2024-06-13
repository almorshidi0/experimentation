"""
Autonomous Car Controller
=========================

This script controls an autonomous car's movement using a pre-trained model to predict speed and steering angle from camera input.

It initializes modules for the PiCamera module for image capture and UART communication to send control commands.
The script continuously captures images, processes them, and uses a machine learning model to predict the speed and steering angle to control the car's movement.

Modules:
--------
- uart_module: Manages UART communication for sending speed and angle data.
- picamera_module: Interfaces with the Raspberry Pi Camera for image capture.

Global Variables:
-----------------
- uart_controller Instance of UartController for UART communication.
- camera: Instance of PiCameraController to capture images.
- model: Pre-trained machine learning model for speed and angle prediction.

Functions:
----------
- preProcess(img): Preprocess the captured image for the model.
- main(): Main function to capture images, predict speed and angle, and send control commands over UART.

Example Usage:
--------------
To run the script, ensure the required modules (uart_module, picamera_module) are imported and available in the environment.

    $ python autonomous_car_controller.py

Dependencies:
-------------
- uart_module: Ensure that the `uart_module` module is properly implemented and available.
- picamera_module: Ensure that the `picamera_module` module is properly implemented and available.

Note:
-----
This script is designed to control an autonomous car system and requires proper hardware setup and configuration.
"""

# Importing necessary modules
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from uart_module import UartController
from picamera_module import PiCameraController

# Initializing modules
uart_controller = UartController("/dev/ttyS0", 9600)
camera = PiCameraController()
camera.pi_cam_init()
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
    Main function to capture images, predict speed and angle, and send control commands over UART.

    This function continuously captures images, processes them, and uses a pre-trained model to predict the speed and steering angle to control the car's movement.
    """
    img_path = os.path.join(os.getcwd(), "road_img")
    while True:
        camera.get_img(img_path)  # Capture image
        img = cv2.imread(img_path)
        img = np.asarray(img)  # Convert to numpy array
        img = preProcess(img)  # Preprocess the image
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        prediction = model.predict(img)  # Predict angle and speed
        angle = float(prediction[0][0])  # Extract angle
        speed = float(prediction[0][1])  # Extract speed

        print(f"Angle: {angle}, Speed: {speed}")  # Print values
        uart_message = f"{speed},{angle}"  # Create UART message
        uart_controller.send_data(uart_message)  # Send data over UART
        print(f"Sent over UART: {uart_message}")  # Print UART message
        cv2.waitKey(1)  # Wait for 1 ms

if __name__ == "__main__":
    main()
