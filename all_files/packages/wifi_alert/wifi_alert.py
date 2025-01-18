#!/usr/bin/python3

# Description: 

"""
* Monitors internet connectivity using a ping check to a specific IP address (8.8.8.8).
* Utilizes GPIO pins to control a buzzer for alerting when no internet connection is detected.
* Runs in a loop, checking internet status, triggering the buzzer, and attempting Wi-Fi reconnection if needed.
* Runs in a seperate thread parallel to the main program
"""

"""
* declaring package log
* @description Establishes a UDP socket communication setup to send data packets to a designated IP address and port.
*
"""


"""
* import statement section
* importing module os
* importing module sys
* importing module time
* importing module yaml
* importing module subprocess
* importing module Jetson.GPIO
* importing module pylogger
* importing module pyprint
* importing module buzzer
* importing module gpio
*
"""
import os, sys
import time
import yaml
import subprocess
import Jetson.GPIO as GPIO

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from pylogger import pylogger
from pyprint import pyprint
from buzzer import buzzer
from gpio import gpio

# importing the configuration data
config_data = yaml.load(
    open(
        ("/".join(os.path.realpath(__file__).split("/")[0:-3]))
        + "/config/config.yaml",
        "r",
    ),
    Loader=yaml.FullLoader,
)

gpio.declare_gpio()

# Define a list of Wi-Fi network credentials
wifi_networks = [
    {"ssid": config_data['NETWORK_A']['SSID'], "password": config_data['NETWORK_A']['PASSWORD']},
    {"ssid": config_data['NETWORK_B']['SSID'], "password": config_data['NETWORK_B']['PASSWORD']},
    {"ssid": config_data['NETWORK_C']['SSID'], "password": config_data['NETWORK_C']['PASSWORD']},
    {"ssid": config_data['NETWORK_D']['SSID'], "password": config_data['NETWORK_D']['PASSWORD']},
    {"ssid": config_data['NETWORK_E']['SSID'], "password": config_data['NETWORK_E']['PASSWORD']},
]


# initializing the state flag called CONTROLL_SIGNAL
# this flag is used to initialize the state of the buzzer 1 -> active state and 0 -> for innactive state
CONTROLL_SIGNAL = 1


"""
* declaring function change_controll_signal
* @param None
* @return None
* the main process of this function is to change the state of the CONTROLL_SIGNAL according to the btn input that recive from the config_data["BUTTON_PIN"]
*
"""
def change_controll_signal():
    global CONTROLL_SIGNAL
    while True:
        while not GPIO.input(int(config_data["BUTTON_PIN"])):
            time.sleep(0.01)
            if GPIO.input(int(config_data["BUTTON_PIN"])):
                # this function change the state of the CONTROLL_SIGNAL according to the btn input that recive from the config_data["BUTTON_PIN"]
                CONTROLL_SIGNAL = 0
    

"""
* declaring function is_internet_connected
* @param None
* @return None
* the main process of this function is to check internet connectivity
*
"""
def is_internet_connected():
    try:
        subprocess.check_output(["ping", "-c", "1", "8.8.8.8"], stderr=subprocess.STDOUT, universal_newlines=True)
        return True  
        # If the subprocess completes without errors, the internet is connected.
    except subprocess.CalledProcessError:
        return False


"""
* declaring function connect_to_wifi
* @param None
* @return None
* the main process of this function is to connect to pre defined Wi-Fi networks
*
"""
def connect_to_wifi():
    if config_data['WIFI_AUTO_CONNET_ENABLE']:
        for wifi_network in wifi_networks:
            ssid = wifi_network["ssid"]
            password = wifi_network["password"]

            try:
                connection_result = subprocess.run(
                    [
                        'nmcli', 'dev', 'wifi',
                        'connect', ssid,
                        'password', password
                    ]
                )
                pylogger.write_log(
                    f"connected to wifi network {ssid}",
                    executable_name=os.path.basename(__file__),
                    function_name='connect_to_wifi',
                    log_name="logger_wifi_check_alert_all.log",
                    log_dir=pylogger.log_instance(file_suffix="wifi_alert")
                )
                pyprint.print_msg(
                    f"connected to wifi network {ssid}",
                    executable_name=os.path.basename(__file__),
                    function_name='connect_to_wifi',
                ) 
            except subprocess.CalledProcessError as e:
                pylogger.write_log(
                    f"error connecting to wifi network {ssid}: {e}",
                    executable_name=os.path.basename(__file__),
                    function_name='connect_to_wifi',
                    log_name="logger_wifi_check_alert_all.log",
                    log_dir=pylogger.log_instance(file_suffix="wifi_alert")
                )
                pyprint.print_msg(
                    f"connected to wifi network {ssid}",
                    executable_name=os.path.basename(__file__),
                    function_name='connect_to_wifi',
                )
            
            if not connection_result:
                return True

    return False


"""
* declaring function wifi_check_alert
* @param None
* @return None
* the main process of this function is to enable the buzzer signal if the wifi is not connected
*
"""
def wifi_check_alert():
    from mod.mod import STATUS
    if STATUS and config_data['WIFI_ALLERT_ENABLE']:
        # state wether the mode is AUTO
        if ((not is_internet_connected())):# when no internet
            if( not connect_to_wifi()):
                pylogger.write_log("Connection estabilization is failed for all SSID\'s provided. retying.",
                    executable_name=os.path.basename(__file__),
                    function_name='wifi_check_alert',
                    log_name="logger_wifi_check_alert_all.log",
                    log_dir=pylogger.log_instance(file_suffix="wifi_alert")
                )
                pyprint.print_msg(
                    "All available networks failed to connect. retrying.",
                    executable_name=os.path.basename(__file__),
                    function_name='wifi_check_alert',
                )     
            
            if CONTROLL_SIGNAL:
                print(CONTROLL_SIGNAL)
                # state wether the CONTROLL_SIGNAL is TRUE
                buzzer.sound_buzzer()
                pylogger.write_log("Internet connection is not avaliable. The sound buzzer function has been called with using GPIO {A} with the value {B}'.format(A=config_data['BUZZER_PIN'], B='HIGH')'",
                    executable_name=os.path.basename(__file__),
                    function_name='wifi_check_alert',
                    log_name="logger_wifi_check_alert_all.log",
                    log_dir=pylogger.log_instance(file_suffix="wifi_alert")
                )

            return 0
            
        else:
            return 1

if __name__ == "__main__":
    wifi_check_alert()