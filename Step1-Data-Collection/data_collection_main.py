"""
Data Collection Main Program
=========================

This script controls a car's movement using key presses and records data while the car is in motion.

It initializes modules for data collection, key press detection, and the PiCamera module for image capture.
The script continuously monitors key presses to adjust the car's speed and steering angle.
Key presses trigger various actions, such as adjusting speed and angle, starting and stopping recording, and terminating the program.
Recorded data includes images and corresponding speed and steering angle.

Modules:
--------
- data_collection_module: Handles data collection and saving.
- key_press_module: Manages key press detection and control.
- uart_module: Manages UART communication for sending speed and angle data to the microcontroller.
- picamera_module: Interfaces with the Raspberry Pi Camera for image capture.

Global Variables:
-----------------
- done: Flag variable to terminate the program.
- record: Flag variable to control recording status.
- key_val: Last key pressed.
- key_press_t, key_press_t_1: Dictionaries to track key press status.

Functions:
----------
- main(): Main function to control the car's movement, handle key presses, and manage data recording.

Key Presses:
------------
- RIGHT: Steer right.
- LEFT: Steer left.
- UP: Increase speed.
- DOWN: Decrease speed.
- r: Start or stop recording.
- s: Stop the car.
- k: Terminate the program.

Example Usage:
--------------
To run the script, ensure the required modules (data_collection_module, key_press_module, uart_module, picamera_module) are imported and available in the environment.

    $ python data_collection_main.py

Dependencies:
-------------
- data_collection_module: Ensure that the `data_collection_module` module is properly implemented and available.
- key_press_module: Ensure that the `key_press_module` module is properly implemented and available.
- uart_module: Ensure that the `uart_module` module is properly implemented and available.
- picamera_module: Ensure that the `picamera_module` module is properly implemented and available.

Note:
-----
This script is designed to control an autonomous car system and requires proper hardware setup and configuration.
"""

# Importing necessary modules
import os
from data_collection_module import DataCollector
from key_press_module       import KeyPressController
from picamera_module        import PiCameraController
from uart_module            import UartController

# Constants
KEY_LIST = ["RIGHT", "LEFT", "UP", "DOWN", "r", "s", "k"]
SERIAL_PORT = "/dev/ttyS0"
BAUD_RATE = 9600

# Global Variables
done            = 0                                 # Flag variable to terminate the program
record          = 0                                 # Flag variable to control recording status
key_val         = KEY_LIST[0]                       # Last key pressed
key_press_t_1   = {key: False for key in KEY_LIST}  # Dictionary to track key press status (previous)
key_press_t     = {key: False for key in KEY_LIST}  # Dictionary to track key press status (current)
speed           = 0                                 # Initial speed
angle           = 0                                 # Initial steering angle

# Initializing modules
data_collector = DataCollector()
data_collector.data_collection_init()

key_controller = KeyPressController()
key_controller.key_press_init()

uart_controller = UartController(SERIAL_PORT, BAUD_RATE)

camera_controller = PiCameraController()
roi = (0.0, 0.2, 0.8, 0.8) #ratio of interest
camera_controller.pi_cam_init(roi)

def get_key_press():
    """
    Get key press status and update global variables.
    
    This function checks the status of each key in the KEY_LIST and updates the key_val and key_press_t variables accordingly.
    
    Args:
        None
    
    Returns:
        None
    """
    global key_val
    for key in KEY_LIST:
        if key_controller.get_key_status(key):
            key_val = key
            key_press_t[key] = True
            break
        else:
            key_press_t[key] = False

def update_movement_controls():
    """
    Update speed and angle based on key presses.
    
    This function updates the speed and angle variables based on the last key pressed.
    
    Args:
        None
    
    Returns:
        None
    """
    global speed, angle, record, done
    if (key_press_t[key_val] != key_press_t_1[key_val]):
        key_press_t_1[key_val] = key_press_t[key_val]
    else:
        return
    if (key_press_t[key_val] == True):
        key_press_t_1[key_val]
        print(key_val)
        if key_val == "RIGHT":
            angle += 0.2
        elif key_val == "LEFT":
            angle -= 0.2
        elif key_val == "UP":
            speed += 0.2
            angle = 0
        elif key_val == "DOWN":
            speed -= 0.2
            angle = 0
        elif key_val == "r":
            record += 1
        elif key_val == "s":
            speed = 0
            angle = 0
        elif key_val == "k":
            done += 1

def main():
    """
    Main function to control the car's movement.
    
    This function continuously monitors key presses, updates movement controls, sends movement controls to the microcontroller, and manages data recording.
    
    Args:
        None
    
    Returns:
        None
    """
    global speed, angle, record, done
    while True:
        get_key_press()
        update_movement_controls()

        # Send speed and angle over UART
        uart_message = f"{speed},{angle}"
        uart_controller.send_data(uart_message)
        print(f"Sent over UART: {uart_message}")

        # Start recording
        if record == 1:
            print("Recording Started ...")
            while os.path.exists(os.path.join(data_collector.data_directory, f"img{str(data_collector.folder_index)}")):
                data_collector.folder_index += 1
            new_path = os.path.join(data_collector.data_directory, f"img{str(data_collector.folder_index)}")
            os.makedirs(new_path)
            record += 1
        # Collect data
        if record == 2:
            data_collector.collect_data(camera_controller, new_path, speed, angle)
        # Save data and reset
        elif record == 3:
            record = 0
            data_collector.save_log()
            data_collector.img_list.clear()
            data_collector.angle_list.clear()

        # Terminate program
        if done != 0:
            uart_controller.close()
            break

if __name__ == "__main__":
    main()
