#!/usr/bin/python3


"""
* declaring package parse
* @description Establishes a UDP msg sending process for the system.
*
"""


"""
* import statement section
* importing module os
* importing module sys
* importing module udp
* importing module pylogger
* importing module msgs
*
"""
import os, sys

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from udp import udp
from pylogger import pylogger
from msgs import msgs

packet = ''


"""
* declaring function codeFailed
* @param int code
* @return None
"""
def codeFailed(code:int):
    # returning lists of key value pairs in the dictionary udp_msgs['code_faild']
    for element_id, element in enumerate(msgs.udp_msgs['code_faild'].keys()):
        # identifying the passed value matches for a value in the seperated value list
        if code == element:
            # if there is a matching value it will be return 
            return msgs.udp_msgs['code_faild'][code]


"""
* declaring function codeOveride
* @param int code
* @return None
"""
def codeOveride(code:int):
    # returning lists of key value pairs in the dictionary udp_msgs['code_overide']
    for element_id, element in enumerate(msgs.udp_msgs['code_overide'].keys()):
        # identifying the passed value matches for a value in the seperated value list
        if code == element:
            # if there is a matching value it will be return 
            return  msgs.udp_msgs['code_overide'][code]
    # othervise it will return text 'invalid attempt'
    return "invalid attempt"


"""
* declaring function codeSuccess
* @param str vehicleID
* @param str spot
* @param int code
* @return str
"""
def codeSuccess(vehicleID:str, spot:str,code:int):
     # returning lists of key value pairs in the dictionary udp_msgs['code_success']
    for element_id, element in enumerate(msgs.udp_msgs['code_success'].keys()):
        # identifying the passed value matches for a value in the seperated value list
        if code == element:
            # above statements will check for a specif code that return from the server and send some text that corresponding to that code 
            if code == 10009:
                pylogger.write_log(f"{vehicleID} Vehicle Leaving Good Bye",
                        executable_name=os.path.basename(__file__),
                        function_name='codeSuccess',
                        log_name="logger_parse_all.log",
                        log_dir=pylogger.log_instance(file_suffix="parse")
                )
                return vehicleID +' Good Bye'
            elif((len(vehicleID) > 0) and (len(spot) > 0)):
                pylogger.write_log(f"{vehicleID} + Parking spot: +{spot}",
                        executable_name=os.path.basename(__file__),
                        function_name='codeSuccess',
                        log_name="logger_parse_all.log",
                        log_dir=pylogger.log_instance(file_suffix="parse")
                )
                return vehicleID +" spot: "+spot
            pylogger.write_log(msgs.udp_msgs['code_success'][code],
                        executable_name=os.path.basename(__file__),
                        function_name='codeSuccess',
                        log_name="logger_parse_all.log",
                        log_dir=pylogger.log_instance(file_suffix="parse")
            )
            # othervise it will return the code from udp_msgs['code_success'][code]
            return msgs.udp_msgs['code_success'][code]


"""
* declaring function sendPacket
* @param str packet
* @param str UDP_IP
* @param str UDP_PORT
* @return None
"""
def sendPacket(packet:str, UDP_IP:str, UDP_PORT:str):
    try:
        # initialize the socket connection for UDP data transfer
        socket = udp.create_socket_connection()
        pylogger.write_log('Established the socket connection to the {A} via port {B}'.format(A=UDP_IP, B=UDP_PORT),
                executable_name=os.path.basename(__file__),
                function_name='sendPacket',
                log_name="logger_parse_all.log",
                log_dir=pylogger.log_instance(file_suffix="parse")
        )
    # this exception will handell the error that can be occured withing the initialzation of the socket connection
    except Exception as e_con:
        pylogger.write_log(e_con,
                executable_name=os.path.basename(__file__),
                function_name='sendPacket',
                log_name="logger_parse_all.log",
                log_dir=pylogger.log_instance(file_suffix="parse")
        )
    
    try:
        # calling the method to cast the UDP packets to the edge side end
        udp.cast_udp_packets(packet, socket, UDP_IP, UDP_PORT)
        pylogger.write_log('Data has been written to the {A} via {B} IP and {C} PORT. DATA: [{D}]'.format(A=socket, B=UDP_IP, C=UDP_PORT, D=packet),
                executable_name=os.path.basename(__file__),
                function_name='sendPacket',
                log_name="logger_parse_all.log",
                log_dir=pylogger.log_instance(file_suffix="parse")
        )
    # this exception will handell the errors that can occure during the transmission of the UDP packets
    except Exception as e_cast:
        pylogger.write_log(e_cast,
                executable_name=os.path.basename(__file__),
                function_name='sendPacket',
                log_name="logger_parse_all.log",
                log_dir=pylogger.log_instance(file_suffix="parse")
        )
    # this method will disconnect the UDP connection that initialize with the edge side
    udp.disconnect_socket_connection(socket)
    pylogger.write_log('Terminated the socket connection to the {A} via port {B}'.format(A=UDP_IP, B=UDP_PORT),
                executable_name=os.path.basename(__file__),
                function_name='sendPacket',
                log_name="logger_parse_all.log",
                log_dir=pylogger.log_instance(file_suffix="parse")
        )
    


"""
* declaring function panelReset
* @param str UDP_IP
* @param str UDP_PORT
* @return None
"""
def panelReset(UDP_IP:str, UDP_PORT:str):
    try:
        # initialize the socket connection for UDP data transfer
        socket = udp.create_socket_connection()
        pylogger.write_log('Established the socket connection to the {A} via port {B}'.format(A=UDP_IP, B=UDP_PORT),
                executable_name=os.path.basename(__file__),
                function_name='panelReset',
                log_name="logger_parse_all.log",
                log_dir=pylogger.log_instance(file_suffix="parse")
        )
    # this exception will handell the error that can be occured withing the initialzation of the socket connection
    except Exception as e_con:
        pylogger.write_log(e_con,
                executable_name=os.path.basename(__file__),
                function_name='panelReset',
                log_name="logger_parse_all.log",
                log_dir=pylogger.log_instance(file_suffix="parse")
        )
    
    try:
        udp.cast_udp_packets("DR", socket, UDP_IP, UDP_PORT)
        pylogger.write_log('Data has been written to the {A} via {B} IP and {C} PORT. DATA: [{D}]'.format(A=socket, B=UDP_IP, C=UDP_PORT, D='DR'),
                executable_name=os.path.basename(__file__),
                function_name='panelReset',
                log_name="logger_parse_all.log",
                log_dir=pylogger.log_instance(file_suffix="parse")
        )
    # this method will disconnect the UDP connection that initialize with the edge side
    except Exception as e_cast:
        pylogger.write_log(e_cast,
                executable_name=os.path.basename(__file__),
                function_name='panelReset',
                log_name="logger_parse_all.log",
                log_dir=pylogger.log_instance(file_suffix="gui")
        )
    # this method will disconnect the UDP connection that initialize with the edge side
    udp.disconnect_socket_connection(socket)
    pylogger.write_log('Terminated the socket connection to the {A} via port {B}'.format(A=UDP_IP, B=UDP_PORT),
                executable_name=os.path.basename(__file__),
                function_name='panelReset',
                log_name="logger_parse_all.log",
                log_dir=pylogger.log_instance(file_suffix="parse")
        )