#!/usr/bin/python3
import requests
import os
import sys
import yaml
import time
import tkinter as tk
from tkinter import messagebox

# declaring package relative import for import sibling directories of the sub package parser
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-3]))

from packages import parse
from packages import pyprint

# importing the configuration data
config_data = yaml.load(
    open(
        ("/".join(os.path.realpath(__file__).split("/")[0:-3])) + "/config/config.yaml",
        "r",
    ),
    Loader=yaml.FullLoader,
)



def main():
    print("Parse Test executed")
    print("Initialization of the testing of led panels")

    # parse.sendPacket(
    #     packet=(parse.codeOveride(10015)),
    #     UDP_IP=config_data["UDP_IP_OUT"],
    #     UDP_PORT=config_data["UDP_PORT"],
    # )

    # parse.sendPacket(
    #     packet=(parse.codeOveride(10015)),
    #     UDP_IP=config_data["UDP_IP_IN"],
    #     UDP_PORT=config_data["UDP_PORT"],
    # )
    parse.panelReset(
        UDP_IP=config_data["UDP_IP_OUT"],
        UDP_PORT=config_data["UDP_PORT"],
    )
    parse.panelReset(
        UDP_IP=config_data["UDP_IP_IN"],
        UDP_PORT=config_data["UDP_PORT"],
    )

    time.sleep(3)

    if len(sys.argv) < 2:
        print("Error: Expected input argument not provided.")
        return

    update_seen = sys.argv[1]

    time.sleep(3)  # Simulate some initial processing

    if update_seen == 'prompt':
        root = tk.Tk()  # Create a temporary Tk instance for messagebox
        root.withdraw()  # Hide the root window

        answer = messagebox.askyesno("Prompt", "Please wait. Can you see any update on those two screens?")

        root.destroy()  # Destroy the temporary Tk instance after use

        if answer:
            update_seen = '1'
        else:
            update_seen = '0'

    if update_seen == '1':
        
        pyprint.print_msg(
            f"Test cases for the panel testing pass",
            executable_name=os.path.basename(__file__),
            function_name="test_parse_cases",
        )


    elif update_seen == '0':
        pyprint.print_msg(
            f"Test cases for the panel testing fail",
            executable_name=os.path.basename(__file__),
            function_name="test_parse_cases",
        )

    update_seen == 'prompt'

    if len(sys.argv) < 2:
        print("Error: Expected input argument not provided.")
    
    update_seen = sys.argv[1]

    time.sleep(1)  # Simulate some initial processing

    if update_seen == 'prompt':
        root = tk.Tk()  # Create a temporary Tk instance for messagebox
        root.withdraw()  # Hide the root window

        answer = messagebox.askyesno(title="Test Case Complete", message="Did 'Parse_Test' complete successfully?")

        root.destroy()  # Destroy the temporary Tk instance after use

        if answer:
            update_seen = '1'
        else:
            update_seen = '0'

    if update_seen == '1':
        print("User confirmed success.")
        sys.exit(0)

    elif update_seen == '0':
        print("User confirmed failure.")
        sys.exit(1)




if __name__ == "__main__":
    main()

