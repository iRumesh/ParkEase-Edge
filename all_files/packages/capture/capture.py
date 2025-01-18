#!/usr/bin/python3


"""
* declaring package capture
* @description initialing the process of image capturing.
* image captured in/out from the ip camera and saved in the temp location, processed and deleted.
*
"""


"""
* import statement section
* importing module os
* importing module sys
* importing module shutil
* importing module datetime
* importing modul pylogger
* importing module pyprint
*
"""
import os, sys
import shutil
import cv2 as cv
import yaml
from datetime import datetime


# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from pylogger import pylogger
from pyprint import pyprint


# importing the configuration data
config_data = yaml.load(
    open(
        ("/".join(os.path.realpath(__file__).split("/")[0:-3]))
        + "/config/config.yaml",
        "r",
    ),
    Loader=yaml.FullLoader,
)


"""
* declaring function capture
* @param str CAM_URL
* @param str image_path_one
* @param str image_path_two
* @return None
* the main process of this function is to capture the images via the ip cameras and save them in the temp locations
*
"""
def capture(CAM_URL:str, image_path_one:str, image_path_two:str):
    try:
        pylogger.write_log("Capture function has been called.[Initialized the image capturing process]",
                executable_name=os.path.basename(__file__),
                function_name='capture',
                log_name="logger_capture_all.log",
                log_dir=pylogger.log_instance(file_suffix="capture")
        )
        
        # sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-3]))
        
        # if still precent a file in the temp folder removing it
        if os.path.isfile(((("/".join(os.path.realpath(__file__).split("/")[0:-3]))
            + image_path_one))):
                os.remove(
                    ((("/".join(os.path.realpath(__file__).split("/")[0:-3]))
                + image_path_one))
        )

        
        if config_data['CAM_ENABLE']:
            # to use the wifi cameras we need to uncomment those parts from here 
            
            camera = cv.VideoCapture(CAM_URL)

            # Capture a frame
            ret, frame = camera.read()

            # Save the frame at path at project director as Entrance.jpg

            cv.imwrite(
                ((("/".join(os.path.realpath(__file__).split("/")[0:-3]))
                + image_path_one))
                , frame
            )
                
            cv.imwrite(
                ((("/".join(os.path.realpath(__file__).split("/")[0:-3]))
                + image_path_two + datetime.now().strftime('build_%Y-%m-%d') +'.jpg'))
                , frame
            )
            
            # to here 
            
            
        else:        
            # and coment the statements from here 
            
            # coping files for temperory testing
            shutil.copyfile(
                (("/".join(os.path.realpath(__file__).split("/")[0:-3]))
                + "/capture/1.jpg"),
                ((("/".join(os.path.realpath(__file__).split("/")[0:-3]))
                + image_path_one))
            )
            if config_data['REAL_TIME_SAVING']:
                shutil.copyfile(
                    (("/".join(os.path.realpath(__file__).split("/")[0:-3]))
                    + "/capture/1.jpg"),
                    ((("/".join(os.path.realpath(__file__).split("/")[0:-3]))
                    + image_path_two + (datetime.now().strftime('build_%Y-%m-%d_%H-%M-%S_%f')[:-3]) +'.jpg'))
                )
            
            # to here
        
        pyprint.print_msg(
            "End of capturing process",
            executable_name=os.path.basename(__file__),
            function_name='capture',
        )
        
    # wrote an exception to check if there is any error in the image capturing process
    except Exception as e_capture:
        pylogger.write_log(e_capture,
                executable_name=os.path.basename(__file__),
                function_name='capture',
                log_name="logger_capture_all.log",
                log_dir=pylogger.log_instance(file_suffix="capture")
        )
