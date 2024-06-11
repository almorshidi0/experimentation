"""
Key Press Module
=======================

This module provides a simple interface to initialize Pygame and check for key presses.

Classes:
--------
- KeyPressController: A class to manage Pygame initialization and key press detection.

Example Usage:
--------------
To use this module, create an instance of `KeyPressController` and call its methods.

    from pygame_key_press_module import KeyPressController

    key_controller = KeyPressController()
    key_controller.key_press_init()
    if key_controller.get_key_status("r"):
        print("Key 'r' was pressed")

To test this module, you can run it directly as a script. It will check for key presses and print a message when a specified key is pressed.

    $ python pygame_key_press_module.py

Dependencies:
-------------
- pygame: Ensure that the `pygame` library is installed.

Note:
-----
This script creates a small window to capture key presses.
"""

import pygame
from time import sleep

class KeyPressController:
    """
    A class to manage Pygame initialization and key press detection.

    Attributes:
    -----------
    window: Pygame display surface.
    """
    def __init__(self):
        """
        Initialize the KeyPressController class.

        Initializes the window attribute to None.
        """
        self.window = None

    def key_press_init(self):
        """
        Initialize Pygame and create a window.

        This method initializes Pygame and creates a window with a size of 100x100 pixels to capture key presses.
        
        Args:
        None
        
        Returns:
        None
        """
        pygame.init()
        self.window = pygame.display.set_mode((100, 100))

    def get_key_status(self, key_name):
        """
        Check if a specific key is pressed.

        This method checks if a specific key is currently pressed.
        
        Args:
        key_name (str): The name of the key to check.
        
        Returns:
        bool: True if the key is pressed, False otherwise.
        """
        ans = False
        my_key = getattr(pygame, 'K_{}'.format(key_name))
        for event in pygame.event.get():
            pass
        key_input = pygame.key.get_pressed()
        ans = key_input[my_key]
        pygame.display.update()
        return ans

def main():
    """
    Main function for module testing.

    This function creates an instance of `KeyPressController`, initializes Pygame, and
    then checks for key presses. If a key is pressed, it prints a message indicating which key was pressed.
    
    This function is intended for testing purposes and should not be used
    when the module is imported elsewhere.
    
    Args:
    None
    
    Returns:
    None
    """
    key_list = ['r', 'g', 's', 'UP', 'DOWN', 'RIGHT', 'LEFT']
    key_controller = KeyPressController()
    key_controller.key_press_init()
    count = 0 
    while count < 1000:
        sleep(0.02)
        for key in key_list:
            if key_controller.get_key_status(key):
                print(f'Key {key} was pressed')
        count += 1

if __name__ == '__main__':
    main()
