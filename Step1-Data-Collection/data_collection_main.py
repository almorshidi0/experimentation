"""
Data Collection Main Program
=========================

This script controls a car's movement using key presses and records data while the car is in motion.

It initializes modules for data collection, key press detection, and the PiCamera module for image capture.
The script continuously monitors key presses to adjust the car's speed and steering angle .
Key presses trigger various actions, such as adjusting speed and angle, starting and stopping recording, and terminating the program.
Recorded data includes images and corresponding speed and steering angle.

Modules:
--------
- data_collection_module    : Handles data collection and saving.
- key_press_module          : Manages key press detection and control.
- uart_module               : Manages UART communication for sending control commands.
- picamera_module           : Interfaces with the Raspberry Pi Camera for image capture.

Global Variables:
-----------------
- done      : Flag variable to terminate the program.
- record    : Flag variable to control recording status.
- key_val   : Current pressed key.
- key_old   : Last pressed key
- speed     : Speed
- angle     : Steering angle

Functions:
----------
- get_key_press()               : Get key press status and update global variables.
- update_movement_controls()    : Update speed and angle based on key presses.
- send_movement_commands()      : Send movement commands over UART based on current speed and angle.
- main()                        : Main function to control the car's movement, handle key presses, and manage data recording.


Key Presses:
------------
- RIGHT : Increase speed and steer right.
- LEFT  : Increase speed and steer left.
- UP    : Increase speed.
- DOWN  : Decrease speed.
- r     : Start or stop recording.
- s     : Stop the car.
- k     : Terminate the program.

Example Usage:
--------------
To run the script, ensure the required modules (data_collection_module, key_press_module, uart_module, picamera_module) are imported and available in the environment.

    $ python3 data_collection_main.py

Dependencies:
-------------
- data_collection_module    : Ensure that the `data_collection_module` module is properly implemented and available.
- key_press_module          : Ensure that the `key_press_module` module is properly implemented and available.
- uart_module               : Ensure that the `uart_module` module is properly implemented and available.
- picamera_module           : Ensure that the `picamera_module` module is properly implemented and available.

Note:
-----
This script is designed to control an autonomous car system and requires proper hardware setup and configuration.
"""

# Importing necessary modules
import os
from data_collection_module import DataCollector
from key_press_module       import KeyPressController
from uart_module            import UartController
from picamera_module        import PiCameraController

# Constants
KEY_LIST = ["RIGHT", "LEFT", "UP", "DOWN", "r", "s", "k"]
SERIAL_PORT = "/dev/ttyS0"
BAUD_RATE = 9600
ROI = (0.0, 0.2, 0.8, 0.8) # Ratio of interest

# Global Variables
done    = 0     # Flag variable to terminate the program
record  = 0     # Flag variable to control recording status
key_val = None  # Current pressed key
key_old = None  # Last pressed key
speed   = 0     # Initial speed
angle   = 0     # Initial steering angle

# Initializing modules
data_collector = DataCollector()
data_collector.data_collection_init()

key_controller = KeyPressController()
key_controller.key_press_init()

uart_controller = UartController(SERIAL_PORT, BAUD_RATE)

camera_controller = PiCameraController()
camera_controller.pi_cam_init(ROI)

def get_key_press():
    """
    Get key press status and update global variables.
    
    This function checks the status of each key in the KEY_LIST and updates the key_val accordingly.
    
    Args:
        None
    
    Returns:
        None
    """
    global key_val
    for key in KEY_LIST:
        if key_controller.get_key_status(key):
            key_val = key
            break

def update_movement_controls():
    """
    Update speed and angle based on key presses.
    
    This function updates the speed and angle variables based on the current pressed key.
    
    Args:
        None
    
    Returns:
        None
    """
    global speed, angle, record, done, key_val, key_old
    if key_val == "RIGHT":
        speed = 0.6
        angle = speed
    elif key_val == "LEFT":
        speed = 0.6
        angle = -speed
    elif key_val == "UP":
        speed = 0.4
        angle = 0
    elif key_val == "DOWN":
        speed = -0.4
        angle = 0
    elif key_val == "s":
        speed = 0
        angle = 0
    elif key_val == "k":
        done += 1
    elif key_val == key_old:
        pass
    elif key_val == "r":
        key_old = key_val
        record += 1
    if key_val != "r":
        key_val = None
        key_old = None

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
    Main function to control the car's movement.
    
    This function continuously monitors key presses, updates movement controls, and manages data recording.
    
    Args:
        None
    
    Returns:
        None
    """
    global speed, angle, record, done, key_val, key_old
    while True:
        angle = 0
        get_key_press()
        update_movement_controls()
        send_movement_commands()

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
            data_collector.speed_list.clear()
            data_collector.angle_list.clear()

        # Terminate program
        if done != 0:
            uart_controller.send_data("stop")
            uart_controller.close()
            break

if __name__ == "__main__":
    main()
