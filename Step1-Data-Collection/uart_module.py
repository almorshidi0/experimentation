"""
UART Module
=======================

This module provides a simple interface to control UART communication on a Raspberry Pi.

Classes:
--------
- UartController: A class to manage the initialization and control of UART communication.

Example Usage:
--------------
To use this module, create an instance of `UartController` and call its methods.

    from uart_module import UartController

    uart_controller = UartController("/dev/ttyS0", 9600)
    uart_controller.send_data("Hello, UART!")
    data = uart_controller.receive_data()

To test this module, you can run it directly as a script. It will perform a series of UART operations.

    $ python uart_module.py

Dependencies:
-------------
- pyserial: Ensure that the `pyserial` library is installed and properly configured on your system.

Note:
-----
This script is intended to run on a Raspberry Pi with a UART interface.
"""

import serial
import time

class UartController:
    """
    Class to control UART communication.
    """
    def __init__(self, port, baudrate):
        """
        Initialize the UART interface with the specified port and baudrate.

        Args:
            port: UART port (e.g., "/dev/ttyS0").
            baudrate: Baud rate for UART communication.
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = serial.Serial(port, baudrate)

    def send_data(self, data):
        """
        Send data over UART.

        Args:
            data: Data to be sent as a string.
        """
        if self.serial_connection.is_open:
            self.serial_connection.write(data.encode())

    def receive_data(self, timeout=1):
        """
        Receive data over UART.

        Args:
            timeout: Timeout for receiving data in seconds. Default is 1 second.
            
        Returns:
            Received data as a string.
        """
        self.serial_connection.timeout = timeout
        if self.serial_connection.is_open:
            received_data = self.serial_connection.read_all()
            return received_data.decode()
        return ""

    def close(self):
        """Close the UART connection."""
        if self.serial_connection.is_open:
            self.serial_connection.close()

def main():
    """
    Main function for module testing.

    This function creates an instance of `UartController`, initializes the UART interface, and
    performs a series of UART operations to test the communication functions.
    
    This function is intended for testing purposes and should not be used
    when the module is imported elsewhere.
    
    Args:
    None
    
    Returns:
    None
    """
    print("Initializing UART communication...")
    uart_controller = UartController("/dev/ttyS0", 9600)
    print("UART initialized.")

    try:
        while True:
            # Send data
            uart_controller.send_data("Hello, UART!")
            print("Sent: Hello, UART!")
            time.sleep(1)

            # Receive data
            received_data = uart_controller.receive_data()
            if received_data:
                print(f"Received: {received_data}")
            else:
                print("No data received.")
            time.sleep(1)

    except KeyboardInterrupt:
        uart_controller.close()
        print()
        print("UART communication stopped.")

if __name__ == '__main__':
    main()
