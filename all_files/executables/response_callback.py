#!/usr/bin/python3


"""
* declaring module response_callback
* @description Establishes the http request process.
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
* importing module requests
* importing module json
* importing module time
* importing module mod
* importing module response_topic
* importing module pyprint
* importing module pylogger
* importing module parse
*
"""
import os, sys
import yaml
import requests
import json
import time

HOME_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, HOME_DIR)

from packages import mod
from packages import response_topic
from packages import pyprint
from packages import pylogger
from packages import parse

# importing the configuration data
config_data_path = os.path.join(HOME_DIR, "config", "config.yaml")
config_data = yaml.load( open(config_data_path, "r"), Loader=yaml.FullLoader )


"""
* declaring function request_callback
* @param str path
* @param int gate_type
* @return int 0
* the main function of this method is generate a http request to the server and call the corresonding response topics module, remove the img files from the temp storage and call the request_callback
* this method going to pass variables like path, gate type
* we use 1 for reprecent in gate and 0for the out gate
* this function is only executed when mod.STATUS is set to true
*
"""
# gate_type 1 for in, 0 for out 'capture/entrance/1.jpg'
def request_callback(path:str='', gate_type: int = 1): 
    # statements that are going to run if the system is running on auto mode 
    if mod.STATUS: 
        # identifying the image availability in the passed path variable 
        if os.path.isfile(path):
            # Prepare the headers
            headers = {
                'api_key': config_data['API_KEY_SLT'],
                'device_id': config_data['API_DD_SLT'],
                'client_name': config_data['API_USER_SLT']
            }

            # headers = {
            #     'API-Key': config_data['API_KEY_SLT'],
            #     'user': config_data['API_USER_SLT'],
            #     'did': config_data['API_DD_SLT'],
            #     'gate': 'in' if gate_type else 'out'
            # }
            
            '''
                Relying solely on server response time for Wi-Fi handling has limitations. 
                We can introduce a delay before assuming a failed request is due to a server issue.
                This delay gives the Wi-Fi connection a chance to recover if a brief disconnection occurred during the request initiation.
                By implementing a timeout with retries or an explicit Wi-Fi check before the request,
                we can improve the system's ability to handle temporary network disruptions.
            '''
            time.sleep(4)# put here 4 second delay to prevent the issue that can be occure with the network disconnection
            
            try:
                # Prepare the request payload
                # files = {'image': open(path, 'rb')}
                files = {'image': ('image.jpg', open(path, 'rb'), 'image/jpeg')}

                if gate_type:
                    # Make the POST request to the server's ENTRANCE_ENDPOINT
                    response = requests.post(config_data['ENDPOINT_ENTRANCE_URL'], headers=headers, files=files, timeout=config_data['REQUEST_TIME_OUT'], verify=False)
                else:
                    # Make the POST request to the server's ENTRANCE_ENDPOINT
                    response = requests.post(config_data['ENDPOINT_EXIT_URL'], headers=headers, files=files, timeout=config_data['REQUEST_TIME_OUT'], verify=False)
            
                # if the request is passing the status code success the process will continue
                if response.status_code == 200:
                    
                    try :
                        available_spots = response.json()["parking_spot_availability"]

                        parse.sendPacket(
                            packet=(
                                f"A: {available_spots['A']} E: {available_spots['E']} F: {available_spots['F']}"
                            ),
                            UDP_IP=config_data["UDP_IP_IN"],
                            UDP_PORT=config_data["UDP_PORT"],
                        )
                    except:
                        pass

                    # here each statement check for a specific response code that going to return from the server side for the passed parameters in the request
                    if response.json()["code"] == 10000:
                        if mod.STATUS:
                            response_topic.response_topic_10000(response, gate_type)
                        
                    elif response.json()["code"] == 10001:
                        if mod.STATUS:
                            response_topic.response_topic_10001(response, gate_type)
                        
                    elif response.json()["code"] == 10002:
                        if mod.STATUS:
                            response_topic.response_topic_10002(response, gate_type)
                        
                    elif response.json()["code"] == 10003:
                        if mod.STATUS:
                            response_topic.response_topic_10003(response, gate_type)
                        
                    elif response.json()["code"] == 10004:
                        if mod.STATUS:
                            response_topic.response_topic_10004(response, gate_type)
                        
                    elif response.json()["code"] == 10005:
                        if mod.STATUS:
                            response_topic.response_topic_10005(response, gate_type)
                        
                    elif response.json()["code"] == 10006:
                        if mod.STATUS:
                            response_topic.response_topic_10006(response, gate_type)
                        
                    elif response.json()["code"] == 10007:
                        if mod.STATUS:
                            response_topic.response_topic_10007(response, gate_type)
                        
                    elif response.json()["code"] == 10008:
                        if mod.STATUS:
                            response_topic.response_topic_10008(response, gate_type)
                        
                    elif (
                        response.json()["code"] == 10009
                        or response.json()["code"] == 10012
                        or response.json()["code"] == 10013
                        or response.json()["code"] == 10014
                    ):
                        if mod.STATUS:
                            response_topic.response_topic_10009_12_13_14(response, gate_type)
                        
                    elif response.json()["code"] == 10010:
                        if mod.STATUS:
                            response_topic.response_topic_10010(response, gate_type)
                        
                    elif response.json()["code"] == 10011:
                        if mod.STATUS:
                            response_topic.response_topic_10011(response, gate_type)
                        
                    elif response.json()["code"] == 10015:
                        if mod.STATUS:
                            response_topic.response_topic_10015(response, gate_type)
                        
                else:
                    if mod.STATUS:
                        response_topic.response_topic_otherise(response, gate_type)

            except requests.exceptions.Timeout:
                pyprint.print_msg(
                    f"request to {config_data['ENDPOINT_URL_1']} timed out after {config_data['REQUEST_TIME_OUT']} seconds.",
                    executable_name=os.path.basename(__file__),
                    function_name='request_callback',
                )
                pylogger.write_log(
                    f"request to {config_data['ENDPOINT_URL_1']} timed out after {config_data['REQUEST_TIME_OUT']} seconds.",
                    executable_name=os.path.basename(__file__),
                    function_name='request_callback',
                    log_name="logger_request_callback_all.log",
                    log_dir=pylogger.log_instance(file_suffix="request_callback")
                )
                return 0

    else:
        return 0

