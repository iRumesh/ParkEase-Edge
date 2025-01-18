#!/usr/bin/python3
import requests
import os, sys
import yaml
import time
import tkinter as tk
from tkinter import messagebox

HOME_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, HOME_DIR)

from packages import pyprint

# importing the configuration data
config_data_path = os.path.join(HOME_DIR, "config", "config.yaml")
config_data = yaml.load( open(config_data_path, "r"), Loader=yaml.FullLoader )

def test_api_cases(gate_type: int):
    # url for request server the parkNpay system
    request_url = config_data['ENDPOINT_URL_1']
    # Prepare the headers
    headers = {
                'api_key': config_data['API_KEY_SLT'],
                'device_id': config_data['API_DD_SLT'],
                'client_name': config_data['API_USER_SLT']
    }

    """
                Relying solely on server response time for Wi-Fi handling has limitations. 
                We can introduce a delay before assuming a failed request is due to a server issue.
                This delay gives the Wi-Fi connection a chance to recover if a brief disconnection occurred during the request initiation.
                By implementing a timeout with retries or an explicit Wi-Fi check before the request,
                we can improve the system's ability to handle temporary network disruptions.
            """
    time.sleep(4)  # put here 4 second delay to prevent the issue that can be occure with the network disconnection

    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "imgs", "1.jpg")

    try:
        # Prepare the request payload
        files = {'image': ('image.jpg', open(file_path, 'rb'), 'image/jpeg')} 

        # Make the POST request to the server
        response = requests.post(config_data['ENDPOINT_ENTRANCE_URL'], headers=headers, files=files, timeout=config_data['REQUEST_TIME_OUT'], verify=False)

        # if the request is passing the status code success the process will continue
        if response.status_code == 200:
            pyprint.print_msg(
            f"request to {request_url} succesfull with code 200. API test Succesfull.",
            executable_name=os.path.basename(__file__),
            function_name="test_api_cases",
        )
            sys.exit(0)

        else:
            pyprint.print_msg(
            f"request to {request_url} unsuccessfull.",
            executable_name=os.path.basename(__file__),
            function_name="test_api_cases",
        )
            sys.exit(1)

    except requests.exceptions.Timeout:
        pyprint.print_msg(
            f"request to {request_url} timed out after {config_data['REQUEST_TIME_OUT']} seconds. API test case Failed.",
            executable_name=os.path.basename(__file__),
            function_name="test_api_cases",
        )

        
    
    # ###################################   This coding part is specifically to generate the pop up window to check the success of the test  ###################################

    # # Update_seen variable is used to communicate between this thread and the main thread to find the best position to pop up the askyesno window
    # if len(sys.argv) < 2:
    #     print("Error: Expected input argument not provided.")

    # update_seen = sys.argv[1]

    # time.sleep(1)  # Simulate some initial processing

    # if update_seen == 'prompt':
    #     root = tk.Tk()  # Creating a temporary Tk instance for messagebox
    #     root.withdraw()  # Hiding the root window

    #     answer = messagebox.askyesno(title="Test Case Complete", message="Did 'API_test' complete successfully?")  # askyesno window to get the user inputs at the end. 

    #     root.destroy()  # Destroy the temporary Tk instance after use
    
    # # Logical parts to decide the user inout and pass the relavant return code to main thread
    #     if answer:
    #         update_seen = '1'
    #     else:
    #         update_seen = '0'

    # if update_seen == '1':
    #     print("User confirmed success.")
    #     sys.exit(0)

    # elif update_seen == '0':
    #     print("User confirmed failure.")
    #     sys.exit(1)

# main function running
if __name__ == '__main__':
    test_api_cases(1)
