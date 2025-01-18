#!/usr/bin/python3


"""
* declaring package log
* @description Establishes a UDP socket communication setup to send data packets to a designated IP address and port.
*
"""


"""
* import statement section
* importing module os
* importing module sys
* importing module pylogger
* importing module pyprint
* importing module parse
* importing module vehicle_passed
* importing module gate
* importing module mod
*
"""
import os, sys
import yaml
import time

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from pylogger import pylogger
from pyprint import pyprint
from parse import parse
from vehicle_passed import vehicle_passed
from gate import gate
from mod import mod

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
* declaring function response_topic_10000
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10000(response, gate_type):
    if mod.STATUS:
        pyprint.print_msg(
            "invalid API key or expired API key",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10000',
        )
        pylogger.write_log("invalid API key or expired API key",
                        executable_name=os.path.basename(__file__),
                        function_name='response_topic_10000',
                        log_name="logger_request_callback_all.log",
                        log_dir=pylogger.log_instance(file_suffix="request_callback")
        )
    else:
        return 0


"""
* declaring function response_topic_10001
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10001(response, gate_type):
    if mod.STATUS:
        pyprint.print_msg(
            "API server error. please contact API team",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10001',
        )
        pylogger.write_log("API server error. please contact API team",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10001',
            log_name="logger_request_callback_all.log",
            log_dir=pylogger.log_instance(file_suffix="request_callback")
        )
    else:
        return 0


"""
* declaring function response_topic_10002
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10002(response, gate_type):
    if mod.STATUS:
        pyprint.print_msg(
            "recive an image error",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10002',
        )
        pylogger.write_log("Image error",
                        executable_name=os.path.basename(__file__),
                        function_name='response_topic_10002',
                        log_name="logger_request_callback_all.log",
                        log_dir=pylogger.log_instance(file_suffix="request_callback")
        )
    else:
        return 0


"""
* declaring function response_topic_10003
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10003(response, gate_type):
    if mod.STATUS:
        pyprint.print_msg(
            "Vehicle plate not detected. change vehicle angle",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10003',
        )
        pylogger.write_log( "Respons code[10003]. Vehicle plate not detected. change vehicle angle",
                        executable_name=os.path.basename(__file__),
                        function_name='response_topic_10003',
                        log_name="logger_request_callback_all.log",
                        log_dir=pylogger.log_instance(file_suffix="request_callback")
        )
    else:
        return 0


"""
* declaring function response_topic_10004
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10004(response, gate_type):
    if mod.STATUS:
        if gate_type:
            parse.sendPacket(
                packet=(parse.codeFailed(10004)),
                UDP_IP=config_data["UDP_IP_IN"],
                UDP_PORT=config_data["UDP_PORT"],
            )
        else:
            parse.sendPacket(
                packet=(parse.codeFailed(10004)),
                UDP_IP=config_data["UDP_IP_OUT"],
                UDP_PORT=config_data["UDP_PORT"],
            )

        pyprint.print_msg(
            "This is OCR error. please change vehicle angle. (Plate not visible clearly)",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10004',
        )
        pylogger.write_log(
            "Respons code[10004]. OCR error, please change vehicle angle. (Plate not visible clearly)",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10004',
            log_name="logger_request_callback_all.log",
            log_dir=pylogger.log_instance(file_suffix="request_callback")
        )
    
        parse.panelReset(
            UDP_IP=config_data["UDP_IP_IN"],
            UDP_PORT=config_data["UDP_PORT"],
        )

        parse.panelReset(
            UDP_IP=config_data["UDP_IP_OUT"],
            UDP_PORT=config_data["UDP_PORT"],
        )

    else:
        return 0


"""
* declaring function response_topic_10005
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10005(response, gate_type):
    if mod.STATUS:
        if gate_type:
            parse.sendPacket(
                packet=(parse.codeFailed(10005)),
                UDP_IP=config_data["UDP_IP_IN"],
                UDP_PORT=config_data["UDP_PORT"],
            )
            pyprint.print_msg(
                response.json()["data"]["reason"],
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10005',
            )
            pylogger.write_log(str(response.json()["data"]["reason"]),
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10005',
                log_name="logger_request_callback_all.log",
                log_dir=pylogger.log_instance(file_suffix="request_callback")
            )
            time.sleep(4)
        else:
            parse.sendPacket(
                packet=(parse.codeFailed(10005)),
                UDP_IP=config_data["UDP_IP_OUT"],
                UDP_PORT=config_data["UDP_PORT"],
            )
            pyprint.print_msg(
                response.json()["data"]["reason"],
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10005',
            )
            pylogger.write_log(str(response.json()["data"]["reason"]),
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10005',
                log_name="logger_request_callback_all.log",
                log_dir=pylogger.log_instance(file_suffix="request_callback")
            )
            time.sleep(4)

        parse.panelReset(
            UDP_IP=config_data["UDP_IP_IN"],
            UDP_PORT=config_data["UDP_PORT"],                               
        )

        parse.panelReset(
            UDP_IP=config_data["UDP_IP_OUT"],
            UDP_PORT=config_data["UDP_PORT"],
        )

    else:
        return 0



"""
* declaring function response_topic_10006
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10006(response, gate_type):
    if mod.STATUS:
        pyprint.print_msg(
            response.json()["data"]["reason"],
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10006',
        )
    else:
        return 0


