"""
Autonomous Car Controller
=========================

This script controls an autonomous car's movement using a pre-trained model to predict speed and steering angle from camera input.

It initializes modules for the PiCamera module for image capture and UART communication to send control commands.
The script continuously captures images, processes them, and uses a machine learning model to predict the speed and steering angle to control the car's movement.

Modules:
--------
- uart_module       : Manages UART communication for sending speed and angle data.
- picamera_module   : Interfaces with the Raspberry Pi Camera for image capture.

Global Variables:
-----------------
- speed : Initial speed.
- angle : Initial steering angle.
- model : Pre-trained machine learning model for speed and angle prediction.

Functions:
----------
- preProcess(img)           : Preprocess the captured image for the model.
- send_movement_commands()  : Send movement commands over UART based on current speed and angle.
- main()                    : Main function to capture images, predict speed and angle, and send control commands over UART.

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
from tensorflow.keras.models    import load_model
from uart_module                import UartController
from picamera_module            import PiCameraController

# Constants
SERIAL_PORT = "/dev/ttyS0"
BAUD_RATE   = 9600
ROI         = (0.0, 0.2, 0.8, 0.8)  # Ratio of interest
MODEL_PATH  = "path_to_your_model.h5"  # Update with your model path

# Global Variables
speed = 0  # Initial speed
angle = 0  # Initial steering angle
model = load_model(MODEL_PATH)

# Initializing modules
uart_controller = UartController(SERIAL_PORT, BAUD_RATE)

camera_controller = PiCameraController()
camera_controller.pi_cam_init(ROI)

def preProcess(img):
    """
    Preprocess the captured image for the model.

    Args:
        img (numpy.ndarray): The input image.

    Returns:
        numpy.ndarray: Preprocessed image.
    """
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)  # Convert to YUV color space
    img = cv2.GaussianBlur(img, (3, 3), 0)  # Apply Gaussian blur
    img = cv2.resize(img, (200, 66))  # Resize the image
    img = img / 255.0  # Normalize the image
    return img

def send_movement_commands():
    """
    Send movement commands over UART based on current speed and angle.
    
    This function formats the speed and angle into a string and sends it over UART.
    
    Args:
        None
    
    Returns:
        None
    """
    command = f"{speed},{angle}"
    uart_controller.send_data(command)

def main():
    """
    Main function to capture images, predict speed and angle, and send control commands over UART.

    This function continuously captures images, processes them, and uses a pre-trained model to predict the speed and steering angle to control the car's movement.
    
    Args:
        None
    
    Returns:
        None
    """
    global speed, angle, model
    try:
        while True:
            img_path = camera_controller.get_img()  # Capture image and get path
            img = cv2.imread(img_path)
            img = np.asarray(img)  # Convert to numpy array
            img = preProcess(img)  # Preprocess the image
            img = np.expand_dims(img, axis=0)  # Add batch dimension
            prediction = model.predict(img)  # Predict angle and speed
            speed = float(prediction[0][0])  # Extract speed
            angle = float(prediction[0][1])  # Extract angle

            print(f"Angle: {angle}, Speed: {speed}")  # Print values
            send_movement_commands()
            cv2.waitKey(1)  # Wait for 1 ms
    except KeyboardInterrupt:
        uart_controller.send_data("stop")
        uart_controller.close()

if __name__ == "__main__":
    main()
