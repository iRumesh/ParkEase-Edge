#!/usr/bin/python3


"""
* declaring package gate
* @description initializing the gate control. 3 Controlls, Open, Close and Stop.
* Gate will not close if the distance is less than the threshold distance.
"""


"""
* import statement section
* importing module yaml
* importing module sys
* importing module os
* importing module time
* importing module Jetson.GPIOn
* importing module pylogger
* importing module gpio
*
"""
import time
import sys, os
import yaml
import Jetson.GPIO as GPIO

# declaring package relative import for import sibiling directories of the sub package udp
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from pylogger import pylogger
from gpio import gpio
from sonar import sonar

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
* declaring function open_gate
* @param None
* @return None
* the main process of this function is to set the sr correspondig to gate open to ACTIVE HIGH
*
"""
def open_gate():
    GPIO.output(int(config_data['GATE_OPEN_OUT']), GPIO.HIGH)
    pylogger.write_log(
        'The open gate function has been called with using GPIO {A} with the value {B}'.format(A=config_data['GATE_OPEN_OUT'], B='HIGH'),
        executable_name=os.path.basename(__file__),
        function_name='open_gate',
        log_name="logger_gate_all.log",
        log_dir=pylogger.log_instance(file_suffix="gate")
    )
    time.sleep(float(config_data['SWITCH_DELAY']))
    GPIO.output(int(config_data['GATE_OPEN_OUT']), GPIO.LOW)
    pylogger.write_log(
        'The open gate function has been called with using GPIO {A} with the value {B}'.format(A=config_data['GATE_OPEN_OUT'], B='LOW'),
        executable_name=os.path.basename(__file__),
        function_name='open_gate',
        log_name="logger_gate_all.log",
        log_dir=pylogger.log_instance(file_suffix="gate")
    )
    time.sleep(float(config_data['GATE_CLOSE_TIME']) - float(config_data['SWITCH_DELAY']))


"""
* declaring function close_gate
* @param None
* @return None
* the main process of this function is to set the sr correspondig to gate close to ACTIVE HIGH
*
"""
def close_gate():
    GPIO.output(int(config_data['GATE_CLOSE_OUT']), GPIO.HIGH)
    pylogger.write_log(
        'The close gate function has been called with using GPIO {A} with the value {B}'.format(A=config_data['GATE_CLOSE_OUT'], B='HIGH'),
        executable_name=os.path.basename(__file__),
        function_name='close_gate',
        log_name="logger_gate_all.log",
        log_dir=pylogger.log_instance(file_suffix="gate")
    )

    start_time = time.time()
    exceed_count = 0
    while time.time() - start_time < float(config_data['SWITCH_DELAY']):
        if sonar.distance() < float(config_data['THRESHOLD_DIST']):
            exceed_count += 1
        else:
            exceed_count = 0
        if exceed_count > 5:
            GPIO.output(int(config_data['GATE_CLOSE_OUT']), GPIO.LOW)
            GPIO.output(int(config_data['GATE_STOP_OUT']), GPIO.HIGH)
            not_exceed_count = 0
            while True:
                if sonar.distance() < float(config_data['THRESHOLD_DIST']):
                    not_exceed_count += 1
                else:
                    not_exceed_count = 0
                if not_exceed_count > 5:
                    break
            GPIO.output(int(config_data['GATE_STOP_OUT']), GPIO.LOW)
            GPIO.output(int(config_data['GATE_CLOSE_OUT']), GPIO.HIGH)
            start_time = time.time()
            exceed_count = 0

    GPIO.output(int(config_data['GATE_CLOSE_OUT']), GPIO.LOW)
    pylogger.write_log(
        'The close gate function has been called with using GPIO {A} with the value {B}'.format(A=config_data['GATE_CLOSE_OUT'], B='LOW'),
        executable_name=os.path.basename(__file__),
        function_name='close_gate',
        log_name="logger_gate_all.log",
        log_dir=pylogger.log_instance(file_suffix="gate")
    )
    while time.time() - start_time < float(config_data['GATE_CLOSE_TIME']):
        pass


"""
* declaring function stop_gate
* @param None
* @return None
* the main process of this function is to set the sr correspondig to gate stop to ACTIVE HIGH
*
"""
def stop_gate():
    GPIO.output(int(config_data['GATE_STOP_OUT']), GPIO.HIGH)
    pylogger.write_log(
        'The stop gate function has been called with using GPIO {A} with the value {B}'.format(A=config_data['GATE_STOP_OUT'], B='HIGH'),
        executable_name=os.path.basename(__file__),
        function_name='stop_gate',
        log_name="logger_gate_all.log",
        log_dir=pylogger.log_instance(file_suffix="gate")
    )
    time.sleep(float(config_data['SWITCH_DELAY']))
    GPIO.output(int(config_data['GATE_STOP_OUT']), GPIO.LOW)
    pylogger.write_log(
        'The stop gate function has been called with using GPIO {A} with the value {B}'.format(A=config_data['GATE_STOP_OUT'], B='LOW'),
        executable_name=os.path.basename(__file__),
        function_name='stop_gate',
        log_name="logger_gate_all.log",
        log_dir=pylogger.log_instance(file_suffix="gate")
    )
