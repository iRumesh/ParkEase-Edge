"""
* import statement section
* importing os
* importing sys
* importing yaml
* importing time
* importing threading
* importing GPIO from jetson
* importing status module from packages
* importing pylogger module from packages
* importing pyprint module from packages
* importing gpio from packages
* importing mod from packages
* importing module gate from packages
* importing module wifi_alert from packages
* importing module main_callable from executables
*
"""
import os, sys
import yaml
import time
import threading
import Jetson.GPIO as GPIO

HOME_DIR = os.path.dirname(os.path.realpath(__file__))

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, HOME_DIR)

from packages import status
from packages import pylogger
from packages import pyprint
from packages import gpio
from packages import mod
from packages import gate
from packages import wifi_alert
from packages import vehicle_passed
from packages import parse
from executables import main_callable

# importing the configuration data
config_data_path = os.path.join(HOME_DIR, "config", "config.yaml")
config_data = yaml.load( open(config_data_path, "r"), Loader=yaml.FullLoader )

gpio.declare_gpio()


"""
* declaring function main -> the main executable point
* @param int args
* @return None
"""
def main(args:int=None):
    try:
        # calling the automode indicator function to indicate the system is running on auto mode
        mod.auto_mode_indicator() 

        parse.panelReset(
            UDP_IP=config_data["UDP_IP_IN"],
            UDP_PORT=config_data["UDP_PORT"],
        )

        parse.panelReset(
            UDP_IP=config_data["UDP_IP_OUT"],
            UDP_PORT=config_data["UDP_PORT"],
        )
  
        pyprint.print_msg(
            f"\n\nEdge system is controlled via {('AUTO' if status.STATUS else 'MANUAL')} mod",
            executable_name=os.path.basename(__file__),
            function_name='main',
        )
        pylogger.write_log(f"Edge system is controlled via {('AUTO' if status.STATUS else 'MANUAL')} mod",
            executable_name=os.path.basename(__file__),
            function_name='main',
            log_name="logger_main_all.log",
            log_dir=pylogger.log_instance(file_suffix="main")
        )     
        time.sleep(1)
        
        pylogger.write_log(
            'calling the function close gate',
            executable_name=os.path.basename(__file__),
            function_name='main',
            log_name="logger_main_all.log",
            log_dir=pylogger.log_instance(file_suffix="main")
        )
        
        pyprint.print_msg(
            "gate is closing for the startup debug",
            executable_name=os.path.basename(__file__),
            function_name='main',
        )
        # calling the gate close function to close the gate for testing
        gate.close_gate()

        pylogger.write_log(
            'calling the function close gate',
            executable_name=os.path.basename(__file__),
            function_name='main',
            log_name="logger_main_all.log",
            log_dir=pylogger.log_instance(file_suffix="main")
        )

        pyprint.print_msg(
            "gate is closing for the startup debug",
            executable_name=os.path.basename(__file__),
            function_name='main',
        )
        # calling the gate close function to close the gate for testing
        gate.close_gate()
        time.sleep(2)

        # entering to the continous loop
        while 1:
            # statements that are going to run if the system is running on auto mode
            if mod.STATUS and wifi_alert.is_internet_connected():
                # calling the gate mode out indicator function to switch on the SSR drives
                mod.gate_mode_out_indicator(GPIO.LOW)
                time.sleep(2)
                # calling the automode indicator function to indicate the system is running on auto mode
                mod.auto_mode_indicator()
                # continouning the system process
                main_callable.main_callable()
                
            # statements that are going to run if the system is running on manual mode
            else:
                # calling the gate mode out indicator function to switch off the SSR drives
                # this function will pass the controll to the manual remote system

                wifi_alert.wifi_check_alert() #added this line for testing
                
                mod.gate_mode_out_indicator(GPIO.HIGH)
                time.sleep(1)
                # calling the manualmode indicator function to indicate the system is running on manual mode
                mod.manual_mode_indicator()

                parse.panelReset(
                    UDP_IP=config_data["UDP_IP_IN"],
                    UDP_PORT=config_data["UDP_PORT"],
                )

                parse.panelReset(
                    UDP_IP=config_data["UDP_IP_OUT"],
                    UDP_PORT=config_data["UDP_PORT"],
                )


    # expecting for a keybord interrupt to manually stop the system 
    except KeyboardInterrupt as exp:
        print(f"Application killed by keybord interrupt {exp}")
        # switching the level to low level of the all GPIOs
        gpio.clear_all_GPIOs()
    finally:
        # cleaning up the GPIO declaration
        GPIO.cleanup((int(config_data["GATE_OPEN_OUT"])))
        GPIO.cleanup((int(config_data["GATE_CLOSE_OUT"])))
        GPIO.cleanup((int(config_data["GATE_STOP_OUT"])))
        GPIO.cleanup((int(config_data["GATE_MODE_OUT"])))
        GPIO.cleanup((int(config_data["MODE_LED"])))
        GPIO.cleanup((int(config_data["BUZZER_PIN"])))
        # GPIO.cleanup((int(config_data["TRIG_PIN"])))
    
if __name__ == "__main__":
    # declaring a thread for capture the mod change event
    mod_change_thread = threading.Thread(
        target=mod.mode_handler, args=(), daemon=True
    )
    # declaring a thread for capture the btn press event for stop the buzzer
    buzzer_interrupt_thread = threading.Thread(
        target=wifi_alert.change_controll_signal, args=(), daemon=True
    )
    mod_change_thread.start()
    buzzer_interrupt_thread.start()
    # calling the main executble function of the file [main]
    main()

    