"""
* declaring function response_topic_10007
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10007(response, gate_type):
    if mod.STATUS:
        pyprint.print_msg(
            "Indication of wrong data detection",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10007',
        )
        pylogger.write_log("Indication of wrong data detection",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10007',
            log_name="logger_request_callback_all.log",
            log_dir=pylogger.log_instance(file_suffix="request_callback")
        )
    else:
        return 0


"""
* declaring function response_topic_10008
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10008(response, gate_type):
    if mod.STATUS:
        if gate_type:
            parse.sendPacket(
                packet=(parse.codeOveride(10008)),
                UDP_IP=config_data["UDP_IP_IN"],
                UDP_PORT=config_data["UDP_PORT"],
            )
            pyprint.print_msg(
                "Already entered Vehicle. The detected vehicle has already Entered the parking lot. Please exit the vehicle using manual mode.",
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10008',
            )

            pylogger.write_log("Already Entered Vehicle {A}. Please exit the vehicle using manual mode.".format(
                A=response.json()["data"]["reason"].split(
                    "Detected Vehicle : "
                )[1]
            ),
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10008',
                log_name="logger_request_callback_all.log",
                log_dir=pylogger.log_instance(file_suffix="request_callback")
            )
            time.sleep(4)

        else:
            parse.sendPacket(
                packet=(parse.codeOveride(10008)),
                UDP_IP=config_data["UDP_IP_OUT"],
                UDP_PORT=config_data["UDP_PORT"],
            )
            pyprint.print_msg(
                "Already Exited Vehicle. The detected vehicle has already Exited the parking lot. Please exit the vehicle using manual mode",
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10008',
            )
            pylogger.write_log("Already Exited Vehicle. The detected vehicle has already Exited the parking lot. Please exit the vehicle using manual mode",
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10008',
                log_name="logger_request_callback_all.log",
                log_dir=pylogger.log_instance(file_suffix="request_callback")
            )
            time.sleep(4)
    
        parse.panelReset(
            UDP_IP=config_data["UDP_IP_IN"],
            UDP_PORT=config_data["UDP_PORT"],
        )

        parse.panelReset(
            UDP_IP=config_data["UDP_IP_OUT"],
            UDP_PORT=config_data["UDP_PORT"],
        )

    else:
        return 0



"""
* declaring function response_topic_10009_12_13_14
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10009_12_13_14(response, gate_type):
    if mod.STATUS:
        # process Success This is gate open signal
        if gate_type:
            spot_id = (
                response.json()["data"]["reason"]
                .split("Spot ID : ")[1]
                .split(". Detected Vehicle : ")[0]
            )

            pyprint.print_msg(
                ("allocated spot id is :", spot_id),
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10009_12_13_14',
            )
            pylogger.write_log(f"Allocated spot id is: {spot_id}",
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10009_12_13_14',
                log_name="logger_request_callback_all.log",
                log_dir=pylogger.log_instance(file_suffix="request_callback")
            )

        detected_vehicle = response.json()["data"]["reason"].split(
            "Detected Vehicle : "
        )[1]
        
        pyprint.print_msg(
            (("Detected Vehicle:", detected_vehicle)),
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10009_12_13_14',
        )
        if gate_type:
            parse.sendPacket(
                packet=(parse.codeSuccess(detected_vehicle, spot_id, 10013)),
                UDP_IP=config_data["UDP_IP_IN"],
                UDP_PORT=config_data["UDP_PORT"],
            )
            time.sleep(4)

        else:
            parse.sendPacket(
                packet=(parse.codeSuccess(detected_vehicle, 1234, 10009)),
                UDP_IP=config_data["UDP_IP_OUT"],
                UDP_PORT=config_data["UDP_PORT"],
            )
            time.sleep(4)

        pylogger.write_log(f"Detected vehicle id is: {detected_vehicle}",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10009_12_13_14',
            log_name="logger_request_callback_all.log",
            log_dir=pylogger.log_instance(file_suffix="request_callback")
        )

        # Open the gate
        if mod.STATUS:
            pyprint.print_msg(
                "Edge controlling is opening the {A} gate".format(
                    A=("IN" if gate_type else "OUT")
                ),
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10009_12_13_14',
            )
            pylogger.write_log("Edge controlling is opening the {A} gate".format(
                A=("IN" if gate_type else "OUT")
            ),
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10009_12_13_14',
                log_name="logger_request_callback_all.log",
                log_dir=pylogger.log_instance(file_suffix="request_callback")
            )
            gate.open_gate()

            # See if vehicle has passed through gate
            if config_data["ENABLE_ULTRASONIC"]:
                vehicle_passed.confirm_vehicle_passed()
            time.sleep(1)

            # Close the gate
            pyprint.print_msg(
                "Edge controlling is closing the {A} gate".format(
                    A=("IN" if gate_type else "OUT")
                ),
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10009_12_13_14',
            )
            pylogger.write_log("Edge controlling is closing the {A} gate".format(
                A=("IN" if gate_type else "OUT")
            ),
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10009_12_13_14',
                log_name="logger_request_callback_all.log",
                log_dir=pylogger.log_instance(file_suffix="request_callback")
            )
            gate.close_gate()
        
        parse.panelReset(
            UDP_IP=config_data["UDP_IP_IN"],
            UDP_PORT=config_data["UDP_PORT"],
        )

        parse.panelReset(
            UDP_IP=config_data["UDP_IP_OUT"],
            UDP_PORT=config_data["UDP_PORT"],
        )

    else:
        return 0



"""
* declaring function response_topic_10010
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10010(response, gate_type):
    if mod.STATUS:
        pyprint.print_msg(
            "exit process faild",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10010',
        )
        pylogger.write_log("exit process faild",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10010',
            log_name="logger_request_callback_all.log",
            log_dir=pylogger.log_instance(file_suffix="request_callback")
        )
    else:
        return 0



