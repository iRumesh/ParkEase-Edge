import tkinter as tk
import subprocess
import os
import queue
import threading
import sys
import time
import yaml
from tkinter import messagebox, simpledialog, Toplevel
from PIL import Image, ImageTk
import Jetson.GPIO as GPIO
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml import YAML
from tkinter import PhotoImage
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)



HOME_DIR = os.path.dirname(os.path.abspath(__file__))
PKG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_files")

# declaring package relative import for import sibiling directories of the sub package parser
sys.path.insert(1, PKG_DIR)

from packages import status
from packages import pylogger
from packages import pyprint
from packages import gpio
from packages import mod
from packages import gate
from packages import wifi_alert
from packages import vehicle_passed
from packages import parse
from executables import main_callable
from gui import spot


# importing the configuration data
config_data_path = os.path.join(HOME_DIR, "all_files", "config", "config.yaml")
config_data = yaml.load(open(config_data_path, "r"), Loader=yaml.FullLoader)

# # app icon path declaration
icon_path = os.path.join(HOME_DIR, "all_files",'gui','images', 'logo.png')

gpio.declare_gpio()



###############################  Declaring paths to find the relavant scripts for the functions of the GUI  ###############################


# Get the script's directory
script_dir = os.path.join(HOME_DIR,"all_files",'gui')
os.chdir(script_dir)

# Path to the folder containing the other Python scripts
scripts_path = os.path.join(script_dir,'tests')

# Custom path to the folder containing b.py
auto_mode_path = script_dir
settings_mode_path = script_dir
spot_mode_path = script_dir

# Footer LOGO paths
logo1_path = os.path.join(script_dir,'images', '1.png')
logo2_path = os.path.join(script_dir,'images', '2.png')
logo3_path = os.path.join(script_dir,'images', '3.png')
correct_image_path = os.path.join(script_dir, 'images', 'correct.png')
wrong_image_path = os.path.join(script_dir, 'images', 'wrong.png')

# icon_image = Image.open("logo.JPG")
# photo = ImageTk.PhotoImage(icon_image)
# Assuming the icon file is in the same directory as the script
# icon_path = "/home/slt/dev_gui/park_n_pay_edge_ws/1.png"  # Replace with your actual icon filename


# Add the custom path to sys.path
sys.path.append(auto_mode_path)
sys.path.append(settings_mode_path)
sys.path.append(spot_mode_path)
try:
    import auto
    import settings
    import spot

except ImportError:
    print(f"auto.py not found in {auto_mode_path}")
    print(f"settings.py not found in {settings_mode_path}")
    print(f"spot.py not found in {spot_mode_path}")



# Queue to store the output from main.py and other threads' outputs
output_queue = queue.Queue()


# Color Palette
bg_color = "#666666" #"#666666"  #"#333333"  "#505050"  
upper_btn_bg_color= "#25416F"
frame_bg_color = "#505050" #"#121212" #"#505050"
bg_root = "#121212"
display_bg_color =  "#C5E8FC"  #"#121212" #"#C5E8FC"  #"#000000" #"#FFFFFF"  #"#C5E8FC"  #"#DDDDDD"
nav_bg_color = "#d9d9d9"
btn_bg_color = "#286EB1"
btn_fg_color = "#ffffff"
text_fg_color = "#121212"
highlight_color = "#ff9800"

# declaring the security frame as global
security_window = None


###############################  Functions to run the main.py, parse test, GPIO test cases in a seperate thread due to  user input requirenments ###############################



