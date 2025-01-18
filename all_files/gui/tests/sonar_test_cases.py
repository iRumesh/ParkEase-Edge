########################################################  Ultrasonic sensor testing for the new setup  ##################################################################

import Jetson.GPIO as GPIO
import time
import sys,os
import yaml
from tkinter import messagebox
import tkinter as tk
import serial

HOME_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, HOME_DIR)

from packages import sonar

# importing the configuration data
config_data_path = os.path.join(HOME_DIR, "config", "config.yaml")
config_data = yaml.load( open(config_data_path, "r"), Loader=yaml.FullLoader )

# Use the correct serial port; it might not be ttyUSB0
ser = serial.Serial('/dev/ttyTHS1', 9600)  # Check this port

while True:
    
    for i in range(20):
        distance = sonar.distance()
        print(f"Distance: {distance} cm")
        time.sleep(0.05)

    update_seen = sys.argv[1]

    time.sleep(1)  # Simulate some initial processing

    if update_seen == 'prompt':
        root = tk.Tk()  # Create a temporary Tk instance for messagebox
        root.withdraw()  # Hide the root window

        answer = messagebox.askyesno(title="Test Case Complete", message="Did 'Sonar_test' complete successfully?")

        root.destroy()  # Destroy the temporary Tk instance after use

        if answer:
            update_seen = '1'
        else:
            update_seen = '0'

    if update_seen == '1':
        print("User confirmed success.")
        sys.exit(0)

    elif update_seen == '0':
        print("User confirmed failure.")
        sys.exit(1)