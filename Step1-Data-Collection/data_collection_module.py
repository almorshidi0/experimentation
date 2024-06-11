"""
Data Collection Module
======================

This module provides a simple interface to collect data by capturing images and logging associated information using pandas.

Classes:
--------
- DataCollector: A class to manage data collection.

Example Usage:
--------------
To use this module, create an instance of `DataCollector` and call its methods.

    from data_collection_module import DataCollector

    data_collector = DataCollector()
    data_collector.data_collection_init()
    data_collector.collect_data(0.5)

To test this module, you can run it directly as a script. It will collect data and save logs.

    $ python data_collection_module.py

Dependencies:
-------------
- pandas: Ensure that the `pandas` library is installed and properly configured on your system.
- picamera_module: Ensure that the `picamera_module` module is properly implemented and available.

Note:
-----
This script is intended to run on a Raspberry Pi with a connected camera module.
"""

import pandas as pd
import os
from picamera_module import PiCameraController
from datetime import datetime

class DataCollector:
    """
    Class to manage data collection.
    """
    def __init__(self):
        """
        Initialize DataCollector instance.

        This method initializes the data directory and lists.
        
        Args:
        None
        
        Returns:
        None
        """
        self.data_directory = None
        self.folder_index = None
        self.img_list = []
        self.speed_list = []
        self.angle_list = []

    def data_collection_init(self):
        """
        Initialize data collection.

        This method creates the data directory and initializes lists for image paths, speeds, and steering angles.
        
        Args:
        None
        
        Returns:
        None
        """
        self.data_directory = os.path.join(os.getcwd(), 'data_collected')
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)
        self.folder_index = 0
        self.img_list = []
        self.speed_list = []
        self.angle_list = []

    def collect_data(self, img_path, speed, angle):
        """
        Collect data by saving images and logging the speed and steering angle.

        Args:
        camera_controller (PiCameraController): Instance of PiCameraController.
        img_path (str): The directory path to save images.
        speed (float): Speed value.
        angle (float): Steering angle.
        
        Returns:
        None
        """
        self.img_list.append(img_path)
        self.speed_list.append(speed)
        self.angle_list.append(angle)

    def save_log(self):
        """
        Save the log file with image filenames, speeds, and steering angles.

        Args:
        None
        
        Returns:
        None
        """
        print(f"img: {len(self.img_list)}, speed:{len(self.speed_list)}, angle:{len(self.angle_list)}")
        raw_data = {'image': self.img_list, 'speed': self.speed_list, 'angle': self.angle_list}
        df = pd.DataFrame(raw_data)
        log_file_path = os.path.join(self.data_directory, f'log_{str(self.folder_index)}.csv')
        df.to_csv(log_file_path, index=False, header=False)
        print('Log saved')
        print('Total images:', len(self.img_list))
