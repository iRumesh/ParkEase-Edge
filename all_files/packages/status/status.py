#!/usr/bin/python3



"""
* import statement section
* importing module os
* importing module sys
* importing module yaml
*
"""
import os, sys
import yaml

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

# current configuration STATUS that used to switch between AUTO and MANUAL mode in the system
STATUS = [int(config_data["STATE"])]