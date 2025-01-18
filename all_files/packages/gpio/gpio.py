#!/usr/bin/python3


"""
* declaring package gpio
* @description this module is used to initialize the GPIO configuration for the edge controller
*
"""


"""
* import statement section
* importing os
* importing yaml
* importing GPIO from jetson
*
"""
import os
import yaml
import Jetson.GPIO as GPIO

# importing the configuration data
config_data = yaml.load(
    open(
        ("/".join(os.path.realpath(__file__).split("/")[0:-3]))
        + "/config/config.yaml",
        "r",
    ),
    Loader=yaml.FullLoader,
)

def declare_gpio():
    # bord configuration
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # setting the GATE_OPEN_OUT AS GPIO.OUT and initial state GPIO.LOW
    GPIO.setup(int(config_data['GATE_OPEN_OUT']), GPIO.OUT, initial=GPIO.LOW)

    #setting the GATE_CLOSE_OUT AS GPIO.OUT and initial state GPIO.LOW
    GPIO.setup(int(config_data['GATE_CLOSE_OUT']), GPIO.OUT, initial=GPIO.LOW)

    #setting the GATE_STOP_OUT AS GPIO.OUT and initial state GPIO.LOW
    GPIO.setup(int(config_data['GATE_STOP_OUT']), GPIO.OUT, initial=GPIO.LOW)

    #setting the GATE_MODE_OUT AS GPIO.OUT and initial state GPIO.LOW
    GPIO.setup(int(config_data['GATE_MODE_OUT']), GPIO.OUT,initial=GPIO.LOW)  # Automatic Mode

    #setting the GATE_MODE_IN AS GPIO.OUT and initial state GPIO.LOW
    GPIO.setup(int(config_data['GATE_MODE_IN']), GPIO.IN)

    #setting the MODE_LED AS GPIO.OUT and initial state GPIO.LOW
    GPIO.setup(int(config_data['MODE_LED']), GPIO.OUT, initial=GPIO.LOW)  # LED
    
    #setting the BUZZER_PIN AS GPIO.OUT
    GPIO.setup(int(config_data['BUZZER_PIN']), GPIO.OUT)

    #setting the BUTTON_PIN AS GPIO.OUT
    GPIO.setup(int(config_data['BUTTON_PIN']), GPIO.IN)

    # #setting the GPIO_TRIGGER AS GPIO.OUT
    # GPIO.setup(int(config_data['TRIG_PIN']), GPIO.OUT)

    # #setting the GPIO_ECHO AS GPIO.OUT
    # GPIO.setup(int(config_data['ECHO_PIN']), GPIO.IN)
    
"""
* declaring function clear_all_GPIOs
* @param None
* @return None
* the main process of this function is to set all GPIOs ACTIVE LOW
*
"""
def clear_all_GPIOs():
    GPIO.output((int(config_data["GATE_OPEN_OUT"])), 0)
    GPIO.output((int(config_data["GATE_CLOSE_OUT"])), 0)
    GPIO.output((int(config_data["GATE_STOP_OUT"])), 0)
    GPIO.output((int(config_data["GATE_MODE_OUT"])), 0)
    GPIO.output((int(config_data["MODE_LED"])), 0)
    GPIO.output((int(config_data["BUZZER_PIN"])), 0)
    # GPIO.output((int(config_data["TRIG_PIN"])), 0)