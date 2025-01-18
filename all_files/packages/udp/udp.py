#!/usr/bin/python3


"""
* declaring package udp
* @description Establishes a UDP socket communication setup to send data packets to a designated IP address and port.
*
"""

"""
* import statement section
* importing module socket
* importing module threading
* importing module time
"""
from socket import socket, AF_INET, SOCK_DGRAM


"""
* declaring function create_socket_connection
* @param socket af_inet
* @param socket sock_dgram
* return obj sock (object of class socket)
*
"""
def create_socket_connection(af_inet:socket=AF_INET,
                             sock_dgram:socket=SOCK_DGRAM):
    return socket(af_inet, sock_dgram)

"""
* declaring function disconnect_socket_connection
* @param socket af_inet
* @param socket sock_dgram
* return obj sock (object of class socket)
*
"""
def disconnect_socket_connection(con_scket:socket):
    con_scket.close()


"""
* declaring function cast_udp_packets
* @param str message
* @param socket con_socket
* @param str ip
* @param int port
"""
def  cast_udp_packets(message:str, con_scket:socket, ip:str=None , port:int = None):
    con_scket.sendto(message.encode(), (ip, port))
