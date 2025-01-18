

#!/usr/bin/python3
import cv2
import requests
import sys
import os
import time
import tkinter as tk
from tkinter import messagebox
import yaml



# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-3]))

# importing the configuration data
config_data = yaml.load(
    open(
        ("/".join(os.path.realpath(__file__).split("/")[0:-3])) + "/config/config.yaml",
        "r",
    ),
    Loader=yaml.FullLoader,
)

#print(config_data)


# Replace with your IP camera details
in_gate_ip = config_data["CAM_URL_ENTRANCE"]
out_gate_ip = config_data["CAM_URL_EXIT"]

# Now you can use both IP addresses in your script
ips = [in_gate_ip, out_gate_ip]
# ips = ["192.168.1.118:8080", "192.168.1.105:8080"]


# print(f"In-Gate IP Camera Address: {in_gate_ip}")
# print(f"Out-Gate IP Camera Address: {out_gate_ip}")
timeout = 10

def check_IP_camera(ip):
    try:
        response = requests.get(f'http://{ip}', timeout=timeout)
        if response.status_code == 200:
            stream_url = f"http://{ip}/video"
            cap = cv2.VideoCapture(stream_url)

            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()

                if ret:
                    cv2.imshow("IP Camera Test", frame)
                    cv2.waitKey(1000)  # Display the frame for 1 second
                    cv2.destroyAllWindows()

                    return True  # Indicate success

    except requests.RequestException as e:
        print(f"Camera test failed for {ip}: {str(e)}")
    except Exception as e:
        print(f"Camera test failed for {ip}: {str(e)}")

    return False  # Indicate failure

def prompt_user(ip):
    root = tk.Tk()  # Creating a temporary Tk instance for messagebox
    root.withdraw()  # Hiding the root window

    answer = messagebox.askyesno(title="Test Case Complete",
                                 message=f"Did 'Camera_test' for {ip} complete successfully?")

    root.destroy()  # Destroy the temporary Tk instance after use

    return answer

def main():
    if len(sys.argv) < 2:
        print("Error: Expected input argument not provided.")
        sys.exit(1)

    update_seen = sys.argv[1]

    all_success = True  # Track overall success

    for ip in ips:
        print(f"Testing camera at {ip}")
        success = check_IP_camera(ip)
        time.sleep(2)  # Give some time for simulate some initial processing

        if update_seen == 'prompt':
            answer = prompt_user(ip)

            if not answer:
                all_success = False
                print(f"User confirmed failure for {ip}.")
            else:
                print(f"User confirmed success for {ip}.")

    sys.exit(0 if all_success else 1)

if __name__ == "__main__":
    main()

