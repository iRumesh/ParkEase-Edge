#!/usr/bin/python3


"""
* declaring package pylogger
* @description this module is initalized for logging process fo this system.
*
"""

"""
* import statement section
* importing module os
* importing module yaml
* from datetime importing method datetime
"""
import os, sys
import yaml
from datetime import datetime

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

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
* declaring function log_instance
* @param str file_suffix
* @return str log_dir
*
"""
def log_instance(file_suffix:str="") -> None:
    # Format the date and time as required
    log_dir = (
        ("/".join(os.path.realpath(__file__).split("/")[0:-3]))
        + r"/log/{A}/".format(A=file_suffix)
        + datetime.now().strftime('build_%Y-%m-%d')
    )

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    return log_dir


"""
* declarng function write_log
* @param string message
* @param string log_dir
* @param string executable_name
* @param string function_name
* @param string log_name
* @param string log_mode: str = "a+"
* @return None
* the main process of this method is to wrote the log files that we going to use for the debug session for this code
*
"""
def write_log(message: str, log_dir:str, executable_name:str, function_name:str, log_name: str, log_mode: str = "a+") -> None:
    from mod.mod import STATUS
    # this function will identify if the logging is enebled or not 
    if config_data["LOG_ENABLE"]:
        # this statement will identify the current mode of the system
        if STATUS:
            with open(r"{A}/{B}".format(A=log_dir, B=log_name), log_mode) as f:
                f.write(
                "{A} - {B} - {C} - INFO - {D}. \n".format(
                        A=(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 
                        B=executable_name,
                        C=function_name,
                        D=message)
                )