# Function to run gpio_test_cases.py in a separate thread
def c_test_function():
    script_name = "gpio_test_cases.py"
    script_path = os.path.join(scripts_path, script_name)

    def capture_output():
        try:
            # Open subprocess and communicate input
            process = subprocess.Popen(
                ["python3", "-u", script_path, "prompt"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                universal_newlines=True
            )

            for line in process.stdout:
                output_queue.put(line.strip())
                if "Prompt:" in line:
                    user_input = simpledialog.askstring("User Input", line.strip())
                    process.stdin.write(user_input + "\n")
                    process.stdin.flush()

            process.wait()  # Wait for the process to complete
        except Exception as e:
            output_queue.put(f"Error: {str(e)}")

    output_thread = threading.Thread(target=capture_output)
    output_thread.start()

    return output_thread


# Function to run parse_test_cases.py in a separate thread
def a_test_function():
    script_name = "parse_test_cases.py"
    script_path = os.path.join(scripts_path, script_name)

    def capture_output():
        try:
            # Open subprocess and communicate input
            process = subprocess.Popen(
                ["python3", "-u", script_path, "prompt"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                universal_newlines=True
            )

            for line in process.stdout:
                output_queue.put(line.strip())
                if "Prompt:" in line:
                    user_input = simpledialog.askstring("User Input", line.strip())
                    process.stdin.write(user_input + "\n")
                    process.stdin.flush()

            process.wait()  # Wait for the process to complete
        except Exception as e:
            output_queue.put(f"Error: {str(e)}")

    output_thread = threading.Thread(target=capture_output)
    output_thread.start()

    return output_thread


# Function to run main.py in a separate thread
# def main_thread_function():
    script_name = "main.py"
    script_path = os.path.join(scripts_path, script_name)

    def capture_output():
        try:
            process = subprocess.Popen(
                ["python3", "-u", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            for line in process.stdout:
                output_queue.put(line.strip())

            for line in process.stderr:
                output_queue.put(line.strip())

            process.wait() 
        except Exception as e:
            output_queue.put(f"Error: {str(e)}")

    output_thread = threading.Thread(target=capture_output)
    output_thread.start()

    return output_thread




###############################  Other functions required for GUI to perform tasks such as update screen, Gate control, running scripts, etc. ###############################




def lower_all_frames():
    auto_mode_frame.lower()
    spot_mode_frame.lower()
    # lower_settings_frame()  # Lower the settings/security window too
    settings_mode_frame.lower()

# Function to periodically update the display with output from the queue
def update_output_display():
    while not output_queue.empty():
        message = output_queue.get_nowait()
        update_display(message)
    root.after(50, update_output_display)  # Check the queue every 50 milliseconds. Frequency can be changed.


# Auto mode frame
def b_indicator():
    update_display("Auto mode activated")
    lower_all_frames()
    auto_mode_frame.lift()
    # show_frame(auto_frame)


# Spot frame
def spot_frame():
    update_display("Spot Allocation Mode activated")
    lower_all_frames()
    spot_mode_frame.lift()


# Manual mode frame
def manual_mode_indicator():
    update_display("Testing Mode activated")
    lower_all_frames()

    # auto_mode_frame.lower()
    # lower_settings_frame()    
    # spot_mode_frame.lower()
    # show_frame(manual_frame)


# Gate open functions manual
def open_gate():
    gate.open_gate()
    update_display("Gate opened")


# Gate close function manual
def close_gate():
    gate.close_gate()
    update_display("Gate closed")



# Pop up window when closing the GUI
def on_closing():
    if messagebox.askyesno(title="Quit?", message="Do you want to quit?"):
        root.destroy()


# Global stop event and process list
stop_event = threading.Event()
processes = []

def run_script(script_name):
    script_path = os.path.join(scripts_path, script_name)
    # print(f'{script_path}')  # Debug print statement

    def capture_output():
        was_stopped = False
        try:
            process = subprocess.Popen(
                ["python3", "-u", script_path, "prompt"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                universal_newlines=True
            )
            processes.append(process)

            output = ""
            for line in process.stdout:
                if stop_event.is_set():
                    was_stopped = True
                    break  # Exit the loop if the stop event is set

                output += line
                output_queue.put(line.strip())
                if "Prompt:" in line:
                    user_input = simpledialog.askstring("User Input", line.strip())
                    process.stdin.write(user_input + "\n")
                    process.stdin.flush()

            if was_stopped:
                process.terminate()
                output_queue.put(f"Script {script_name} was manually stopped.")
            else:
                process.communicate()  # Wait for the process to complete
                return_code = process.returncode
                # print(return_code)
                check_script_completion(return_code, script_name)

        except Exception as e:
            output_queue.put(f"Error: {str(e)}")

    output_thread = threading.Thread(target=capture_output)
    output_thread.start()
    return output_thread



def stop_scripts():
    stop_event.set()  # Signal all threads to stop
    for process in processes:
        process.terminate()  # Terminate all running processes
    processes.clear()  # Clear the list of processes
    # output_queue.put("All running scripts have been stopped.")
    
    # Reset the stop event for future scripts
    stop_event.clear()

def start_new_script(script_name):
    stop_event.clear()  # Clear the stop event before starting a new script
    run_script(script_name)




# function to check the completion of testing scripts
def check_script_completion(return_code, script_name):
    if return_code == -15:
        # If the script was manually stopped, do not update the checkboxes
        output_queue.put(f"Test case '{script_name}' was manually stopped. Test case did not complete.")
        return
    
    else:
        
        if return_code == 0:
            # update_checkbox(script_name)
            checkbox_var = get_checkbox_var(script_name)
            checkbox_var_fail = get_checkbox_var_fail(script_name)
            checkbox_var.set(1)  # Set the success checkbox to be checked (1)
            checkbox_var_fail.set(0)
            checkbox_widget = get_checkbox_widget_success(script_name)
            checkbox_widget.config(bg='green')  # Set the background color to green for success
            fail_checkbox_widget = get_checkbox_widget_fail(script_name)
            fail_checkbox_widget.config(bg=frame_bg_color)

        else:
            messagebox.showerror("Test Case Failed", f"The test case '{script_name}' failed.")
            checkbox_var_fail = get_checkbox_var_fail(script_name)
            checkbox_var = get_checkbox_var(script_name)
            checkbox_var_fail.set(1)
            checkbox_var.set(0)
            checkbox_widget =  get_checkbox_widget_fail(script_name)
            checkbox_widget.config(bg='red')  # Set the background color to red for failure
            fail_checkbox_widget = get_checkbox_widget_success(script_name)
            fail_checkbox_widget.config(bg=frame_bg_color)





# Update the mini display of GUI
def update_display(message):
    display_text.config(state=tk.NORMAL)  # Enable editing the Text widget
    display_text.insert(tk.END, message + "\n\n")  # Insert the message with a newline
    display_text.config(state=tk.DISABLED)  # Disable editing to make it read-only
    display_text.yview(tk.END)  # Scroll to the bottom

spot.initialize(update_display)

# Function to highlight the selected button
def highlight_button(selected_button):
    # Reset the appearance of all buttons first
    auto_button.config(relief=tk.RAISED, bg=upper_btn_bg_color)
    manual_button.config(relief=tk.RAISED, bg=upper_btn_bg_color)
    settings_button.config(relief=tk.RAISED, bg=upper_btn_bg_color)
    spot_button.config(relief=tk.RAISED, bg=upper_btn_bg_color)

    # clear_button.config(relief=tk.RAISED, bg=upper_btn_bg_color)
    
    # Highlight the selected button
    selected_button.config(relief=tk.SUNKEN, bg="lightblue")  # Change the color to your preference


def clear_display_and_checkboxes():
    # Clear the text display
    display_text.config(state=tk.NORMAL)  # Enable editing
    display_text.delete('1.0', tk.END)  # Delete all text
    display_text.config(state=tk.DISABLED)  # Disable editing again

    # Mapping of script names to their respective variables for success and failure checkboxes
    script_var_map = {
        "api_test_cases.py": btn1_var,
        "parse_test_cases.py": btn9_var,
        "sonar_test_cases.py": btn5_var,
        "wifi_test_cases.py": btn6_var,
        "gpio_test_cases.py": btn3_var,
        "camera_test_cases.py": btn2_var,
        "buzzer_test_var": buzzer_test_var, 
        "gate_test_var": gate_test_var,
        "mode_change_var": mode_change_var,
    }

    script_var_fail_map = {
        "api_test_cases.py": btn1_fail,
        "parse_test_cases.py": btn9_fail,
        "sonar_test_cases.py": btn5_fail,
        "wifi_test_cases.py": btn6_fail,
        "gpio_test_cases.py": btn3_fail,
        "camera_test_cases.py": btn2_fail,
        "buzzer_test_var_fail": buzzer_test_var_fail, 
        "gate_test_var_fail": gate_test_var_fail,
        "mode_change_var_fail": mode_change_var_fail,
    }

    # Uncheck all checkboxes in both maps and reset their background colors
    for script_name, var in script_var_map.items():
        var.set(0)  # Uncheck the checkbox
        checkbox_widget = get_checkbox_widget_success(script_name)
        if checkbox_widget:  # Ensure the widget exists
            checkbox_widget.config(bg=frame_bg_color)  # Reset to the original background color

    for script_name, var in script_var_fail_map.items():
        var.set(0)  # Uncheck the checkbox
        checkbox_widget = get_checkbox_widget_fail(script_name)
        if checkbox_widget:  # Ensure the widget exists
            checkbox_widget.config(bg=frame_bg_color)  # Reset to the original background color
    
    gpio_check_01.config(bg=frame_bg_color)
    gpio_check_02.config(bg=frame_bg_color)
    gpio_check_03.config(bg=frame_bg_color)
    gpio_check_01_fail.config(bg=frame_bg_color)
    gpio_check_02_fail.config(bg=frame_bg_color)
    gpio_check_03_fail.config(bg=frame_bg_color)



# Function to execute different python scripts and update the display
def execute_and_update(script_name, btn_text, success=False):
    update_display(f"{btn_text} executed")
    output_thread = run_script(script_name)

    def check_completion(): #checking completion of the code for checkbox
        if output_thread.is_alive():
            root.after(1000, check_completion)  
        else:
            if success:
                update_checkbox(script_name)

    check_completion()


def get_checkbox_widget_success(script_name):
    checkbox_name_success = {
        "api_test_cases.py": btn3_check,
        "parse_test_cases.py": btn4_check,
        "sonar_test_cases.py": btn5_check,
        "wifi_test_cases.py": btn1_check,
        "gpio_test_cases.py": btn2_check,
        "camera_test_cases.py": btn6_check,


    }
    return checkbox_name_success.get(script_name)  # Assuming you have a dictionary mapping script_name to widgets

def get_checkbox_widget_fail(script_name):
    checkbox_name_fail = {
        "api_test_cases.py": btn3_check_fail,
        "parse_test_cases.py": btn4_check_fail,
        "sonar_test_cases.py": btn5_check_fail,
        "wifi_test_cases.py": btn1_check_fail,
        "gpio_test_cases.py": btn2_check_fail,
        "camera_test_cases.py": btn6_check_fail,


    }
    return checkbox_name_fail.get(script_name)  # Assuming you have a dictionary mapping script_name to widgets



# Function to update the checkboxes of the GPIO stages automatically
def update_checkboxes():
    # print("working")
    result = read_confirmation_result()
    
    if result:
        if "Success" in result:
            if "GPIO output pins" in result:
                # print("working")
                buzzer_test_var.set(1)
                buzzer_test_var_fail.set(0)
                gpio_check_01.config(bg='green')
                gpio_check_01_fail.config(bg=frame_bg_color)


            elif "gate controller" in result:
                gate_test_var.set(1)
                gate_test_var_fail.set(0)
                gpio_check_02.config(bg='green')
                gpio_check_02_fail.config(bg=frame_bg_color)


            elif "Mode change complete" in result:
                mode_change_var.set(1)
                mode_change_var_fail.set(0) 
                gpio_check_03.config(bg='green')
                gpio_check_03_fail.config(bg=frame_bg_color)

 

        if "Failure" in result:
            if "GPIO output pins" in result:
                # print("working")
                buzzer_test_var_fail.set(1)
                buzzer_test_var.set(0)
                gpio_check_01_fail.config(bg='red')
                gpio_check_01.config(bg=frame_bg_color)



            elif "gate controller" in result:
                gate_test_var_fail.set(1)
                gate_test_var.set(0)
                gpio_check_02_fail.config(bg='red')
                gpio_check_02.config(bg=frame_bg_color)


            elif "Mode change complete" in result:
                mode_change_var_fail.set(1)
                mode_change_var.set(0)
                gpio_check_03_fail.config(bg='red')
                gpio_check_03.config(bg=frame_bg_color)

  
    root.after(1000, update_checkboxes)  # Check every second



def update_checkbox(script_name):
    try:
        # Retrieve the checkbox variables
        checkbox_var = get_checkbox_var(script_name)
        checkbox_var_fail = get_checkbox_var_fail(script_name)
        
        # Print the retrieved checkbox variables for debugging
        print(f"Updating checkboxes for script: {script_name}")
        print("Success checkbox variable:", checkbox_var)
        print("Failure checkbox variable:", checkbox_var_fail)
        
        # Check if the variables are valid
        if checkbox_var is None or checkbox_var_fail is None:
            raise ValueError("Checkbox variables could not be retrieved.")
        
        # Update the checkboxes
        checkbox_var.set(1)  # Set success checkbox to checked (1)
        checkbox_var_fail.set(0)  # Set failure checkbox to unchecked (0)
    
    except Exception as e:
        print(f"Error updating checkbox: {e}")



# check box variable mapping based on button setup in GUI
def get_checkbox_var(script_name):
    script_var_map = {
        "api_test_cases.py": btn1_var,
        "parse_test_cases.py": btn9_var,
        "sonar_test_cases.py": btn5_var,
        "wifi_test_cases.py": btn6_var,
        "gpio_test_cases.py": btn3_var,
        "camera_test_cases.py": btn2_var,
        # "mod_test_cases.py": btn4_var,
        # "logger_test_cases.py": btn7_var,
        # "msgs_test_cases.py": btn8_var,
        
    }
    return script_var_map.get(script_name)

# check box fail variable mapping based on button setup in GUI
def get_checkbox_var_fail(script_name):
    script_var_fail_map = {
        "api_test_cases.py": btn1_fail,
        "parse_test_cases.py": btn9_fail,
        "sonar_test_cases.py": btn5_fail,
        "wifi_test_cases.py": btn6_fail,
        "gpio_test_cases.py": btn3_fail,
        "camera_test_cases.py": btn2_fail,
        # "mod_test_cases.py": btn4_var,
        # "logger_test_cases.py": btn7_var,
        # "msgs_test_cases.py": btn8_var,
        
    }
    return script_var_fail_map.get(script_name)

# def show_frame(frame):
#     frame.tkraise()

# Function to read the temporary files of GPIO checkboxes
def read_confirmation_result():
    try:
        with open('/tmp/gpio_confirmation_result.txt', 'r') as f:
            result = f.read()
            # print(f"Read result: {result}")  # Print the content read from the file
            clear_confirmation_result()
            return result
    except FileNotFoundError:
        # print("File not found")
        return None

# clearing function for temporary files of GPIO checkboxes 
def clear_confirmation_result():
    if os.path.exists('/tmp/gpio_confirmation_result.txt'):
        os.remove('/tmp/gpio_confirmation_result.txt')
        # print("Cleared confirmation result file")  # Debug print


# Initialize YAML instance
yaml = YAML()
yaml.preserve_quotes = True

def load_config(file_path):
    """Load YAML file while preserving comments."""
    with open(file_path, 'r') as file:
        return yaml.load(file)


def save_config(data, file_path):
    """Save YAML data with custom formatting, ensuring quotes around strings and adding extra line spaces for clarity."""
    with open(file_path, 'w') as file:
        if isinstance(data, CommentedMap):
            # Write top-level comments if they exist
            if data.ca.comment and len(data.ca.comment) > 1:
                for comment in data.ca.comment[1]:
                    file.write(f"\n{comment.value.strip()}\n")  # Add an extra line space before the comment

            for key, value in data.items():
                # Write comments before the key-value pair
                pre_comment = data.ca.items.get(key, [None, None, None, None])[0]
                if pre_comment:
                    file.write(f"\n{pre_comment.value.strip()}\n")  # Add an extra line space before the comment

                # Write the key and value, ensuring quotes around strings
                if isinstance(value, str):
                    file.write(f"{key}: '{value}'\n")
                elif isinstance(value, CommentedSeq):
                    yaml.dump({key: value}, file)  # Preserve structure for lists
                else:
                    yaml.dump({key: value}, file)  # Preserve structure for other types

                # Write comments after the key-value pair
                post_comment = data.ca.items.get(key, [None, None, None, None])[2]
                if post_comment:
                    file.write(f"\n{post_comment.value.strip()}\n")  # Add an extra line space before the comment

            # Handle comments at the end of the document
            if data.ca.comment and len(data.ca.comment) > 3:
                for comment in data.ca.comment[3]:
                    file.write(f"\n{comment.value.strip()}\n")  # Add an extra line space before the comment


# Load the configuration values from the YAML file
config = load_config(config_data_path)

# Assign YAML values to variables for GUI use
current_password = config["CONFIG_PASSWORD"]
# print(current_password)



# Function to save YAML configuration
def save_changes(new_password):
    config = load_config(config_data_path)
    
    # Update USER values based on the current inputs
    config['CONFIG_PASSWORD'] = new_password
    
    # Save the updated config
    save_config(config, config_data_path)
    

def show_password_popup():
    update_display("Configuration mode activated")
    highlight_button(settings_button)
    popup = tk.Toplevel()
    popup.title("Password Verification!")

    # Set the desired dimensions for the popup window
    popup_width = 800
    popup_height = 400
    
    # Get the screen dimensions
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width // 2) - (popup_width // 2)
    y = (screen_height // 2) - (popup_height // 2)

    # Set the geometry of the popup window
    popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    popup.config(bg='lightblue')
    
    # Title Label
    title_label = tk.Label(popup, text="Security Verification for settings window", font=("Arial", 30, 'bold'))
    title_label.pack(pady=30)
    
    # Password Entry
    password_label = tk.Label(popup, text="Please enter the password to access the configuration window", font=("Arial", 20))
    password_label.pack(pady=5)
    
    password_entry = tk.Entry(popup, show="*", font=("Arial", 12))
    password_entry.pack(pady=(10,30))
    



    # Function to verify the password
    def verify_password():
        entered_password = password_entry.get()
        if entered_password == current_password:
            messagebox.showinfo("Success", "Password Verified!")
            popup.destroy()  # Close the popup after verification
            open_settings_frame()  # Open settings after successful verification
        else:
            messagebox.showerror("Error", "Incorrect Password. Try Again.")
            popup.destroy()
            show_password_popup()


    # Function to change the password
    def show_change_password_popup():
        def change_password():
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()
            if new_password == confirm_password and new_password:
                global current_password
                current_password = new_password
                messagebox.showinfo("Success", "Password Changed Successfully!")
                change_popup.destroy()
                save_changes(new_password)

            else:
                messagebox.showerror("Error", "Passwords do not match or are empty.")

        # Create a change password popup window
        change_popup = tk.Toplevel(popup)
        change_popup.title("Change Password")
        # Set the desired dimensions for the popup window
        popup_width = 800
        popup_height = 400
        
        # Get the screen dimensions
        screen_width = change_popup.winfo_screenwidth()
        screen_height = change_popup.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)

        # Set the geometry of the popup window
        change_popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        change_popup.config(bg="lightblue")

        # Title Label for change password window
        security_title_01 = tk.Label(change_popup, text="Please enter the new password and re-enter the same password again to confirm.", font=("Arial", 15, 'bold'))
        security_title_01.pack(pady=30)
            
        # New Password Entry
        new_password_label = tk.Label(change_popup, text="New Password:", font=("Arial", 12), bg="lightblue")
        new_password_label.pack(pady=5)
        
        new_password_entry = tk.Entry(change_popup, show="*", font=("Arial", 12))
        new_password_entry.pack(pady=5)
        
        # Confirm Password Entry
        confirm_password_label = tk.Label(change_popup, text="Confirm Password:", font=("Arial", 12), bg="lightblue")
        confirm_password_label.pack(pady=5)
        
        confirm_password_entry = tk.Entry(change_popup, show="*", font=("Arial", 12))
        confirm_password_entry.pack(pady=5)
        
        # Submit Button
        change_button = tk.Button(change_popup, text="Change Password", font=("Arial", 12), command=change_password, bg=btn_bg_color, fg=btn_fg_color)
        change_button.pack(pady=10)
    
    # Verify Button
    verify_button = tk.Button(popup, text="Confirm", font=("Arial", 20), command=verify_password, bg=btn_bg_color, fg=btn_fg_color)
    verify_button.pack(padx=10, pady=10, fill='x')
    
    # Change Password Button
    change_password_button = tk.Button(popup, text="Change Password", font=("Arial", 20), command=show_change_password_popup, bg=btn_bg_color, fg=btn_fg_color)
    change_password_button.pack(padx=10, pady=10, fill='x')

def open_settings_frame():
    # global security_window
    # settings_mode_frame = tk.Frame(root, bg=bg_color)
    # settings_mode_frame.place(relx=0, rely=1 - frame_height_percentage, relwidth=1, relheight=frame_height_percentage)
    # security_window = settings_mode_frame
    # settings_window = settings.create_settings_frame(settings_mode_frame, update_display)

    update_display("Spot Allocation Mode activated")
    settings_mode_frame.lift()  # Assuming spot_mode_frame is already defined elsewhere



# Example spot_current_password (to be replaced with the actual implementation)
spot_current_password = config["SPOT_PASSWORD"]

# Function to save YAML configuration
def save_spot_changes(spot_new_password):
    config = load_config(config_data_path)
    
    # Update USER values based on the current inputs
    config['SPOT_PASSWORD'] = spot_new_password
    
    # Save the updated config
    save_config(config, config_data_path)
    

# Function to show password popup for the "spot" frame
def show_spot_password_popup():
    update_display("Spot Allocation Security Verification")
    highlight_button(spot_button)
    
    popup = tk.Toplevel()
    popup.title("Password Verification!")

    # Set the desired dimensions for the popup window
    popup_width = 800
    popup_height = 400
    
    # Get the screen dimensions
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width // 2) - (popup_width // 2)
    y = (screen_height // 2) - (popup_height // 2)

    # Set the geometry of the popup window
    popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
    popup.config(bg='lightblue')

    # Title Label
    title_label = tk.Label(popup, text="Security Verification for spot allocation", font=("Arial", 30, 'bold'))
    title_label.pack(pady=30)

    # Password Entry
    password_label = tk.Label(popup, text="Please enter the password to access the spot allocation window", font=("Arial", 20))
    password_label.pack(pady=5)

    password_entry = tk.Entry(popup, show="*", font=("Arial", 12))
    password_entry.pack(pady=(10,30))

    # Function to verify the password
    def verify_spot_password():
        entered_password = password_entry.get()
        if entered_password == spot_current_password:
            messagebox.showinfo("Success", "Password Verified!")
            popup.destroy()  # Close the popup after verification
            open_spot_frame()  # Open the spot frame after successful verification
        else:
            messagebox.showerror("Error", "Incorrect Password. Try Again.")
            popup.destroy()
            show_spot_password_popup()  # Show the popup again for retry

    # Function to change the password
    def show_change_password_popup():
        def change_password():
            spot_new_password = spot_new_password_entry.get()
            confirm_password = confirm_password_entry.get()
            if spot_new_password == confirm_password and spot_new_password:
                global spot_current_password
                spot_current_password = spot_new_password
                messagebox.showinfo("Success", "Password Changed Successfully!")
                change_popup.destroy()
                save_spot_changes(spot_new_password)
            else:
                messagebox.showerror("Error", "Passwords do not match or are empty.")

        # Create a change password popup window
        change_popup = tk.Toplevel(popup)
        change_popup.title("Change Password")

        # Set the desired dimensions for the popup window
        popup_width = 800
        popup_height = 400
        
        # Get the screen dimensions
        screen_width = change_popup.winfo_screenwidth()
        screen_height = change_popup.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)

        # Set the geometry of the popup window
        change_popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        change_popup.config(bg="lightblue")
        
        # Title Label for change password window
        security_title_02 = tk.Label(change_popup, text="Please enter the new password and re-enter the same password again to confirm.", font=("Arial", 15, 'bold'))
        security_title_02.pack(pady=30)

        # New Password Entry
        spot_new_password_label = tk.Label(change_popup, text="New Password:", font=("Arial", 12), bg="lightblue")
        spot_new_password_label.pack(pady=5)
        
        spot_new_password_entry = tk.Entry(change_popup, show="*", font=("Arial", 12))
        spot_new_password_entry.pack(pady=5)
        
        # Confirm Password Entry
        confirm_password_label = tk.Label(change_popup, text="Confirm Password:", font=("Arial", 12), bg="lightblue")
        confirm_password_label.pack(pady=5)
        
        confirm_password_entry = tk.Entry(change_popup, show="*", font=("Arial", 12))
        confirm_password_entry.pack(pady=5)
        
        # Submit Button
        change_button = tk.Button(change_popup, text="Change Password", font=("Arial", 12), command=change_password, bg=btn_bg_color, fg=btn_fg_color)
        change_button.pack(pady=10)

    # Verify Button
    verify_button = tk.Button(popup, text="Confirm", font=("Arial", 20), command=verify_spot_password, bg=btn_bg_color, fg=btn_fg_color)
    verify_button.pack(padx=10, pady=10, fill='x')

    # Change Password Button
    change_password_button = tk.Button(popup, text="Change Password", font=("Arial", 20), command=show_change_password_popup, bg=btn_bg_color, fg=btn_fg_color)
    change_password_button.pack(padx=10, pady=10, fill='x')

# Function to open the spot frame
def open_spot_frame():
    update_display("Spot Allocation Mode activated")
    spot_mode_frame.lift()  # Assuming spot_mode_frame is already defined elsewhere




###############################  Coding parts for the main structure of the GUI  ###############################





root = tk.Tk()
root.configure(bg=bg_color)

# Configure root window size and grid
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# print(screen_height)
# print(screen_width)

window_width = int(screen_width * 0.95)
window_height = int(screen_height * 0.95)

root.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")
root.title("ParkEase")

# Setting the app icon into the window
try:
    icon = PhotoImage(file=icon_path)  # Load the icon image
    root.iconphoto(True, icon)  # Set the loaded image as the icon
except Exception as e:
    print(f"Error loading icon: {e}")



# Define the percentages for each frame
frame_height_percentage = 0.68  
frame1_percentage = 0.24 
frame2_percentage = 0.08  
frame3_percentage = 0.05  
frame4_percentage = 0.07
frame5_percentage = 0.05
frame6_percentage = 0.39
frame7_percentage = 0.12


# Calculate the height for each frame
frame1_height = int(window_height * frame1_percentage)
frame2_height = int(window_height * frame2_percentage)
frame3_height = int(window_height * frame3_percentage)
frame4_height = int(window_height * frame4_percentage)
frame5_height = int(window_height * frame5_percentage)
frame6_height = int(window_height * frame6_percentage)
frame7_height = int(window_height * frame7_percentage)

# Frame 1 (10% height)
frame1 = tk.Frame(root, bg=bg_color, height=frame1_height)
frame1.pack(fill='x')

# Frame 2 (20% height)
frame2 = tk.Frame(root, bg=frame_bg_color, height=frame2_height)
frame2.pack(fill='x')

# Frame 3 (30% height)
frame3 = tk.Frame(root, bg=bg_color, height=frame3_height)
frame3.pack(fill='x')

# Frame 4 (40% height)
frame4 = tk.Frame(root, bg=frame_bg_color, height=frame4_height)
frame4.pack(fill='x')

# Frame 4 (40% height)
frame5 = tk.Frame(root, bg=bg_color, height=frame5_height)
frame5.pack(fill='x')

# Frame 4 (40% height)
frame6 = tk.Frame(root, bg=frame_bg_color, height=frame6_height)
frame6.pack(fill='x')

# Frame 4 (40% height)
frame7 = tk.Frame(root, bg=frame_bg_color, height=frame7_height)
frame7.pack(fill='x')

frame1.grid_propagate(False)
frame2.grid_propagate(False)
frame3.grid_propagate(False)
frame4.grid_propagate(False)
frame5.grid_propagate(False)
frame6.grid_propagate(False)
frame7.grid_propagate(False)

# Use grid layout in frame1
frame1.grid_rowconfigure(0, weight=1)  # Row for display_text
frame1.grid_columnconfigure(0, weight=1)  # Column for display_text

# Mini screen at the top for displaying messages
display_text = tk.Text(frame1, font=('Arial'), bg=display_bg_color, fg=text_fg_color)
display_text.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

# Configure frame2 grid layout for buttons
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_columnconfigure(0, weight=1)
frame2.grid_columnconfigure(1, weight=1)
frame2.grid_columnconfigure(2, weight=1)
frame2.grid_columnconfigure(3, weight=1)
frame2.grid_columnconfigure(4, weight=1)



# Auto mode button
auto_button = tk.Button(frame2, text="Main", font=('Arial'), command=lambda:[b_indicator(), highlight_button(auto_button)],  bg=upper_btn_bg_color, fg=btn_fg_color)
auto_button.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

# Manual mode button
manual_button = tk.Button(frame2, text="Checklist", font=('Arial'), command=lambda: [manual_mode_indicator(), highlight_button(manual_button)], bg=upper_btn_bg_color, fg=btn_fg_color)
manual_button.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

# Manual mode button
settings_button = tk.Button(frame2, text="Settings", font=('Arial'), command=show_password_popup, bg=upper_btn_bg_color, fg=btn_fg_color)
settings_button.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)



# Modify the spot button command
spot_button = tk.Button(frame2, text="Spot", font=('Arial'), command=show_spot_password_popup, bg=upper_btn_bg_color, fg=btn_fg_color)
spot_button.grid(row=1, column=3, sticky='nsew', padx=10, pady=10)

# Clear text button
clear_button = tk.Button(frame2, text="Clear", font=('Arial'), command=lambda: [clear_display_and_checkboxes()], bg=upper_btn_bg_color, fg=btn_fg_color)
clear_button.grid(row=1, column=4, sticky='nsew', padx=10, pady=10)


auto_mode_frame = tk.Frame(root, bg=bg_color)
auto_mode_frame.place(relx=0, rely=1 - frame_height_percentage, relwidth=1, relheight=frame_height_percentage)
auto_frame = auto.create_auto_frame(auto_mode_frame, update_display)

settings_mode_frame = tk.Frame(root, bg=bg_color)
settings_mode_frame.place(relx=0, rely=1 - frame_height_percentage, relwidth=1, relheight=frame_height_percentage)
settings_window = settings.create_settings_frame(settings_mode_frame, update_display)

spot_mode_frame = tk.Frame(root, bg=bg_color)
spot_mode_frame.place(relx=0, rely=1 - frame_height_percentage, relwidth=1, relheight=frame_height_percentage)
spot_window = spot.create_spot_frame(spot_mode_frame, update_display)


button_labels_02 = tk.Label(frame3, text='Gate Controller', font=('Arial', 18, 'bold'), bg=bg_color, fg=text_fg_color)
# button_labels_02.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=5)
button_labels_02.pack(pady=3)


# Configure frame2 grid layout for buttons
frame4.grid_rowconfigure(0, weight=1)
frame4.grid_columnconfigure(0, weight=1)
frame4.grid_columnconfigure(1, weight=1)


# Button for open Gate control
open_button = tk.Button(frame4, text='Open Gate', font=('Arial'),command=open_gate, bg=btn_bg_color, fg=btn_fg_color)
open_button.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

# Button for close Gate control
close_button = tk.Button(frame4, text='Close Gate', font=('Arial'), command=close_gate, bg=btn_bg_color, fg=btn_fg_color)
close_button.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)


# Button frame 02 label on the top and all the test cases
btn_labels = tk.Label(frame5, text='Testing Cases', font=('Arial',18, 'bold'), bg=bg_color, fg=text_fg_color)
btn_labels.pack(pady=3)

# Configure row and column weights for testing buttons
frame6.grid_rowconfigure(0, weight=0)
frame6.grid_rowconfigure(1, weight=1)
frame6.grid_rowconfigure(2, weight=1)
frame6.grid_rowconfigure(3, weight=1)
frame6.grid_rowconfigure(4, weight=1)
frame6.grid_rowconfigure(5, weight=1)
frame6.grid_rowconfigure(6, weight=1)
frame6.grid_columnconfigure(0, weight=1)
frame6.grid_columnconfigure(1, weight=0)
frame6.grid_columnconfigure(2, weight=0)
frame6.grid_columnconfigure(3, weight=1)
frame6.grid_columnconfigure(4, weight=0)
frame6.grid_columnconfigure(5, weight=0)


# initiating variables for each checkbox for test cases
btn1_var = tk.IntVar(value=0)  
btn3_var = tk.IntVar(value=0)
btn5_var = tk.IntVar(value=0)
btn6_var = tk.IntVar(value=0)
btn9_var = tk.IntVar(value=0)
btn2_var = tk.IntVar(value=0)
buzzer_test_var = tk.IntVar(value = 0)
gate_test_var = tk.IntVar(value=0)
mode_change_var = tk.IntVar(value=0)

# fail buttons
btn6_fail = tk.IntVar(value=0)
btn3_fail = tk.IntVar(value=0)
btn1_fail = tk.IntVar(value=0)
btn9_fail = tk.IntVar(value=0)
btn5_fail = tk.IntVar(value=0)
btn2_fail = tk.IntVar(value=0)
buzzer_test_var_fail = tk.IntVar(value = 0)
gate_test_var_fail = tk.IntVar(value=0)
mode_change_var_fail = tk.IntVar(value=0)


# Test Buttons
btn1 = tk.Button(frame6, text='Internet Test', font=('Arial'), bg=btn_bg_color, fg=btn_fg_color, command=lambda: execute_and_update("wifi_test_cases.py", "Wifi Test"))
btn1_check = tk.Checkbutton(frame6, variable=btn6_var, bg=frame_bg_color, state=tk.DISABLED)
btn1_check_fail = tk.Checkbutton(frame6, variable=btn6_fail, bg=frame_bg_color, state=tk.DISABLED)
btn1.grid(row=1, column=0, sticky='nsew', padx=(10, 5), pady=10)
btn1_check.grid(row=1, column=1, sticky='nsew', padx=(5, 5), pady=10)
btn1_check_fail.grid(row=1, column=2, sticky='nsew', padx=(5, 10), pady=10)

btn2 = tk.Button(frame6, text='GPIO Test', font=('Arial'), bg=btn_bg_color, fg=btn_fg_color, command=lambda: execute_and_update("gpio_test_cases.py", "GPIO Test"))
btn2_check = tk.Checkbutton(frame6, variable=btn3_var, bg=frame_bg_color, state=tk.DISABLED)
btn2_check_fail = tk.Checkbutton(frame6, variable=btn3_fail, bg=frame_bg_color, state=tk.DISABLED)
btn2.grid(row=1, column=3, sticky='nsew', padx=(10, 5), pady=10)
btn2_check.grid(row=1, column=4, sticky='nsew', padx=(5, 5), pady=10)
btn2_check_fail.grid(row=1,column=5,sticky='nsew', padx=(5, 5), pady=10)

btn3 = tk.Button(frame6, text='API Test', font=('Arial'), bg=btn_bg_color, fg=btn_fg_color, command=lambda: execute_and_update("api_test_cases.py", "API Test"))
btn3_check = tk.Checkbutton(frame6, variable=btn1_var, bg=frame_bg_color, state=tk.DISABLED)
btn3_check_fail = tk.Checkbutton(frame6, variable=btn1_fail, bg=frame_bg_color, state=tk.DISABLED)
btn3.grid(row=2, column=0, sticky='nsew', padx=(10, 5), pady=10)
btn3_check.grid(row=2, column=1, sticky='nsew', padx=(5, 5), pady=10)
btn3_check_fail.grid(row=2,column=2,sticky='nsew', padx=(5,10), pady=10)

btn4 = tk.Button(frame6, text='Parse Test', font=('Arial'),bg=btn_bg_color, fg=btn_fg_color, command=lambda: run_script("parse_test_cases.py"))
btn4_check = tk.Checkbutton(frame6, variable=btn9_var, bg=frame_bg_color, state=tk.DISABLED)
btn4_check_fail = tk.Checkbutton(frame6, variable=btn9_fail, bg=frame_bg_color, state=tk.DISABLED)
btn4.grid(row=3, column=0, sticky='nsew', padx=(10, 5), pady=10)
btn4_check.grid(row=3, column=1, sticky='nsew', padx=(5, 5), pady=10)
btn4_check_fail.grid(row=3,column=2,sticky='nsew', padx=(5,10), pady=10)

btn5 = tk.Button(frame6, text='Sonar Test', font=('Arial'),bg=btn_bg_color, fg=btn_fg_color, command=lambda: execute_and_update("sonar_test_cases.py", "Sonar Test"))
btn5_check = tk.Checkbutton(frame6, variable=btn5_var, bg=frame_bg_color, state=tk.DISABLED)
btn5_check_fail = tk.Checkbutton(frame6, variable=btn5_fail, bg=frame_bg_color, state=tk.DISABLED)
btn5.grid(row=4, column=0, sticky='nsew', padx=(10, 5), pady=10)
btn5_check.grid(row=4, column=1, sticky='nsew', padx=(5, 5), pady=10)
btn5_check_fail.grid(row=4,column=2,sticky='nsew', padx=(5, 10), pady=10)

btn6 = tk.Button(frame6, text='Camera Test', font=('Arial'),bg=btn_bg_color, fg=btn_fg_color, command=lambda: execute_and_update("camera_test_cases.py", "Camera Test"))
btn6_check = tk.Checkbutton(frame6, variable=btn2_var, bg=frame_bg_color, state=tk.DISABLED)
btn6_check_fail = tk.Checkbutton(frame6, variable=btn2_fail, bg=frame_bg_color, state=tk.DISABLED)
btn6.grid(row=5, column=0, sticky='nsew', padx=(10, 5), pady=10)
btn6_check.grid(row=5, column=1, sticky='nsew', padx=(5, 5), pady=10)
btn6_check_fail.grid(row=5,column=2,sticky='nsew', padx=(5, 10), pady=10)

btn6 = tk.Button(frame6, text='STOP', font=('Arial'),bg='red', fg=btn_fg_color, command=stop_scripts)
btn6.grid(row=5, column=3, sticky='nsew', padx=(10, 5), pady=10)


# Text labels for the GPIO testing stages under GPIO test button
gpio_label_01 = tk.Label(frame6, text='Mode LED, Buzzer ON/OFF Check, Gate Mode out', font=('Arial'), bg=bg_color, fg=btn_fg_color)
gpio_check_01 = tk.Checkbutton(frame6, variable=buzzer_test_var, bg=frame_bg_color, state=tk.DISABLED)
gpio_check_01_fail = tk.Checkbutton(frame6, variable=buzzer_test_var_fail, bg=frame_bg_color, state=tk.DISABLED)
gpio_label_01.grid(row=2, column=3, sticky='nsew', padx=(10, 5), pady=10)
gpio_check_01.grid(row=2, column=4, sticky='nsew', padx=(5, 5), pady=10)
gpio_check_01_fail.grid(row=2, column=5, sticky='nsew', padx=(5, 10), pady=10)


gpio_label_02 = tk.Label(frame6, text='Gate Function (Gate Open/Gate Close) Check', font=('Arial'), bg=bg_color, fg=btn_fg_color)
gpio_check_02 = tk.Checkbutton(frame6, variable=gate_test_var, bg=frame_bg_color, state=tk.DISABLED)
gpio_check_02_fail = tk.Checkbutton(frame6, variable=gate_test_var_fail, bg=frame_bg_color, state=tk.DISABLED)
gpio_label_02.grid(row=3, column=3, sticky='nsew', padx=(10, 5), pady=10)
gpio_check_02.grid(row=3, column=4, sticky='nsew', padx=(5, 5), pady=10)
gpio_check_02_fail.grid(row=3, column=5, sticky='nsew', padx=(5, 10), pady=10)

gpio_label_03 = tk.Label(frame6, text='Mode Change Button/Buzzer Stop Button Check', font=('Arial'), bg=bg_color, fg=btn_fg_color)
gpio_check_03 = tk.Checkbutton(frame6, variable=mode_change_var, bg=frame_bg_color, state=tk.DISABLED)
gpio_check_03_fail = tk.Checkbutton(frame6, variable=mode_change_var_fail, bg=frame_bg_color, state=tk.DISABLED)
gpio_label_03.grid(row=4, column=3, sticky='nsew', padx=(10, 5), pady=10)
gpio_check_03.grid(row=4, column=4, sticky='nsew', padx=(5, 5), pady=10)
gpio_check_03_fail.grid(row=4, column=5, sticky='nsew', padx=(5, 10), pady=10)

# Footer LOGO and other details

frame7.grid_rowconfigure(0, weight=1)
frame7.grid_columnconfigure(0, weight=1)
frame7.grid_columnconfigure(1, weight=0) 
frame7.grid_columnconfigure(2, weight=1)


# Company LOGO
try:
    # Load and resize logos
    logo1_img = Image.open(logo1_path)
    logo2_img = Image.open(logo2_path)
    logo3_img = Image.open(logo3_path)

    logo1_img = logo1_img.resize((100, 40), Image.ANTIALIAS)  # Resize as needed
    logo2_img = logo2_img.resize((70, 70), Image.ANTIALIAS)  # Resize as needed
    logo3_img = logo3_img.resize((100, 40), Image.ANTIALIAS)  # Resize as needed


    # Convert to ImageTk.PhotoImage
    logo1_photo = ImageTk.PhotoImage(logo1_img)
    logo2_photo = ImageTk.PhotoImage(logo2_img)
    logo3_photo = ImageTk.PhotoImage(logo3_img)


    # Create labels for logos
    logo1_label = tk.Label(frame7, image=logo1_photo, bg=frame_bg_color)
    logo1_label.image = logo1_photo  # Keep a reference to the image
    logo2_label = tk.Label(frame7, image=logo2_photo, bg=frame_bg_color)
    logo2_label.image = logo2_photo  # Keep a reference to the image
    logo3_label = tk.Label(frame7, image=logo3_photo, bg=frame_bg_color)
    logo3_label.image = logo3_photo  # Keep a reference to the image

    logo1_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    logo2_label.grid(row=0, column=1, padx=5, pady=5)
    logo3_label.grid(row=0, column=2, sticky="w", padx=5, pady=5)


    print("Footer logos and text loaded successfully.")
except Exception as e:
    print(f"Error loading footer logos: {e}")

# Complete and Incomplete LOGO
try:
    image1 = Image.open(correct_image_path)
    image1 = image1.resize((25, 25))  # Resize image as needed
    photo1 = ImageTk.PhotoImage(image1)

    image2 = Image.open(wrong_image_path)
    image2 = image2.resize((25, 25))  # Resize image as needed
    photo2 = ImageTk.PhotoImage(image2)
except FileNotFoundError as e:
    print(e)
    exit("Error: Image files not found. Make sure 'correct.png' and 'wrong.png' are in the correct directory.")

# Create labels for images
label1 = tk.Label(frame6, image=photo1, bg=frame_bg_color)
label2 = tk.Label(frame6, image=photo2, bg=frame_bg_color)
label3 = tk.Label(frame6, image=photo1, bg=frame_bg_color)
label4 = tk.Label(frame6, image=photo2, bg=frame_bg_color)

# Place images at specific grid positions
label1.grid(row=0, column=1, padx=10, pady=5)  # Place image1 at (0, 1)
label2.grid(row=0, column=2, padx=10, pady=5) # Place image2 at (0, 2)
label3.grid(row=0, column=4, padx=10, pady=5)  # Place image1 at (0, 4)
label4.grid(row=0, column=5, padx=10, pady=5) # Place image2 at (0, 5)

# Complete and incomplete logos
grid_frame = tk.Frame(root)
grid_frame.pack()




###############################  Coding parts for start to run the GUI  ###############################




# Codes to show auto mode as the default screen
root.protocol("WM_DELETE_WINDOW", on_closing)
auto_mode_frame.lift()  # Keep it behind all other widgets initially

# Start the periodic update of the display
root.after(100, update_output_display)  # Check the queue every 100 milliseconds

#clearing the temporory confirmation results for GPIO checkboxes
clear_confirmation_result()
update_checkboxes() # Update the checkboxes of GPIO checkboxes

# Run the script
root.mainloop()

