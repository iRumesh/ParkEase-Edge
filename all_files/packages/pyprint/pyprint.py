#!/usr/bin/python3


"""
* declaring package pyprint
* @description Establishes terminal printing events for this system.
*
"""

"""
* import statement section
* importing module os
* importing module sys
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
* declarng function  print_msg
* @param string message
* @param string executable_name
* @param string function_name
* @retunr None
* the main process of this method is to wrote the terminal outs that occure during the execution of this process
*
"""
def print_msg(message: str, executable_name:str, function_name:str) -> None:
    from mod.mod import STATUS
    # this statement will initialize the print is enabled and also system is runnig on the auto mode
    if ((config_data["PRINT_ENABLE"]) and (STATUS)):
        print(
            "{A} - {B} - {C} - INFO - {D}. \n".format(
                    A=(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 
                    B=executable_name,
                    C=function_name,
                    D=message),
            flush=True
        )

