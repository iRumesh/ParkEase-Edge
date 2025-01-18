<h3 align="center">Edge side controlling system of ParkEase</h3>

  <p align="center">
    Automated ParkEase system use license plate recognition and sensors to streamline parking. Drivers simply enter and exit without needing tickets, and pay conveniently with cards, apps, or contactless methods. Real-time information guides drivers to available spaces, while operators benefit from efficient management and revenue collection. 
    <br />

  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#main-directory-structure">Directory Structure</a></li>
        <ul>
            <li><a href="#capture-directory">Capture directory</a></li>
            <li><a href="#executable-directory">Executable directory</a></li>
            <li><a href="#packages-directory">Packages directory</a></li>
        </ul>
        <li>
          <a href="#project-configuration">Project Configuration</a> 
          <ul>
            <li><a href="#config-file">Configuration File</a></li>
          </ul>
        </li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>

  </ol>
</details> 

<!-- ABOUT THE PROJECT -->
## About The Project

### Main directory structure
```
ParkEase-Edge/
├── pyproject.toml
├── Readme.md
├── requirements.txt
├── requirements.txt
├── requirements.sh
├── images/
│   ├── logo.png
│   └── ...
├── capture/
│   ├── entance/
│   ├── exit/
│   └── ...
├── config/
│   ├── __init__.py
│   ├── ...
├── executables/
│   ├── __init__.py
│   └── ...
├── log/
│   ├── __init__.py
│   ├── ...
├── packages/
│   ├── __init__.py
│   ├── ...
└── test/
    ├── __init__.py
    └── ... 
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Capture directory

```
.
├── entrance/
├── exit/
└── from/
    ├── 10.jpg
    ├── ...
    └── 9.jpg

3 directories, 68 files

```
1. entrance/
    
    The capture module is designed to facilitate image capture from gate entering and leaving side cameras and temporary storage until the next iteration. The Capture module initializes the image capturing process, allowing for the retrieval of images from specified IP cameras. Captured images are stored in the "entrance" directory and are retained until the subsequent iteration. This directory provides storage for the images captured from the entering side camera.
 

2. exit/
    
    The capture module is designed to facilitate image capture from gate entering and leaving side cameras and temporary storage until the next iteration. The Capture module initializes the image capturing process, allowing for the retrieval of images from specified IP cameras. Captured images are stored in the "exit" directory and are retained until the subsequent iteration. This directory provides storage for the images captured from the leaving side camera.  
    

3. from/
    
    This directory is used to store images that are utilized for testing the system. These images are kept temporarily in this directory until testing purposes are finalized.
    
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Executable directory

```
.
├── img_capture.py
├── __init__.py
├── main_callable.py
└── response_callback.py

