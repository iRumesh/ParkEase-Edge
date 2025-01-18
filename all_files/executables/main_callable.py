#!/usr/bin/python3


"""
* declaring module main_callable
* @description Establishes the excution of main programme.
* @author [Saneth Sachintha Kalhara, ]
* @modified by Saneth Sachintha Kalhara
* @created 17/04/2024
* @modified 17/04/2024
*
"""


"""
* import statement section
* importing module os
* importing module sys
* importing module yaml
* importing module shutil
* importing module time
* importing module Jetson.GPIO
* importing module mod
* importing module pylogger
* importing module pyprint
* importing module wifi_alert
* importing module vehicle_check
* importing module response_callback
* importing module img_capture
*
"""
import os, sys
import yaml
import shutil
import time
import Jetson.GPIO as GPIO

HOME_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, HOME_DIR)

from packages import mod
from packages import pylogger
from packages import pyprint
from packages import wifi_alert
from packages import vehicle_check
from executables import response_callback
from executables import img_capture

# importing the configuration data
config_data_path = os.path.join(HOME_DIR, "config", "config.yaml")
config_data = yaml.load( open(config_data_path, "r"), Loader=yaml.FullLoader )


"""
* declaring function main_callable
* @param None
* @return int 0
* the main function of this method is call the img_capture module, remove the img files from the temp storage and call the request_callback
* this method going to pass variables like file_path, gate type
* image_path and gate type are hard coded
* we use 1 for reprecent in gate and 0for the out gate
* this function is only executed when mod.STATUS is set to true
*
"""
def main_callable():
    # statements that are going to run if the system is running on auto mode
    if mod.STATUS:
        # this statement going to check if there is a issue with the wifi connection
        if wifi_alert.is_internet_connected():    
            pylogger.write_log(
                "System has been entered to the main loop",
                executable_name=os.path.basename(__file__),
                function_name='main_callable',
                log_name="logger_main_callable_all.log",
                log_dir=pylogger.log_instance(file_suffix="main_callable")
            )

            # if there is a file calle [1.jpg] in the temp location called 'capture/entrance' it will be deleted
            if os.path.isfile(
                'capture/entrance/1.jpg'
            ):
                os.remove(
                    'capture/entrance/1.jpg'
                )

            # if there is a file calle [1.jpg] in the temp location called 'capture/exit' it will be deleted
            if os.path.isfile(
                'capture/exit/1.jpg'
            ):
                os.remove(
                    'capture/exit/1.jpg'
                )

            if config_data['CAM_ENABLE']:
                # to use the entering side camera we need to use 1, to use the leaving side camera we need to use 0
                # calling the image capture process for park entering side
                img_capture.img_capture(1)
                # initializing the server request with the data saved in the temp location [capture/entrance] with the gate_type = 1
                if mod.STATUS and os.path.isfile('capture/entrance/1.jpg'):
                    if vehicle_check.detect_vehicle('capture/entrance/1.jpg',1):
                        response_callback.request_callback(
                            'capture/entrance/1.jpg',
                            1
                        )
                
                time.sleep(3)

                # calling the image capturing process for park leaving side
                img_capture.img_capture(0)
                # initializing the server request with the data saved in the temp location [capture/exit] with the gate_type = 0
                if mod.STATUS and os.path.isfile('capture/exit/1.jpg'):
                    if vehicle_check.detect_vehicle('capture/exit/1.jpg',0):
                        response_callback.request_callback(
                            'capture/exit/1.jpg', 
                            0
                        )

            else:
                # this line implement for testing the code

                if os.path.isfile(
                    'capture/1.jpg'
                ):
                    os.remove(
                        'capture/1.jpg'
                    )

                if mod.STATUS:

                    for img_number in range(1, 69, 1):
                        pyprint.print_msg(
                            f"sending vehicle no: {img_number}",
                            executable_name=os.path.basename(__file__),
                            function_name='main_callable',
                        )
                        shutil.copyfile(
                            (("/".join(os.path.realpath(__file__).split("/")[0:-2]))
                            + f"/capture/from/{img_number}.jpg"),
                            ((("/".join(os.path.realpath(__file__).split("/")[0:-2]))
                            + '/capture/1.jpg'))
                        )

                        img_capture.img_capture(1)
                        # initializing the server request with the data saved in the temp location [capture/entrance] with the gate_type = 1
                        if mod.STATUS and os.path.isfile('capture/entrance/1.jpg'):
                            if vehicle_check.detect_vehicle('capture/entrance/1.jpg',1):
                                response_callback.request_callback(
                                    'capture/entrance/1.jpg',
                                    1
                                )
                    
                        time.sleep(3)

                        img_capture.img_capture(0)
                        # initializing the server request with the data saved in the temp location [capture/exit] with the gate_type = 0
                        if mod.STATUS and os.path.isfile('capture/exit/1.jpg'):
                            if vehicle_check.detect_vehicle('capture/exit/1.jpg',0):
                                response_callback.request_callback(
                                        'capture/exit/1.jpg', 
                                        0
                                    )

                # code testing ends here 


        if not mod.STATUS:
            return 0