#!/usr/bin/python3


"""
* declaring module img_capture
* @description Establishes image capturing process for the main system.
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
* importing module pylogger
* importing module pyprint
* importing module capture
* importing module mod
*
"""
import os, sys
import yaml

HOME_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, HOME_DIR)

from packages import pylogger
from packages import pyprint
from packages import capture
from packages import mod

# importing the configuration data
config_data_path = os.path.join(HOME_DIR, "config", "config.yaml")
config_data = yaml.load( open(config_data_path, "r"), Loader=yaml.FullLoader )

"""
* declaring function img_capture
* @param int gate_type
* @return None
* the main function of this method is call the capture module
* this method going to pass variables like CAM_URL, image_path_one, image_path_two
* image_path_one and image_path_two are hard coded
* the variable CAM_URL is taking data from the configuration array
* this function is only executed when mod.STATUS is set to true
*
"""
def img_capture(gate_type:int):
    # statements that are going to run if the system is running on auto mode
    if mod.STATUS:
        pylogger.write_log("Entering to image capture loop",
            executable_name=os.path.basename(__file__),
            function_name='img_capture',
            log_name="logger_img_capture_all.log",
            log_dir=pylogger.log_instance(file_suffix="img_capture")
        )
        # the ststements that going to work if the camera is entrance side camera
        if gate_type:
            pyprint.print_msg(
                "Capturing from in gate",
                executable_name=os.path.basename(__file__),
                function_name='img_capture',
            )
            pylogger.write_log("Capturing from in gate",
                executable_name=os.path.basename(__file__),
                function_name='img_capture',
                log_name="logger_img_capture_all.log",
                log_dir=pylogger.log_instance(file_suffix="img_capture")
            )
            
            # calling the process of capturing the images
            # withe passed parameters of camera url, image path one[the temporary path] and image path two[the path that going to save the image permantly]
            capture.capture(CAM_URL=config_data['CAM_URL_ENTRANCE'],
                            image_path_one='/capture/entrance/1.jpg',
                            image_path_two='/capture/all_captures/')

        # the ststements that going to work if the camera is leaving side camera
        else:
            pyprint.print_msg(
                "Capturing from out gate",
                executable_name=os.path.basename(__file__),
                function_name='img_capture',
            )
            pylogger.write_log("Capturing from out gate",
                executable_name=os.path.basename(__file__),
                function_name='img_capture',
                log_name="logger_img_capture_all.log",
                log_dir=pylogger.log_instance(file_suffix="img_capture")
            )
            # calling the process of capturing the images
            # withe passed parameters of camera url, image path one[the temporary path] and image path two[the path that going to save the image permantly]
            capture.capture(CAM_URL=config_data['CAM_URL_EXIT'],
                            image_path_one='/capture/exit/1.jpg',
                            image_path_two='/capture/all_captures/')
    
    return 0