0 directories, 4 files
```
1. img_capture.py
    
    The img_capture function captures images of vehicles entering or exiting a controlled area (potentially for a park and pay system). It first checks a system flag to see if image capture is enabled. If enabled, it differentiates between entrance and exit gates based on a provided parameter. The function then retrieves camera URLs and image paths from a configuration file. Finally, it calls another module (capture) to take pictures and save them to temporary and permanent locations on the system.
  

2. response_callback.py
    
    The `request_callback` function handles sending captured vehicle images to a server. It only runs if the system is in "auto mode." First, it checks if the image file exists. If it does, the function builds a web request with the image data and sends it to a server address. Upon receiving a response, it checks the status code. If successful, the function dives into the response data, looking for a specific "code" field. Depending on this code (likely indicating success, errors, or specific situations), the function calls a corresponding function from another module (`response_topic`) to handle further actions based on the server's response. If there's an error or timeout during the request, the function logs an error message.  
   

3. main_callable.py
   
    The `main_callable` function acts as the program's core. It checks if the system is in "auto mode." If so, it verifies the Wi-Fi connection (optional) and cleans temporary image files. It then captures vehicle images at both the entry and exit points (currently commented out). Finally, it sends these captured images along with gate information (entrance or exit) to a server, likely for further processing (also commented out).  
   
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Packages directory

```
executables/
├── buzzer/
│   ├── __init__.py
│   ├── ...
├── capture/
│   ├── __init__.py
│   ├── ...
├── gate/
│   ├── __init__.py
│   ├── ...
├── gpio/
│   ├── __init__.py
│   ├── ...
├── gui/
│   ├── __init__.py
│   ├── ...
├── mod/
│   ├── __init__.py
│   ├── ...
├── msgs/
│   ├── __init__.py
│   ├── ...
├── parse/
│   ├── __init__.py
│   ├── ...
├── pylogger/
│   ├── __init__.py
│   ├── ...
├── pyprint/
│   ├── __init__.py
│   ├── ...
├── response_topic/
│   ├── __init__.py
│   ├── ...
├── sonar/
│   ├── __init__.py
│   ├── ...
├── udp/
│   ├── __init__.py
│   ├── ...
├── vehicle_passed/
│   ├── __init__.py
│   ├── ...
├── wifi_alert/
│   ├── __init__.py
│   ├── ...
├── __init__.py
```
1. buzzer
    ```
    .
    ├── buzzer.py
    └── __init__.py

    0 directories, 2 files
    ```

   
    This Python script is designed to control a buzzer using the Jetson.GPIO library on a Jetson device. It initializes the GPIO pins, imports necessary modules, and loads configuration data from a YAML file. The script includes two primary functions: `sound_buzzer()` and `stop_buzzer()`. The `sound_buzzer()` function activates the buzzer by setting the GPIO pin to high for a brief period, then turns it off. The `stop_buzzer()` function ensures the buzzer is turned off by setting the GPIO pin to low. Both functions log their actions using the `pylogger` module. This script is useful for managing auditory alerts in an embedded system.
    

2. capture
    ```
    .
    ├── capture.py
    └── __init__.py

    0 directories, 2 files

    ```

    
    This Python script initializes the process of image capturing using an IP camera or by copying existing image files for temporary testing. It imports necessary modules such as os, sys, shutil, cv2 (as cv), yaml, datetime, pylogger, and pyprint. The script reads configuration data from a YAML file (config.yaml) located in the project directory. The capture function is the main process responsible for capturing images from the specified camera URL (CAM_URL) and saving them to temporary locations (image_path_one and optionally image_path_two). It logs events using a custom logging module (pylogger) and prints messages using another custom module (pyprint). Exception handling is implemented to catch and log any errors that occur during the image capturing process. The script also contains commented-out code for capturing images from an IP camera using OpenCV (cv2.VideoCapture), which can be uncommented to enable real-time image capturing from a live camera feed.
    

3. gate
    ```
    .
    ├── gate.py
    └── __init__.py

    0 directories, 2 files
    ```

   
    This Python script is designed to control gate operations (open, close, and stop) using GPIO pins on a Jetson device. It initializes the GPIO pins and imports necessary modules and configuration data from a YAML file. The script provides three main functions: `open_gate()`, `close_gate()`, and `stop_gate()`. These functions activate the gate mechanisms by setting the corresponding GPIO pins to high, waiting for a specified delay, and then setting the pins to low, with logging of each action. This ensures proper timing and logging, facilitating automated gate control and monitoring.
    

4. gpio
    ```
    .
    ├── gpio.py
    └── __init__.py

    0 directories, 2 files
    ```

   
    This Python script is used to initialize the GPIO configuration for an edge controller on a Jetson device. It imports necessary modules and configuration data from a YAML file. The script defines two main functions: `declare_gpio()` and `clear_all_GPIOs()`. The `declare_gpio()` function sets up various GPIO pins for output or input with initial states, configuring them for different functionalities such as gate control, mode indication, buzzer, and ultrasonic sensor pins. The `clear_all_GPIOs()` function sets all output GPIO pins to low, effectively turning off all connected components. This setup ensures the proper initialization and management of GPIO pins for the edge controller's operations.
    

5. gui
    ```
    .
    ├── gui.py
    └── __init__.py

    0 directories, 2 files
    ```

    
    This Python script sets up a basic user interface (UI) using the Tkinter library and logs actions using a custom logging module, `pylogger`. The script imports necessary modules and includes a `usr_gui()` function to initialize and manage the UI. The `usr_gui()` function logs its initialization, creates a main window with a title and specified size, and adds a label, text entry field for an API key, and a save button. The function also handles exceptions by logging any errors encountered during execution. This setup is intended for collecting and saving user input, such as an API key, in a graphical interface.
    

6. mod
    ```
    .
    ├── mod.py
    └── __init__.py

    0 directories, 2 files
    ```


    This Python script is part of a system controlling gate operations and modes (manual or automatic) using GPIO pins on a Jetson device. It imports necessary modules and configuration data from a YAML file and defines several functions to manage different functionalities. The script includes the `manual_mode_indicator()` and `auto_mode_indicator()` functions to control an LED indicating the current mode. The `gate_mode_out_indicator(param)` function sets the state of an output pin based on the mode. The `mode_handler()` function continuously checks for mode change inputs, and the `mode_change_callback()` function updates the system mode and logs the change. The global variable `STATUS` tracks the current mode, with 0 for manual and 1 for automatic. This setup facilitates automated and manual control of gate operations, ensuring proper logging and mode indication.
  

7. msgs
    ```
    .
    ├── msgs.py
    └── __init__.py

    0 directories, 2 files
    ```
    This Python script initializes a dictionary named `udp_msgs` that contains predefined messages for various status codes used in edge-side codes. The dictionary is structured into three categories: `code_faild` (likely a typo for `failed request`), `code_overide` (possibly a typo for `overrided request`), and `successfull request`. Each category maps specific numeric codes to their corresponding messages, such as "Not registered" for code 10005 in `code_faild`, "Exited vehicle" for code 10008 in `code_overide`, and "Invalid attempt" for code 10012 in `code_success`. This setup allows for easy retrieval of descriptive messages based on status codes, facilitating better communication and debugging in the edge controller system.
  

8. parse
    ```
    .
    ├── parse.py
    └── __init__.py

    0 directories, 2 files
    ```

   
    This Python script defines several functions to handle UDP message processing, logging, and socket communication within a system. It begins by importing necessary modules and setting up relative imports for sibling directories. The `codeFailed`, `codeOveride`, and `codeSuccess` functions retrieve and log specific messages based on predefined status codes. The `sendPacket` function establishes a UDP socket connection, sends a data packet to a specified IP and port, logs the process, and then disconnects the socket. Similarly, the `panelReset` function resets the panel by sending a "DR" packet to a specified IP and port. The script uses a logging module, `pylogger`, to document each step and any exceptions encountered during execution, ensuring robust error handling and traceability.
  

9. pylogger
    ```
    .
    ├── pylogger.py
    └── __init__.py

    0 directories, 2 files
    ```


    The `pylogger` module is designed for logging processes in a system, initialized to manage logging throughout a larger project. It imports necessary modules such as `os`, `sys`, `yaml`, and `datetime`, and loads configuration data from a YAML file. The `log_instance` function generates a directory path for log files based on the current date and an optional suffix, ensuring the directory exists. The `write_log` function writes formatted log messages to specified log files, contingent upon whether logging is enabled in the configuration. These functions aid in debugging and monitoring the system's behavior, supporting comprehensive logging practices for operational insights and error management.
   

10. pyprint
    ```
    .
    ├── pyprint.py
    └── __init__.py

    0 directories, 2 files
    ```

    
    The pyprint module provides functionality for printing terminal messages in a system. It imports necessary modules such as os, sys, yaml, and datetime, and loads configuration data from a YAML file. The print_msg function prints formatted messages to the terminal if printing is enabled and the system is in auto mode, as indicated by the STATUS variable. This function helps in displaying informative messages during the execution of processes, aiding in real-time monitoring and debugging of the system.
    

11. response_topic
    ```
    .
    ├── response_topic.py
    └── __init__.py

    0 directories, 2 files
    ```

  
    The Python script handel multiple request that recives from the server side. It imports several modules such as os, sys, yaml, and custom modules like pylogger, pyprint, parse, vehicle_passed, gate, and mod. The config_data is loaded from a YAML configuration file. The script defines multiple functions (response_topic_10000 to response_topic_otherise) to handle different response topics. Each function checks the mod.STATUS before executing. If mod.STATUS is true, it logs messages using pylogger and prints messages using pyprint. It also sends UDP packets using parse.sendPacket() based on the gate_type. If mod.STATUS is false, it returns 0. These functions handle various responses like invalid API keys, server errors, image errors, vehicle plate not detected, OCR errors, spot allocation failures, and API status failures, among others. Each function logs detailed information about the response and performs necessary actions like opening or closing gates and confirming vehicle passage.


12. sonar
    ```
    .
    ├── sonar.py
    └── __init__.py

    0 directories, 2 files
    ```

    
    The Python script configures Jetson Nano GPIO pins to interface with ultrasonic sensors for measuring distances. It imports necessary modules such as Jetson.GPIO for GPIO handling, time for time-related functions, os for operating system interactions, and yaml for configuration data loading. Configuration data is loaded from a YAML file located at config/config.yaml. The GPIO pins for triggering (TRIG_PIN) and receiving (ECHO_PIN) signals from the sensor are set up using GPIO.setup(), with warnings controlled by the configuration setting GPIO_WARNING. The distance() function measures the distance using the ultrasonic sensor. It sets the trigger pin high for a short duration, then calculates the time taken for the echo to return. This time difference is converted into distance in centimeters using the speed of sound formula. 
    

13. udp
    ```
    .
    ├── udp.py
    └── __init__.py

    0 directories, 2 files
    ```

    
    The UDP package script sets up UDP socket communication for sending data packets to a specified IP address and port. It includes functions to establish and disconnect a UDP socket connection, as well as to send UDP packets. The create_socket_connection function initializes a UDP socket based on the provided address family (AF_INET by default) and socket type (SOCK_DGRAM by default). The disconnect_socket_connection function closes the provided socket connection. The cast_udp_packets function sends a provided message as a UDP packet to a specified IP address and port. This setup is ideal for applications that require lightweight and fast communication with minimal overhead, such as real-time data transmission or command signaling in networked systems.
    

14. vehicle_passed
    ```
    .
    ├── vehicle_passed.py
    └── __init__.py

    0 directories, 2 files
    ```

   
    This Python script sets up an environment to monitor vehicle passage using an ultrasonic sensor connected to a Jetson Nano. It imports necessary modules such as os, sys, yaml, and time, and uses custom modules pylogger, pyprint, sonar, and mod. The confirm_vehicle_passed function continuously monitors the ultrasonic sensor for vehicle presence. It retrieves distance measurements using the sonar.distance() function and logs these measurements. The script checks if a vehicle has entered based on the configured THRESHOLD_DIST and WAIT_TIME values. If the sensor detects noise or does not detect a vehicle, it logs this information and continues monitoring. Once a vehicle enters, the script logs the event and waits for an entering time specified in the configuration. The function ends after 50 successful readings of the sensor. If the mod.STATUS is False, the function returns 0 and logs the exit.
  

15. wifi_alert
    ```
    .
    ├── wifi_allert.py
    └── __init__.py

    0 directories, 2 files
    ```

  
    This Python script monitors internet connectivity using a ping check to the IP address 8.8.8.8. It uses GPIO pins on a Jetson Nano to control a buzzer for alerting when no internet connection is detected. The script runs continuously in a separate thread, checking the internet status and triggering the buzzer as needed. It attempts to reconnect to pre-defined Wi-Fi networks from the configuration if the internet is not connected. It logs events using a custom logging module (pylogger) and prints messages using another custom module (pyprint). The script also imports modules for interacting with the buzzer and GPIO. The state of the buzzer is controlled by a CONTROLL_SIGNAL variable, which is set to 1 for active state and 0 for inactive state.
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- PROJECT CONFIGURATION -->
## Project Configuration

Instruction to configure the project.

### Config File

This liine show you how to configure the ultrasonic sensor, that you need to use with the edge side.
* yaml
  ```yaml
  SONAR:
      ECHO_PIN: GPIO pin number (18) where the echo signal of the sonar sensor is connected.
      TRIG_PIN: GPIO pin number (16) where the trigger signal of the sonar sensor is connected.
      THRESHOLD_DIST: Distance threshold value (100) for the sonar sensor, used to determine when an object is detected within a certain range.
  ```

This liine show you how to configure the gate system, that you need to use with the edge side.
* yaml
  ```yaml
  GATE:
      GATE_OPEN_OUT: GPIO pin number (13) used to send a signal to open the gate.
      GATE_CLOSE_OUT: GPIO pin number (15) used to send a signal to close the gate.
      GATE_STOP_OUT: GPIO pin number (37) used to stop the gate's opening or closing process.
      GATE_MODE_IN: GPIO pin number (11) for input signal to identify if the gate is in manual or auto mode.
      GATE_MODE_OUT: GPIO pin number (22) to control the signal for switching the gate control to manual or auto.
  ```

This liine show you how to configure the buzzer and its interrupt button, that you need to use with the edge side.
* yaml
  ```yaml
  BUZZER:
      BUZZER_PIN: GPIO pin number (33) used to control the buzzer.
      BUTTON_PIN: GPIO pin number (23) for the button used to interrupt the buzzer.
  ```

This liine show you how to configure the auto and manual ode indicator, that you need to use with the edge side.
* yaml
  ```yaml
  MODE_INDICATOR:
      MODE_LED: GPIO pin number (38) used for an LED that indicates the current mode of the system.
  ```

This liine show you how to configure the corresponding processes, that you need to use with the edge side.
* yaml
  ```yaml
  TIME:
      GATE_CLOSE_TIME: Time (2.5 seconds) the gate takes to close.
      SWITCH_DELAY: Delay (2 seconds) between switching actions.
      WAIT_TIME: Time (20 seconds) the system waits before closing the gate.
      ENTERING_TIME: Typical time (3 seconds) required for a vehicle to enter through the gate.
  ```

This liine show you how to configure the wifi cameras, that you need to use with the edge side.
* yaml
  ```yaml
  CAMERA:
      CAM_URL_ENTRANCE: URL (http://192.168.23.140:8080/video) for the entrance camera's video feed.
      CAM_URL_EXIT: URL (http://192.168.1.122:8080/video) for the exit camera's video feed.
  ```

This liine show you how to configure the udp communication, that you need to use with the edge side.
* yaml
  ```yaml
  UDP_DATA:
      UDP_IP_IN: IP address (192.168.1.16) assigned for incoming camera data.
      UDP_IP_OUT: IP address (192.168.1.17) assigned for outgoing camera data.
      UDP_PORT: Port number (8888) used for communication with the ESP32 chip via UDP.
  ```

This liine show you how to configure the logging and debuging, that you need to use with the edge side.
* yaml
  ```yaml
  LOGGING AND DEBUGGING:
      LOG_ENABLE: Enable logging (1 for enabled, 0 for disabled).
      PRINT_ENABLE: Enable printing (1 for enabled, 0 for disabled).
      REAL_TIME_SAVING: Enable real-time data saving (1 for enabled, 0 for disabled).
  ```

This liine show you how to configure the gpio warning, that you need to use with the edge side.
* yaml
  ```yaml
  GPIO:
      GPIO_WARNING: Enable GPIO warnings (1 for enabled, 0 for disabled).
  ```

This liine show you how to configure the API communication data, that you need to use with the edge side.
* yaml
  ```yaml
  API KEYS:
      API_KEY_SLT: API key for authentication.
      API_USER_SLT: Username for API access.
      API_DD_SLT: Device descriptor or identifier.
  ```

This liine show you how to configure the status, that you need to use with the edge side.
* yaml
  ```yaml
  STATUS:
      STATE: Current state of the system (1 for auto mode, 0 for manual mode).
      PREVIOUS_STATE: Previous state of the system (1 for auto mode, 0 for manual mode).
  ```

This liine show you how to configure the gate type, that you need to use with the edge side.
* yaml
  ```yaml
  GATE TYPE:
      GATE_TYPE: Type of gate (1 for entry gate, 0 for exit gate).
  ```

This liine show you how to configure the server request waiting time, that you need to use with the edge side.
* yaml
  ```yaml
  SERVER REQUEST:
      REQUEST_TIME_OUT: Time (100 seconds) the system will wait for a server response before timing out.
  ```

This liine show you how to configure the wifi automatic connection, that you need to use with the edge side.
* yaml
  ```yaml
  WIFI ALERT ENABLE:
      WIFI_ALLERT_ENABLE: Enable WiFi alerts (1 for enabled, 0 for disabled).
      WIFI AUTO CONNECT ENABLE:
      WIFI_AUTO_CONNET_ENABLE: Enable auto-connect to WiFi networks (1 for enabled, 0 for disabled).
  ```

This liine show you how to configure the wifi network details, that you need to use with the edge side.
* yaml
  ```yaml
  WIFI NETWORKS:
      NETWORK_A, NETWORK_B, NETWORK_C, NETWORK_D, NETWORK_E: Predefined WiFi networks the system can connect to, each with:
      SSID: The network's name.
      PASSWORD: The password for the network.
  ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Instruction to setting up the project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This liine show you how to install python3, that you need to use the software.
* python
  ```sh
  sudo apt-get update            
  sudo apt-get install python3.6
  ```

This line shows you how to install and update the pip library management tool.
* pip
  ```sh
  sudo apt install python3-pip
  python3 -m pip install --upgrade pip
  ```

This line shows you how to install the virtualenv package using pip library management tool.
* virtualenv
  ```sh
  sudo apt install python3-pip
  python3 -m pip install virtualenv
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation & Execution

1. Cloning the repo from the github
   ```sh
   git clone https://github.com/irumesh/ParkEase-Edge
   ```
2. Create a virtual environment called ``pyenv``
   ```python
   python3.6 -m venv --system-site-packages pyenv
   ```
3. activate the created python environemtn ``pyenv``
   ```sh
   . pyenv/bin/activate
   ```

4. Install the other required packages using ``requirement.txt`` file
   ```python
   python -m pip install -r requirements.txt
   ```
   
3. Run the code
   ```python
   sudo python3 GUI.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


