#!/usr/bin/python3

"""
* declaring package sonar_reading
* @description Configures Jetson Nano GPIO pins to interface with ultrasonic sensors for distance measurement.
    Utilizes GPIO pins (GPIO pins 24 and 26) for triggering and receiving signals from the sensor.
    Operates continuously, displaying measured distances in centimeters and appending the data to a file named "distance.txt".
* 

"""
"""
* import statement section
* importing GPIO from Jetson as GPIO
* importing time
* importing os
* importing sys
* importing yaml
*
"""
import Jetson.GPIO as GPIO
import time
import os, sys
import yaml
import serial

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from mod import mod

# importing the configuration data
config_data = yaml.load(
    open(
        ("/".join(os.path.realpath(__file__).split("/")[0:-3]))
        + "/config/config.yaml",
        "r",
    ),
    Loader=yaml.FullLoader,
)
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(config_data['GPIO_WARNING'])


# Configure the serial connection
dev_serial_prt = serial.Serial(
    port=config_data['SERIAL_PORT'],   # Replace with your specific port
    baudrate=config_data['BAUD_RATE'],        # Set the baudrate to match the Jetson Nano configuration
    timeout=1               # Set timeout for reading in seconds
)

def measure():
    try:
        
        if dev_serial_prt.in_waiting > 0:
            # Read data from the serial port
            data = dev_serial_prt.readline().decode('utf-8').strip()
            # print(f"Raw data received: {data}")  # Debug print
            dist = float(data)  # Decoding to utf-8 and stripping newline cha-racters
        else:
            # print("No data available in the serial port.")  # Debug print
            dist = 0

        # Flush the input buffer to clear any old data
        dev_serial_prt.reset_input_buffer()

    except Exception as e:
        # print(f"Error reading from serial port: {e}")  # Debug print
        dist = 0
    return dist

def distance():
    dist = 0
    count = 0
    while dist == 0 :
        time.sleep(0.1)
        dist = measure()
        count += 1
        if count >= 20:
            return dist
    return dist
