#!/usr/bin/python3
import sys
import requests
import time
import tkinter as tk
from tkinter import messagebox

def internet_connection():
    try:
        response = requests.get("https://google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

if __name__ == '__main__':
    if internet_connection():
        print("The Internet is connected. Wifi alert testing is done.")
        sys.exit(0)

    else:
        print("The Internet is not connected.")
        sys.exit(1)



# ###################################   This coding part is specifically to generate the pop up window to check the success of the test  ###################################
    
    

# if len(sys.argv) < 2:
#     print("Error: Expected input argument not provided.")

# # update_seen == 'prompt'
# update_seen = sys.argv[1]

# time.sleep(1)  # Simulate some initial processing

# if update_seen == 'prompt':
#     root = tk.Tk()  # Create a temporary Tk instance for messagebox
#     root.withdraw()  # Hide the root window

#     answer = messagebox.askyesno(title="Test Case Complete", message="Did 'WIFI_test' complete successfully?")

#     root.destroy()  # Destroy the temporary Tk instance after use

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


