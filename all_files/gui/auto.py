import tkinter as tk
import subprocess
import os
import sys
import yaml
import threading
from PIL import Image, ImageTk

HOME_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Declaring the relevant paths to find the other scripts that are necessary for GUI to function
script_dir = os.path.dirname(os.path.abspath(__file__))

# Logo paths
logo1_path = os.path.join(script_dir,'images', '1.png')
logo2_path = os.path.join(script_dir,'images', '2.png')
logo3_path = os.path.join(script_dir,'images', '3.png')

# Path to the folder containing the other main.py Python script
scripts_path = HOME_DIR

# importing the configuration data
config_data_path = os.path.join(HOME_DIR, "config","config.yaml")
config_data = yaml.load( open(config_data_path, "r"), Loader=yaml.FullLoader)

from packages import parse

# Get the correct working directory (the directory where main.py is located)
main_working_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class RedirectOutput:
    def __init__(self, update_display_func):
        self.update_display = update_display_func
        self.lock = threading.Lock()

    def write(self, message):
        if message.strip():  # Avoid sending empty lines
            with self.lock:
                self.update_display(message)  # Update GUI
                sys.__stdout__.write(message)  # Write to terminal

    def flush(self):
        pass  # Required to emulate sys.stdout's flush method



# Global variable to keep track of the running subprocess/ threading
running_process = None
active_button = None
stop_thread = threading.Event()

# Color Palette
bg_color = "#666666"
frame_bg_color = "#505050"
btn_bg_color = "#286EB1"
btn_fg_color = "#ffffff"
start_bg_color = "#3fada7"
stop_bg_color = "#e7311b"

# Creating the auto mode widgets for the auto mode
def create_auto_frame(container, update_display):
    auto_frame = tk.Frame(container, bg=bg_color)
    auto_frame.pack(fill='x', padx=20, pady=20)
    auto_frame.grid_rowconfigure(0, weight=1)
    auto_frame.grid_columnconfigure(0, weight=1)

    auto_label = tk.Label(auto_frame, text="Auto Mode", font=('Arial', 30, 'bold'), bg=bg_color)
    auto_label.pack(pady=20)

    button_frame = tk.Frame(auto_frame, bg=frame_bg_color)
    button_frame.pack(fill='x', padx=20, pady=20)
    button_frame.grid_rowconfigure(0, weight=1)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)


    # Create Start and Stop buttons
    start_button = tk.Button(button_frame, text="Start", font=('Arial', 20), bg=start_bg_color, fg=btn_fg_color, command=lambda: run_main_thread(update_display))
    start_button.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

    stop_button = tk.Button(button_frame, text="Stop", font=('Arial', 20), bg=stop_bg_color, fg=btn_fg_color, command=lambda: stop_script(update_display))
    stop_button.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

    # Footer LOGO and other details
    logo_frame = tk.Frame(auto_frame, bg=bg_color)
    logo_frame.pack(side='bottom', fill='x', padx=20) 
    logo_frame.rowconfigure(0, weight=1) 
    logo_frame.columnconfigure(0, weight=1)
    logo_frame.columnconfigure(1, weight=1)
    logo_frame.columnconfigure(2, weight=1)


    footer_frame = tk.Frame(logo_frame, bg=bg_color) #bg='lightblue')  # Set a background color for visibility
    footer_frame_2 = tk.Frame(logo_frame, bg=bg_color)
    footer_frame.grid(row=0, column=0, sticky='ew', pady=10)
    footer_frame_2.grid(row=0, column=1, sticky='ew', pady=10)
    footer_frame_3 = tk.Frame(logo_frame, bg=bg_color)
    footer_frame_3.grid(row=0, column=2, sticky='ew', pady=10)

    try:
        # Load and resize logos
        logo1_img = Image.open(logo1_path).convert("RGBA")
        logo2_img = Image.open(logo2_path).convert("RGBA")
        logo3_img = Image.open(logo3_path).convert("RGBA")

        logo1_img = logo1_img.resize((250, 200), Image.ANTIALIAS)  # Resize as needed
        logo2_img = logo2_img.resize((250, 200),Image.ANTIALIAS)  # Resize as needed
        logo3_img = logo3_img.resize((250, 200), Image.ANTIALIAS)  # Resize as needed

        # Convert to ImageTk.PhotoImage
        logo1_photo = ImageTk.PhotoImage(logo1_img)
        logo2_photo = ImageTk.PhotoImage(logo2_img)
        logo3_photo = ImageTk.PhotoImage(logo3_img)


        # Create labels for logos and text
        logo1_label = tk.Label(footer_frame, image=logo1_photo, bg=bg_color)
        logo1_label.image = logo1_photo  # Keep a reference to the image
        logo2_label = tk.Label(footer_frame_2, image=logo2_photo, bg=bg_color)
        logo2_label.image = logo2_photo  # Keep a reference to the image
        logo3_label = tk.Label(footer_frame_3, image=logo3_photo, bg=bg_color)
        logo3_label.image = logo3_photo  # Keep a reference to the image

        # Create a container frame to center the logos
        logo_container = tk.Frame(footer_frame)
        logo_container.pack(expand=True)  # Expand to fill available space

        # Pack the logos into the container frame horizontally centered
        logo1_label.pack(side='right', padx=10)
        logo2_label.pack(side='top', padx=10)
        logo3_label.pack(side='left', padx=15)


        # Pack the container frame into the footer frame
        logo_container.pack()

        print("Footer logos and text loaded successfully.")
    except Exception as e:
        print(f"Error loading footer logos: {e}")

    return auto_frame



# Function to capture terminal output and display in GUI
def main_thread_function(update_display):
    global running_process
    script_path = os.path.join(scripts_path, "main.py")  # Ensure this is the correct path to main.py
    # print(f"Executing: python3 {script_path}")  # Debug print

    try:
        # Run main.py as if executed directly in the terminal
        # Update subprocess.Popen call
        running_process = subprocess.Popen(
            ["python3", "main.py"],
            cwd=main_working_directory,  # Set the working directory explicitly
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        # Read and forward outputs in real time
        while True:
            output = running_process.stdout.readline()
            if output == "" and running_process.poll() is not None:
                break  # Process has finished

            if output:
                update_display(output.strip())  # Update GUI mini display
                # print(output.strip())  # Also print to the terminal

        # Capture any remaining error messages
        err_output = running_process.stderr.read()
        if err_output:
            update_display(err_output.strip())
            print(err_output.strip())

    except Exception as e:
        update_display(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")
    finally:
        running_process = None

# Function to start the above thread
def run_main_thread(update_display):
    global stop_thread
    stop_thread.clear()
    thread = threading.Thread(target=main_thread_function, args=(update_display,))
    thread.start()





# Function to implement the Stop button
def stop_script(update_display):

    parse.panelReset(
        UDP_IP=config_data["UDP_IP_IN"],
        UDP_PORT=config_data["UDP_PORT"],
    )

    parse.panelReset(
        UDP_IP=config_data["UDP_IP_OUT"],
        UDP_PORT=config_data["UDP_PORT"],
    )

    global running_process, stop_thread
    if running_process:
        stop_thread.set()
        running_process.terminate()
        update_display("Stop button pressed: Script terminated")
        running_process = None
    else:
        update_display("No script is running to stop")
