


############################################################################################################################################################################







#!/usr/bin/python3
import os
import sys
import yaml
import time
import Jetson.GPIO as GPIO
import tkinter as tk
from tkinter import messagebox


# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-3]))

from packages import gpio
from packages import gate
from packages import pyprint
# from packages import gui


# importing the configuration data
config_data = yaml.load(
    open(
        ("/".join(os.path.realpath(__file__).split("/")[0:-3])) + "/config/config.yaml",
        "r",
    ),
    Loader=yaml.FullLoader,
)


# Function to write tempororay files of GPIO checkboxe confirmations
def write_confirmation_result(result):
    with open('/tmp/gpio_confirmation_result.txt', 'w') as f:
        f.write(result)


def main():
    # initializing the gpio pins
    gpio.declare_gpio()

    pyprint.print_msg(
        "Initializing the testing process of the gpio configuratiion",
        executable_name=os.path.basename(__file__),
        function_name="test_parse_cases",
    )

    pyprint.print_msg(
        "Testing the GPIO output pins, setting all the output pins to HIGH state",
        executable_name=os.path.basename(__file__),
        function_name="test_parse_cases",
    )

    GPIO.output((int(config_data["GATE_MODE_OUT"])), 1)
    GPIO.output((int(config_data["MODE_LED"])), 1)
    GPIO.output((int(config_data["BUZZER_PIN"])), 1)

    time.sleep(3)

    GPIO.output((int(config_data["BUZZER_PIN"])), 0)


    if len(sys.argv) < 2:
        print("Error: Expected input argument not provided.")
        return
    update_seen = sys.argv[1]
    time.sleep(3)  # Simulate some initial processing

    if update_seen == 'prompt':
        root = tk.Tk()  # Create a temporary Tk instance for messagebox
        root.withdraw()  # Hide the root window

        answer = messagebox.askyesno("Prompt", "Testing the GPIO output pins of gate mode, mode LED and buzzer. Did they toggle correctly?")

        root.destroy()  # Destroy the temporary Tk instance after use

        # Logic to write to temporary files of GPIO confirmation data for GPIO pin high stage
        if answer:
            write_confirmation_result('Testing GPIO output pins: Success') 
            # with open('/tmp/gpio_confirmation_result.txt', 'r') as f:  # debug statements
            #     print(f.read())  # Print the content of the file
        else:
            write_confirmation_result('Testing GPIO output pins: Failure')
           

        if answer:
            update_seen = '1'
        else:
            update_seen = '0'

    if update_seen == '1':
        pyprint.print_msg(
            "testing of the GPIO output pins is succesfull",
            executable_name=os.path.basename(__file__),
            function_name="test_parse_cases",
        )

        # # Example usage in GPIO.py
        # confirmation_point = "Testing GPIO output pins"
        # gpio_checkbox_completion(confirmation_point)

        GPIO.output((int(config_data["GATE_MODE_OUT"])), 0)
        GPIO.output((int(config_data["MODE_LED"])), 0)

    elif update_seen == '0':
        print("testing of the GPIO output pins is NOT succesfull")
    

    pyprint.print_msg(
        "Testing the gate controller, setting the GATE OPEN to HIGH state",
        executable_name=os.path.basename(__file__),
        function_name="test_parse_cases",
    )
    gate.open_gate()
    update_seen == 'prompt'

    if len(sys.argv) < 2:
        print("Error: Expected input argument not provided.")
        return
    update_seen = sys.argv[1]
    time.sleep(3)  # Simulate some initial processing

    if update_seen == 'prompt':
        root = tk.Tk()  # Create a temporary Tk instance for messagebox
        root.withdraw()  # Hide the root window

        answer = messagebox.askyesno("Prompt",  "Testing the gate controller. Did it open correctly?")

        root.destroy()  # Destroy the temporary Tk instance after use

        # Logic to write to temporary files of GPIO confirmation data for gate control
        if answer:
            write_confirmation_result('Testing gate controller: Success')
        else:
            write_confirmation_result('Testing gate controller: Failure')

        if answer:
            update_seen = '1'
        else:
            update_seen = '0'

    if update_seen == '1':
        gate.close_gate()
        # confirmation_point = "Testing gate controller"
        # gpio_checkbox_completion(confirmation_point)

    elif update_seen == '0':
        print("Testing the gate controller is NOT succesfull")

    gate.close_gate()
    pyprint.print_msg(
        "Testing the INPUT pin configurations",
        executable_name=os.path.basename(__file__),
        function_name="test_parse_cases",
    )

    pyprint.print_msg(
        "Testing the MOD change button",
        executable_name=os.path.basename(__file__),
        function_name="test_parse_cases",
    )

    while not GPIO.input(int(config_data["GATE_MODE_IN"])):
        time.sleep(0.01)
        if GPIO.input(int(config_data["GATE_MODE_IN"])):
            pyprint.print_msg(
                "MOD change button testing is successfull",
                executable_name=os.path.basename(__file__),
                function_name="test_parse_cases",
            )
            time.sleep(0.01)
            break

    update_seen == 'prompt'

    if len(sys.argv) < 2:
        print("Error: Expected input argument not provided.")
        return
    update_seen = sys.argv[1]
    time.sleep(3)  # Simulate some initial processing

    if update_seen == 'prompt':
        root = tk.Tk()  # Create a temporary Tk instance for messagebox
        root.withdraw()  # Hide the root window

        answer = messagebox.askyesno("Prompt",  "Testing the Mode change function. Did it operate correctly?")

        root.destroy()  # Destroy the temporary Tk instance after use

        # Logic to write to temporary files of GPIO confirmation data for mode change function
        if answer:
            write_confirmation_result('Testing Mode change complete: Success')
        else:
            write_confirmation_result('Testing Mode change complete: Failure')


    pyprint.print_msg(
        "Testing the buzzer interrupt button",
        executable_name=os.path.basename(__file__),
        function_name="test_parse_cases",
    )

    while not GPIO.input(int(config_data["BUTTON_PIN"])):
        time.sleep(0.01)
        if GPIO.input(int(config_data["BUTTON_PIN"])):
            pyprint.print_msg(
                "Buzzer button testing is successfull",
                executable_name=os.path.basename(__file__),
                function_name="test_parse_cases",
            )
            time.sleep(0.01)
            break

    pyprint.print_msg(
        "End of the test cases",
        executable_name=os.path.basename(__file__),
        function_name="test_parse_cases",
    )

    # Final pop window related logic
    update_seen == 'prompt'

    if len(sys.argv) < 2:
        print("Error: Expected input argument not provided.")
    
    update_seen = sys.argv[1]

    time.sleep(1)  # Simulate some initial processing

    if update_seen == 'prompt':
        root = tk.Tk()  # Create a temporary Tk instance for messagebox
        root.withdraw()  # Hide the root window

        answer = messagebox.askyesno(title="Test Case Complete", message="Did 'GPIO_Test' complete successfully?")

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