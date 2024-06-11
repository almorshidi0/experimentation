"""
DC Motors Module
=======================

This module provides a simple interface to control a small car prototype with four DC motors using the `gpiozero` library.

Classes:
--------
- DcMotorController: A class to manage the initialization and control of the DC motors.

Example Usage:
--------------
To use this module, create an instance of `DcMotorController` and call its methods.

    from dc_motor_module import DcMotorController

    motor_controller = DcMotorController()
    motor_controller.move_forward(0.6)

To test this module, you can run it directly as a script. It will perform a series of movements.

    $ python dc_motor_module.py

Dependencies:
-------------
- gpiozero: Ensure that the `gpiozero` library is installed and properly configured on your system.

Note:
-----
This script is intended to run on a Raspberry Pi with connected DC motors.
"""

from gpiozero import Motor
from time import sleep

class DcMotorController:
    """
    Class to control a DC motor module consisting of two motors.
    """
    def __init__(self, ena1, in1, in2, ena2, in3, in4):
        """
        Initialize the DC motor module with the specified GPIO pins.

        Args:
            ena1: GPIO pin for motor enable 1 (ENA1).
            in1: GPIO pin for motor input 1 (IN1).
            in2: GPIO pin for motor input 2 (IN2).
            ena2: GPIO pin for motor enable 2 (ENA2).
            in3: GPIO pin for motor input 3 (IN3).
            in4: GPIO pin for motor input 4 (IN4).
        """
        self.motors_right = Motor(forward=in1, backward=in2, enable=ena1)
        self.motors_left  = Motor(forward=in3, backward=in4, enable=ena2)

    def move_forward(self, speed=0.5, angle=0):
        """
        Move the motor forward with the specified speed and angle.

        Args:
            speed: Speed of forward motion, ranging from 0 (full stop) to 1 (full forward). Default is 0.5.
            angle: Angle ratio, ranging from -1 (full left) to 1 (full right). Default is 0.
        """
        speed = max(0, min(1, speed))
        angle = max(-1, min(1, angle))
        speed_right = speed - angle
        speed_left  = speed + angle
        speed_right = max(0, min(1, speed_right))
        speed_left = max(0, min(1, speed_left))
        self.motors_right.forward(speed_right)
        self.motors_left.forward(speed_left)

    def move_backward(self, speed=0.5, angle=0):
        """
        Move the motor backward with the specified speed and angle.

        Args:
            speed: Speed of backward motion, ranging from 0 (full stop) to 1 (full backward). Default is 0.5.
            angle: Turn value, ranging from -1 (full left) to 1 (full right). Default is 0.
        """
        speed = -speed
        speed = max(0, min(1, speed))
        angle = max(-1, min(1, angle))
        speed_right = speed - angle
        speed_left  = speed + angle
        speed_right = max(0, min(1, speed_right))
        speed_left = max(0, min(1, speed_left))
        self.motors_right.backward(speed_right)
        self.motors_left.backward(speed_left)

    def stop(self):
        """Stop the motor."""
        self.motors_right.stop()
        self.motors_left.stop()
        
    def release(self):
        """Release the GPIO resources used by the motor."""
        self.motors_right.close()
        self.motors_left.close()

def main():
    """
    Main function for module testing.

    This function creates an instance of `DcMotorController`, initializes the motors, and
    performs a series of movements to test the motor control functions.
    
    This function is intended for testing purposes and should not be used
    when the module is imported elsewhere.
    
    Args:
    None
    
    Returns:
    None
    """
    print("Let's introduce our motors to our PI!")
    motor_controller = DcMotorController(17, 27, 22, 25, 23, 24)
    print("Let's go!")
    try:
        while True:
            # Move Forward
            motor_controller.move_forward(0.6)
            sleep(2)
            print("The car is moving forward!")
            motor_controller.stop()
            print("The car stopped moving!")
            sleep(2)
            
            # Move Backward
            motor_controller.move_backward(0.6)
            print("The car is moving backward!")
            sleep(2)
            motor_controller.stop()
            print("The car stopped moving!")
            sleep(2)
            
            # Move Forward and Turn Right
            motor_controller.move_forward(0.6, 0.4)
            print("The car is turning right!")
            sleep(2)
            motor_controller.stop()
            print("The car stopped moving!")
            sleep(2)
            
            # Move Forward and Turn Left
            motor_controller.move_forward(0.6, -0.4)
            print("The car is turning left!")
            sleep(2)
            motor_controller.stop()
            print("The car stopped moving!")
            sleep(2)
    except KeyboardInterrupt:
        motor_controller.stop()
        motor_controller.release()
        print()
        print("The car is now dead!")

if __name__ == '__main__':
    main()
