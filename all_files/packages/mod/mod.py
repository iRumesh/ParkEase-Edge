#!/usr/bin/python3


"""
* declaring package mod
* @description this module is used to change the mode of the edge controller
* Starting mode: Auto
* During mode change buzzer & LED notification will be triggered
"""

"""
* import statement section
* import sys
* importing module os
* importing time
* import yaml
* importing jetson.GPIO as GPIO
* importing module pylogger
* importing module pyprint
* importing module gpio
* importing module gate
*
"""
import sys, os
import time
import yaml
import Jetson.GPIO as GPIO

# declaring package relative import for import sibiling directories of the sub package udp
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from pylogger import pylogger
from pyprint import pyprint
from gpio import gpio
from gate import gate

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

STATUS = config_data["STATE"]

"""
* declaring function manual_mode_indicator
* @param None
* @return None
* the main process of this function is to set the manual mode indicator to ACTIVE HIGH
*
"""
def manual_mode_indicator():
    GPIO.output((int(config_data["MODE_LED"])), GPIO.LOW)
    time.sleep(2)
    GPIO.output((int(config_data["MODE_LED"])), GPIO.HIGH)


"""
* declaring function mode_change_indicator
* @param None
* @return None
* the main process of this function is to set the manual mode indicator to ACTIVE HIGH
*
"""
def mode_change_indicator():
    for _ in range(10):
        GPIO.output((int(config_data["MODE_LED"])), GPIO.LOW)
        GPIO.output((int(config_data["BUZZER_PIN"])), GPIO.HIGH)

        time.sleep(0.1)
        GPIO.output((int(config_data["MODE_LED"])), GPIO.HIGH)
        GPIO.output((int(config_data["BUZZER_PIN"])), GPIO.LOW)
        time.sleep(0.1)


"""
* declaring function auto_mode_indicator
* @param None
* @return None
* the main process of this function is to set manual mod indicator to ACTIVE LOW
*
"""
def auto_mode_indicator():
    if STATUS:
        GPIO.output((int(config_data["MODE_LED"])), GPIO.HIGH)

"""
* declaring function gate_mode_out_indicator
* @param None
* @return None
* the main process of this function is to set the ssr to active HIGH or LOW corresponding to the mode
*
"""
def gate_mode_out_indicator(param:GPIO):
    GPIO.output((int(config_data["GATE_MODE_OUT"])), param)


"""
* declaring function mode_handler
* @param None
* @return None
* the main process of this function is to trigger the mod change event according to the usr input
*
"""
def mode_handler():
    while True:
        while not GPIO.input(int(config_data["GATE_MODE_IN"])):
            time.sleep(0.01)
            if GPIO.input(int(config_data["GATE_MODE_IN"])):
                mode_change_callback()
                time.sleep(3)


"""
* declaring function mode_change_callback
* @param None
* @return None
* the main process of this function is to set the global variable STATUS to the corresponding intiger
* 0-> manual and 1-> auto
*
"""
def mode_change_callback():
    
    global STATUS

    mode_change_indicator()

    if STATUS:
        pyprint.print_msg(
            "[INFO] Mode Changed to {A} mod".format(A=('MANUAL' if STATUS else 'AUTO')),
            executable_name=os.path.basename(__file__),
            function_name='mode_change_callback',
        )
        pylogger.write_log('Edge controlling mode has been changed from {A} mod to {B} mod'.format(A=('AUTO' if STATUS else 'MANUAL'), B=('MANUAL' if STATUS else 'AUTO')),
            executable_name=os.path.basename(__file__),
            function_name='mode_change_callback',
            log_name="logger_mod_all.log",
            log_dir=pylogger.log_instance(file_suffix="mod")
        )
        # if the STATUS is auto then the STATUS will be set to 0
        STATUS = 0
        time.sleep(2)
        

    else:
        # if the STATUS if manual then the STATUS will be set to 1
        STATUS = 1
        pyprint.print_msg(
            "[INFO] Mode Changed to {A} mod".format(A=('AUTO' if STATUS else 'MANUAL')),
            executable_name=os.path.basename(__file__),
            function_name='mode_change_callback',
        )
        pylogger.write_log('Edge controlling mode has been changed from {A} mod to {B} mod'.format(A=('MANUAL' if STATUS else 'AUTO'), B=('AUTO' if STATUS else 'MANUAL')),
            executable_name=os.path.basename(__file__),
            function_name='mode_change_callback',
            log_name="logger_mod_all.log",
            log_dir=pylogger.log_instance(file_suffix="mod")
        )
        
        gate.close_gate()
        time.sleep(2)