"""
* declaring function response_topic_10011
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10011(response, gate_type):
    if mod.STATUS:
        pyprint.print_msg(
            "spot allocation faild for the vehicle {A}".format(
                A=response.json()["data"]["reason"].split("Detected Vehicle : ")[1]
            ),
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10011',
        )
        pylogger.write_log("spot allocation faild for the vehicle {A}".format(
            A=response.json()["data"]["reason"].split("Detected Vehicle : ")[1]
        ),
            executable_name=os.path.basename(__file__),
            function_name='response_topic_10011',
            log_name="logger_request_callback_all.log",
            log_dir=pylogger.log_instance(file_suffix="request_callback")
        )
    else:
        return 0



"""
* declaring function response_topic_10015
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_10015(response, gate_type):
    if mod.STATUS:
            pyprint.print_msg(
                "API code return a faild status!",
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10015',
            )    
            pylogger.write_log("API code return a faild status! {A}".format(
                    A=response.status_code
                ),
                executable_name=os.path.basename(__file__),
                function_name='response_topic_10015',
                log_name="logger_request_callback_all.log",
                log_dir=pylogger.log_instance(file_suffix="request_callback")
            )

            if mod.STATUS:
                parse.sendPacket(
                    packet=(parse.codeOveride(10015)),
                    UDP_IP=config_data["UDP_IP_OUT"],
                    UDP_PORT=config_data["UDP_PORT"],
                )
                pyprint.print_msg(
                    "Not entered vehicle. The vehicle {A} has not entered to the parking lot".format(
                        A=response.json()["data"]["reason"].split("Detected Vehicle : ")[1]
                    ),
                    executable_name=os.path.basename(__file__),
                    function_name='response_topic_10015',
                )
                pylogger.write_log("Not entered vehicle. The vehicle {A} has not entered to the parking lot".format(
                        A=response.json()["data"]["reason"].split("Detected Vehicle : ")[1]
                    ),
                    executable_name=os.path.basename(__file__),
                    function_name='response_topic_10015',
                    log_name="logger_request_callback_all.log",
                    log_dir=pylogger.log_instance(file_suffix="request_callback")
                )
            time.sleep(4)
    
            parse.panelReset(
                UDP_IP=config_data["UDP_IP_IN"],
                UDP_PORT=config_data["UDP_PORT"],
            )

            parse.panelReset(
                UDP_IP=config_data["UDP_IP_OUT"],
                UDP_PORT=config_data["UDP_PORT"],
            )

    else:
        return 0


"""
* declaring function response_topic_otherise
* @param str response
* @param str gate_type
* @param int 
*
"""
def response_topic_otherise(response, gate_type):
    if mod.STATUS:
        pyprint.print_msg(
            "API code return a faild status!",
            executable_name=os.path.basename(__file__),
            function_name='response_topic_otherise',
        )
        pylogger.write_log("API code return a faild status! {A}".format(
                A=response.status_code
            ),
            executable_name=os.path.basename(__file__),
            function_name='response_topic_otherise',
            log_name="logger_request_callback_all.log",
            log_dir=pylogger.log_instance(file_suffix="request_callback")
        )
    else:
        return 0
