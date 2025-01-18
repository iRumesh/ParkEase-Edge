#!/usr/bin/python3


"""
* declaring package msgs
* @description initializing the msgs for edge side codes
* Messages are used to send the status of the edge side to the LED Panel
"""

udp_msgs = {
        'code_faild':{
            10005:'Not registered',
            10004:'Change the angle',
            10003: 'No plate detected',
        },
        'code_overide':{
            10008:'Exited vehicle',
            10015:'No Vehicle entry',
            10009:'Safe journey',
            10020:'PF',
        },
        'code_success':{
            10012:'Invalid attempt',
            10013:'Invalid attempt',
            10014:'Invalid attempt',
            10009:'Safe journey',
        },
}