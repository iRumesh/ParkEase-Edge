#!/usr/bin/python3
"""
* declaring package buzzer
* @description initializing the buzzer allert.
"""


"""
* import statement section
* importing module os
* importing module sys
* importing module yaml
* importing module time
* importing module Jetson.GPIO
* importing module pylogger
* importing module gpio
*
"""

import os,sys
import yaml
import Jetson.GPIO as GPIO
import time

# declaring package relative import for import sibiling directories of the sub package udp
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from pylogger import pylogger
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

# initializing the GPIO declaration session
gpio.declare_gpio()


"""
* declaring sound_buzzer capture
* @param None
* @return None
* the main process of this function is to sound the buzzer
*
"""
def sound_buzzer():
    GPIO.output(int(config_data['BUZZER_PIN']), GPIO.HIGH)
    pylogger.write_log('The sound buzzer function has been called with using GPIO {A} with the value {B}'.format(A=config_data['BUZZER_PIN'], B='HIGH'),
        executable_name=os.path.basename(__file__),
        function_name='sound_buzzer',
        log_name="logger_buzzer_all.log",
        log_dir=pylogger.log_instance(file_suffix="buzzer")
    )
    time.sleep(0.5)
    GPIO.output(config_data['BUZZER_PIN'], GPIO.LOW)
    pylogger.write_log('The sound buzzer function has been called with using GPIO {A} with the value {B}'.format(A=config_data['BUZZER_PIN'], B='LOW'),
        executable_name=os.path.basename(__file__),
        function_name='sound_buzzer',
        log_name="logger_buzzer_all.log",
        log_dir=pylogger.log_instance(file_suffix="buzzer")
    )
    print("Buzzer is working")

"""
* declaring stop_buzzer capture
* @param None
* @return None
* the main process of this function is to stop the buzzer
*
"""
def stop_buzzer():
    GPIO.output(int(config_data['BUZZER_PIN']), GPIO.LOW)  # Turn off the buzzer
    pylogger.write_log('The sound buzzer function has been called with using GPIO {A} with the value {B}'.format(A=config_data['BUZZER_PIN'], B='LOW'),
        executable_name=os.path.basename(__file__),
        function_name='stop_buzzer',
        log_name="logger_buzzer_all.log",
        log_dir=pylogger.log_instance(file_suffix="buzzer")
    )