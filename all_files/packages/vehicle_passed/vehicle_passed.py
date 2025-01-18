#!/usr/bin/python3

"""
* import statement section
* importing module os
* importing module sys
* importing module yaml
* importing module time from package time
* importing module logger
*
"""
import os, sys
import yaml
import time

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from pylogger import pylogger
from pyprint import pyprint
from sonar import sonar
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
* declaring function confirm_vehicle_passed
* @param str None
* @param int
*
"""
def confirm_vehicle_passed():
    pyprint.print_msg(
        "calling confirming vehicle passed",
        executable_name=os.path.basename(__file__),
        function_name='confirm_vehicle_passed',
    )

    start_time = time.time()
    current_time = time.time()
    # Loop until vehicle not started to enter or WAIT_TIME is exceeded
    dist = sonar.distance()
    count = 0

    # this statement will loupe through checking the the calculated time period is less than the config_data['WAIT_TIME']
    while ((current_time - start_time) < config_data['WAIT_TIME']) and (count < 2):
        if mod.STATUS:
            pyprint.print_msg(
                "vehicle not entered",
                executable_name=os.path.basename(__file__),
                function_name='confirm_vehicle_passed',
            )

            dist = sonar.distance()
            pylogger.write_log('Confirm vehicle passed has been called. It returns false [vehicle is not entered]',
                executable_name=os.path.basename(__file__),
                function_name='confirm_vehicle_passed',
                log_name="logger_vehicle_passed_all.log",
                log_dir=pylogger.log_instance(file_suffix="vehicle_passed")
            )
            pylogger.write_log('Meashured distance value from the ultrasonic {A}'.format(A=str(dist)),
                executable_name=os.path.basename(__file__),
                function_name='confirm_vehicle_passed',
                log_name="logger_vehicle_passed_all.log",
                log_dir=pylogger.log_instance(file_suffix="vehicle_passed")
            )

            current_time = time.time()
            count = 0
            # statement will check the current distance is exeed the config_data['THRESHOLD_DIST'] or not
            if dist < config_data['THRESHOLD_DIST']:
                noise = False
                while (count < 2) and noise == False:
                    if mod.STATUS:
                        count += 1
                        dist = sonar.distance()
                        
                        pyprint.print_msg(
                            f"Meashured Distance: {dist}",
                            executable_name=os.path.basename(__file__),
                            function_name='confirm_vehicle_passed',
                        )
                        pylogger.write_log('Meashured distance value from the ultrasonic {A}'.format(A=str(dist)),
                            executable_name=os.path.basename(__file__),
                            function_name='confirm_vehicle_passed',
                            log_name="logger_vehicle_passed_all.log",
                            log_dir=pylogger.log_instance(file_suffix="vehicle_passed")
                        )
                            
                        if (count == 2) and (dist < config_data['THRESHOLD_DIST']):
                            if mod.STATUS:
                                pyprint.print_msg(
                                    "vehicle is entering",
                                    executable_name=os.path.basename(__file__),
                                    function_name='confirm_vehicle_passed',
                                )
                                pylogger.write_log('Confirm vehicle passed has been called. It returns true [vehicle is entering]',
                                    executable_name=os.path.basename(__file__),
                                    function_name='confirm_vehicle_passed',
                                    log_name="logger_vehicle_passed_all.log",
                                    log_dir=pylogger.log_instance(file_suffix="vehicle_passed")
                                )
                                pylogger.write_log('Confirm vehicle passed has been called. Waiting for average time 3 seconds [Average time for a vehicle to enter]',
                                    executable_name=os.path.basename(__file__),
                                    function_name='confirm_vehicle_passed',
                                    log_name="logger_vehicle_passed_all.log",
                                    log_dir=pylogger.log_instance(file_suffix="vehicle_passed")
                                )
                                    
                                time.sleep(config_data['ENTERING_TIME'])

                        elif dist > config_data['THRESHOLD_DIST']:
                            if mod.STATUS:
                                pyprint.print_msg(
                                    "Sensor data has a noise",
                                    executable_name=os.path.basename(__file__),
                                    function_name='confirm_vehicle_passed',
                                )
                                pylogger.write_log('Sensor return a noise data.',
                                    executable_name=os.path.basename(__file__),
                                    function_name='confirm_vehicle_passed',
                                    log_name="logger_vehicle_passed_all.log",
                                    log_dir=pylogger.log_instance(file_suffix="vehicle_passed")
                                )
                                
                                noise = True
                                count = 0
            # statement will check for the timeout and do the corresponding stuff            
            elif (current_time - start_time) > config_data['WAIT_TIME']:
                pyprint.print_msg(
                            f"Function has been timeout after waiting {str(config_data['WAIT_TIME'])}",
                            executable_name=os.path.basename(__file__),
                            function_name='confirm_vehicle_passed',
                )
                pylogger.write_log('Function has been timeout ater waiting {A} seconds'.format(A=str(config_data['WAIT_TIME'])),
                    executable_name=os.path.basename(__file__),
                    function_name='confirm_vehicle_passed',
                    log_name="logger_vehicle_passed_all.log",
                    log_dir=pylogger.log_instance(file_suffix="vehicle_passed")
                )

    count = 0
    while count < 50:
        if mod.STATUS:
            dist = sonar.distance()
            pyprint.print_msg(
                f"sonar reads {dist} of distance",
                executable_name=os.path.basename(__file__),
                function_name='confirm_vehicle_passed',
            )
            pylogger.write_log('Meashured distance value from the ultrasonic {A}'.format(A=str(dist)),
                executable_name=os.path.basename(__file__),
                function_name='confirm_vehicle_passed',
                log_name="logger_vehicle_passed_all.log",
                log_dir=pylogger.log_instance(file_suffix="vehicle_passed")
            )

            if dist > config_data['THRESHOLD_DIST']:
                if mod.STATUS:
                    count += 1

    if not mod.STATUS:
        return 0
        
    pyprint.print_msg(
        "Exiting from the loop",
        executable_name=os.path.basename(__file__),
        function_name='confirm_vehicle_passed',
    )
    pylogger.write_log('Exiting from the loop. EOF of the function call',
        executable_name=os.path.basename(__file__),
        function_name='confirm_vehicle_passed',
        log_name="logger_vehicle_passed_all.log",
        log_dir=pylogger.log_instance(file_suffix="vehicle_passed")
    )

    # returning 0 to initialize the end of function call
    return 0