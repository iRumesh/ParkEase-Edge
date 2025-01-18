import tkinter as tk
import os
from PIL import Image, ImageTk
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from tkinter import messagebox


HOME_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Declaring the relevant paths to find the other scripts that are necessary for GUI to function
script_dir = os.path.dirname(os.path.abspath(__file__))
update_display_func  = None


# Logo paths
logo1_path = os.path.join(script_dir,'images', '1.png')
logo2_path = os.path.join(script_dir,'images', '2.png')
logo3_path = os.path.join(script_dir,'images', '3.png')
image_path = os.path.join(script_dir, 't.jpg')  # Update this with the actual image path

# List of coordinate labels
coordinate_labels = ['A', 'B', 'C', 'D']
# Keep track of clicked coordinates
coordinates = []
spot_name_global = None

file_path = os.path.join(HOME_DIR, "config","config.yaml")

# Initialize YAML instance
yaml = YAML()
yaml.preserve_quotes = True

# Color Palette
bg_color = "#666666" 
upper_btn_bg_color= "#25416F"
frame_bg_color = "#505050"
bg_root = "#121212"
display_bg_color =  "#C5E8FC"  
nav_bg_color = "#d9d9d9"
btn_bg_color = "#286EB1"
btn_fg_color = "#ffffff"
text_fg_color = "#121212"
highlight_color = "#ff9800"

def initialize(update_display):
    global update_display_func
    update_display_func = update_display


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



def load_image(canvas):
    """Load the image and display it on the canvas."""
    try:
        # Load image using PIL
        image = Image.open(image_path)
        # update_display(image_path)
        image = image.resize((500, 500), Image.LANCZOS)  # Resize to fit your window

        # Convert image to a format tkinter can handle
        photo = ImageTk.PhotoImage(image)

        # Display image on the canvas
        canvas.image = photo  # Keep a reference to avoid garbage collection
        canvas.create_image(0, 0, anchor='nw', image=photo)

    except Exception as e:
        update_display_func(f"Error loading image: {e}")


def on_click(event, canvas, display_label):
    """Capture mouse click coordinates and draw a dot with a label on the image."""
    if len(coordinates) >= 4:
        # Stop accepting clicks after 4 points
        return

    x, y = event.x, event.y
    coordinates.append((x, y))

    # Draw the dot and label on the image
    draw_dot_and_label(canvas, x, y, coordinate_labels[len(coordinates)-1])

    # Update the display label
    display_label.config(text=f"Coordinates: {coordinates}")

    # Stop accepting clicks after marking 4 points
    if len(coordinates) == 4:
        display_label.config(text="All four corners marked. Coordinates: " + str(coordinates))

def draw_dot_and_label(canvas, x, y, label):
    """Draw a small dot and label (A, B, C, D) on the image canvas."""
    radius = 5
    color = "red"

    # Draw the dot
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline=color)

    # Draw the label next to the dot
    canvas.create_text(x + 10, y - 10, text=label, fill="yellow", font=('Arial', 12, 'bold'))



def create_image_frame(container):
    """Create a frame for image coordinate capture."""
    frame = tk.Frame(container, bg='#505050')
    frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Create a canvas to draw on
    canvas = tk.Canvas(frame, width=500, height=500, bg='#505050')
    canvas.pack()

    # Display label for coordinates
    if len(coordinates) >= 4:
        display_label = tk.Label(frame, text="The coordinates are already filled. Please click the 'Restore' button to chnage.", font=('Arial', 14), bg='#505050', fg='#ffffff')
        display_label.pack(pady=10)
    else:
        display_label = tk.Label(frame, text="Click on the image to get coordinates", font=('Arial', 14), bg='#505050', fg='#ffffff')
        display_label.pack(pady=10)


    # Load and display the image on the canvas
    load_image(canvas)

    # Bind mouse click event to capture coordinates
    canvas.bind("<Button-1>", lambda event: on_click(event, canvas, display_label))

    return frame, canvas, display_label


def save_coordinates(coordinates, window):
    global spot_name_global

    if not spot_name_global:
        update_display_func("No spot name saved. Cannot save the coordinates.")
        return

    if not isinstance(coordinates, list):
        coordinates = [coordinates]

    config_data = load_config(file_path)

    # Check if coordinates already exist for this spot
    if spot_name_global in config_data and config_data[spot_name_global]:
        # Prompt user for confirmation if coordinates already exist
        overwrite = messagebox.askyesno("Confirmation", f"Coordinates for '{spot_name_global}' already exist. Do you want to overwrite them?")
        if not overwrite:
            update_display_func(f"Coordinates for spot '{spot_name_global}' were not saved.")
            return  # Exit if user chooses not to overwrite

    # Save coordinates to the YAML configuration
    config_data[spot_name_global] = [tuple(coordinates)]
    save_config(config_data, file_path)
    update_display_func(f"Coordinates have been saved under spot '{spot_name_global}'.")
    window.destroy()  # Close the image window after saving
    coordinates.clear()

def open_image_window(spot_number):

    spot_name = spot_number.get().strip()
        
    if not spot_name:
        update_display_func("Please enter a valid spot number")
        return
    
    config_data = load_config(file_path)

    
    """Open a new window displaying the image and allowing coordinate capture."""
    # Create a new window
    new_window = tk.Toplevel()
    new_window.title("Image Coordinate Capture")
    new_window.geometry("800x800")
    new_window.configure(bg='#666666')


    # Create and pack the image frame
    frame, canvas, display_label = create_image_frame(new_window)

    # Add buttons to clear or confirm coordinates
    button_frame = tk.Frame(new_window, bg=bg_color)
    button_frame.pack(side='bottom', fill='x', padx=20)
    button_frame.rowconfigure(0, weight=1)
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)


    def restore_data(spot_number):
        global coordinates 
        coordinates = []
        new_window.destroy()
        open_image_window(spot_number)

    restore_button = tk.Button(button_frame, text="Restore", font=('Arial'), command=lambda: restore_data(spot_number), bg=upper_btn_bg_color, fg=btn_fg_color)
    restore_button.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

    save_button = tk.Button(button_frame, text="Save", font=('Arial'), command=lambda: save_coordinates(coordinates, new_window), bg=upper_btn_bg_color, fg=btn_fg_color)
    save_button.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)


# Creating the spot frame for configuration
def create_spot_frame(container, update_display_func):
    global spot_number

    spot_window = tk.Frame(container, bg=bg_color)
    spot_window.pack(fill='x', padx=10, pady=10)
    spot_window.grid_rowconfigure(0, weight=1)
    spot_window.grid_columnconfigure(0, weight=1)

    title_label = tk.Label(spot_window, text="Spot Allocation Panel", font=('Arial', 40, 'bold'), bg=bg_color)
    title_label.pack(pady=20)

    descriptiom_label = tk.Label(spot_window, text="Please enter the correct spot number into the entry box.", font=('Arial', 18), bg=bg_color)
    descriptiom_label.pack(pady=5)


    spot_number = tk.Entry(spot_window, bg='#ffffff')  # Added bg color
    spot_number.pack(pady=10)  # Pack the entry widget

    def save_spot_name():
        global spot_name_global
        spot_name = spot_number.get().strip()
        
        if not spot_name:
            update_display_func("Spot name cannot be empty.")
            return

        # Load the configuration to check if the spot name already exists
        config_data = load_config(file_path)
        
        if spot_name in config_data:
            # Spot name already exists; ask for confirmation
            response = messagebox.askyesno("Confirm Spot", f"The spot '{spot_name}' already exists. Do you want to proceed?")
            
            if response:  # User clicked "Yes"
                spot_name_global = spot_name
                # Open the image window to capture coordinates
                open_image_window(spot_number)
            else:
                # User clicked "No," do nothing
                update_display_func("Spot creation canceled.")
        else:
            # Spot name is new; add it directly
            config_data[spot_name] = []
            save_config(config_data, file_path)
            update_display_func(f"Spot '{spot_name}' has been saved as a new entry.")
            spot_name_global = spot_name
            # Open the image window to capture coordinates
            open_image_window(spot_number)


    def clear_entry_box():
        spot_number.delete(0, tk.END)

    button_frame = tk.Frame(spot_window, bg=bg_color)
    button_frame.pack(padx=20, pady=20)
    button_frame.rowconfigure(1, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(1, weight=1)

    spot_save_button = tk.Button(button_frame,text="Confirm",font=('Arial'),command=save_spot_name, bg=upper_btn_bg_color, fg=btn_fg_color)
    spot_save_button.grid(row=0, column=0, pady=10, padx=10, sticky='ew')

    # Auto mode button
    spot_clear_button = tk.Button(button_frame, text="Clear Entry", font=('Arial'), command=clear_entry_box,  bg=upper_btn_bg_color, fg=btn_fg_color)
    spot_clear_button.grid(row=0, column=1, pady=10, padx=10, sticky='ew')


    # Footer LOGO and other details
    logo_frame = tk.Frame(spot_window, bg=bg_color)
    logo_frame.pack(side='bottom', fill='x', padx=20, pady=40)
    logo_frame.rowconfigure(0, weight=1)
    logo_frame.columnconfigure(0, weight=1)
    logo_frame.columnconfigure(1, weight=1)
    logo_frame.columnconfigure(2, weight=1)

    footer_frame = tk.Frame(logo_frame, bg=bg_color)
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

        logo1_img = logo1_img.resize((300, 200), Image.ANTIALIAS)  # Resize as needed
        logo2_img = logo2_img.resize((300, 200), Image.ANTIALIAS)  # Resize as needed
        logo3_img = logo3_img.resize((300, 200), Image.ANTIALIAS)  # Resize as needed

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

        # update_display_func("Footer logos and text loaded successfully.")
    except Exception as e:
        update_display_func(f"Error loading footer logos: {e}")

    return spot_window










##################################################################  IP camera integrated code without static image loading ###################################################################





# import tkinter as tk
# import os
# from PIL import Image, ImageTk
# from ruamel.yaml import YAML
# from ruamel.yaml.comments import CommentedMap, CommentedSeq
# import cv2
# import yaml





# HOME_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# # Declaring the relevant paths to find the other scripts that are necessary for GUI to function
# script_dir = os.path.dirname(os.path.abspath(__file__))
# update_display_func  = None
# config_data_path = os.path.join(HOME_DIR, "config", "config.yaml")



# # Logo paths
# logo1_path = os.path.join(script_dir,'images', '1.png')
# logo2_path = os.path.join(script_dir,'images', '2.png')
# logo3_path = os.path.join(script_dir,'images', '3.png')

# # List of coordinate labels
# coordinate_labels = ['A', 'B', 'C', 'D']
# # Keep track of clicked coordinates
# coordinates = []
# spot_name_global = None

# file_path = os.path.join(HOME_DIR, "config","config.yaml")

# # Initialize YAML instance
# yaml = YAML()
# yaml.preserve_quotes = True

# # Color Palette
# bg_color = "#666666" 
# upper_btn_bg_color= "#25416F"
# frame_bg_color = "#505050"
# bg_root = "#121212"
# display_bg_color =  "#C5E8FC"  
# nav_bg_color = "#d9d9d9"
# btn_bg_color = "#286EB1"
# btn_fg_color = "#ffffff"
# text_fg_color = "#121212"
# highlight_color = "#ff9800"

# # Debugging: Check if the file exists and print the path
# if os.path.exists(config_data_path):
#     print("Config file found at:", config_data_path)
# else:
#     print("Config file not found at:", config_data_path)

# def load_camera_config(config_data_path):
#     """Load YAML file while preserving comments."""
#     with open(config_data_path, 'r') as file:
#         config = yaml.safe_load(file)
#         return config['SPOT_CAMERA_IP']

# # Load the YAML configuration file
# with open("config.yaml", 'r') as file:
#     config = yaml.safe_load(file)

# def capture_image_from_camera(camera_ip):
#     # Attempt to capture from HTTP stream directly
#     cap = cv2.VideoCapture(camera_ip)  # MJPEG stream over HTTP
    
#     if not cap.isOpened():
#         print("Error: Could not access the IP camera.")
#         return None

#     ret, frame = cap.read()

#     if not ret:
#         print("Error: No image captured, unable to display.")
#         return None

#     cap.release()
#     return frame


# def load_image_to_screen(ip_camera_url):
#     image_frame = capture_image_from_camera(ip_camera_url)

#     if image_frame is None:
#         print("No image captured, unable to display.")
#         return

#     image_pil = Image.fromarray(image_frame)
#     image_tk = ImageTk.PhotoImage(image_pil)

#     label = tk.Label(root, image=image_tk)
#     label.image = image_tk  # Keep a reference
#     label.pack()


# # Load IP camera URL from the YAML configuration file
# camera_ip = load_camera_config(config_data_path)
# frame = capture_image_from_camera(camera_ip)
# print(camera_ip)



# def initialize(update_display):
#     global update_display_func
#     update_display_func = update_display


# def load_config(file_path):
#     """Load YAML file while preserving comments."""
#     with open(file_path, 'r') as file:
#         return yaml.load(file)


# def save_config(data, file_path):
#     """Save YAML data with custom formatting, ensuring quotes around strings and adding extra line spaces for clarity."""
#     with open(file_path, 'w') as file:
#         if isinstance(data, CommentedMap):
#             # Write top-level comments if they exist
#             if data.ca.comment and len(data.ca.comment) > 1:
#                 for comment in data.ca.comment[1]:
#                     file.write(f"\n{comment.value.strip()}\n")  # Add an extra line space before the comment

#             for key, value in data.items():
#                 # Write comments before the key-value pair
#                 pre_comment = data.ca.items.get(key, [None, None, None, None])[0]
#                 if pre_comment:
#                     file.write(f"\n{pre_comment.value.strip()}\n")  # Add an extra line space before the comment

#                 # Write the key and value, ensuring quotes around strings
#                 if isinstance(value, str):
#                     file.write(f"{key}: '{value}'\n")
#                 elif isinstance(value, CommentedSeq):
#                     yaml.dump({key: value}, file)  # Preserve structure for lists
#                 else:
#                     yaml.dump({key: value}, file)  # Preserve structure for other types

#                 # Write comments after the key-value pair
#                 post_comment = data.ca.items.get(key, [None, None, None, None])[2]
#                 if post_comment:
#                     file.write(f"\n{post_comment.value.strip()}\n")  # Add an extra line space before the comment

#             # Handle comments at the end of the document
#             if data.ca.comment and len(data.ca.comment) > 3:
#                 for comment in data.ca.comment[3]:
#                     file.write(f"\n{comment.value.strip()}\n")  # Add an extra line space before the comment



# def load_image(canvas):
#     """Load the image and display it on the canvas."""
#     try:
#         # Load image using PIL
#         image = load_image_to_screen(ip_camera_url)

#         # update_display(image_path)
#         image = image.resize((500, 500), Image.LANCZOS)  # Resize to fit your window

#         # Convert image to a format tkinter can handle
#         photo = ImageTk.PhotoImage(image)

#         # Display image on the canvas
#         canvas.image = photo  # Keep a reference to avoid garbage collection
#         canvas.create_image(0, 0, anchor='nw', image=photo)

#     except Exception as e:
#         update_display_func(f"Error loading image: {e}")


# def on_click(event, canvas, display_label):
#     """Capture mouse click coordinates and draw a dot with a label on the image."""
#     if len(coordinates) >= 4:
#         # Stop accepting clicks after 4 points
#         return

#     x, y = event.x, event.y
#     coordinates.append((x, y))

#     # Draw the dot and label on the image
#     draw_dot_and_label(canvas, x, y, coordinate_labels[len(coordinates)-1])

#     # Update the display label
#     display_label.config(text=f"Coordinates: {coordinates}")

#     # Stop accepting clicks after marking 4 points
#     if len(coordinates) == 4:
#         display_label.config(text="All four corners marked. Coordinates: " + str(coordinates))

# def draw_dot_and_label(canvas, x, y, label):
#     """Draw a small dot and label (A, B, C, D) on the image canvas."""
#     radius = 5
#     color = "red"

#     # Draw the dot
#     canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline=color)

#     # Draw the label next to the dot
#     canvas.create_text(x + 10, y - 10, text=label, fill="yellow", font=('Arial', 12, 'bold'))



# def create_image_frame(container):
#     """Create a frame for image coordinate capture."""
#     frame = tk.Frame(container, bg='#505050')
#     frame.pack(fill='both', expand=True, padx=10, pady=10)

#     # Create a canvas to draw on
#     canvas = tk.Canvas(frame, width=500, height=500, bg='#505050')
#     canvas.pack()

#     # Display label for coordinates
#     if len(coordinates) >= 4:
#         display_label = tk.Label(frame, text="The coordinates are already filled. Please click the 'Restore' button to chnage.", font=('Arial', 14), bg='#505050', fg='#ffffff')
#         display_label.pack(pady=10)
#     else:
#         display_label = tk.Label(frame, text="Click on the image to get coordinates", font=('Arial', 14), bg='#505050', fg='#ffffff')
#         display_label.pack(pady=10)


#     # Load and display the image on the canvas
#     load_image(canvas)

#     # Bind mouse click event to capture coordinates
#     canvas.bind("<Button-1>", lambda event: on_click(event, canvas, display_label))

#     return frame, canvas, display_label


# def save_coordinates(coordinates, window):
#     global spot_name_global

#     if not spot_name_global:
#         update_display_func("No spot name saved> cannot save the coordinates.")

#     if not isinstance(coordinates, list):
#         coordinates = [coordinates]

#     print(coordinates)

#     config_data = load_config(file_path)

#     if spot_name_global in config_data:
#         if isinstance(config_data[spot_name_global], list):
#             config_data[spot_name_global].append(tuple(coordinates))
#         else:
#             update_display_func("Unexpected data type entered.")         
#     else:
#         config_data[spot_name_global] = [tuple(coordinates)]


#     save_config(config_data, file_path)
#     update_display_func(f"coordinates have been saved unnder spot '{spot_name_global}' ")
#     window.destroy()


# def open_image_window(spot_number):

#     spot_name = spot_number.get().strip()
        
#     if not spot_name:
#         update_display_func("Please enter a valid spot number")
#         return
        
#     """Open a new window displaying the image and allowing coordinate capture."""
#     # Create a new window
#     new_window = tk.Toplevel()
#     new_window.title("Image Coordinate Capture")
#     new_window.geometry("800x800")
#     new_window.configure(bg='#666666')


#     # Create and pack the image frame
#     frame, canvas, display_label = create_image_frame(new_window)

#     # Add buttons to clear or confirm coordinates
#     button_frame = tk.Frame(new_window, bg=bg_color)
#     button_frame.pack(side='bottom', fill='x', padx=20)
#     button_frame.rowconfigure(0, weight=1)
#     button_frame.columnconfigure(0, weight=1)
#     button_frame.columnconfigure(1, weight=1)


#     def restore_data(spot_number):
#         global coordinates 
#         coordinates = []
#         new_window.destroy()
#         open_image_window(spot_number)

#     restore_button = tk.Button(button_frame, text="Restore", font=('Arial'), command=lambda: restore_data(spot_number), bg=upper_btn_bg_color, fg=btn_fg_color)
#     restore_button.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

#     save_button = tk.Button(button_frame, text="Save", font=('Arial'), command=lambda: save_coordinates(coordinates, new_window), bg=upper_btn_bg_color, fg=btn_fg_color)
#     save_button.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)


# # Creating the spot frame for configuration
# def create_spot_frame(container, update_display_func):
#     global spot_number

#     spot_window = tk.Frame(container, bg=bg_color)
#     spot_window.pack(fill='x', padx=10, pady=10)
#     spot_window.grid_rowconfigure(0, weight=1)
#     spot_window.grid_columnconfigure(0, weight=1)

#     title_label = tk.Label(spot_window, text="Spot Allocation Panel", font=('Arial', 40, 'bold'), bg=bg_color)
#     title_label.pack(pady=20)

#     descriptiom_label = tk.Label(spot_window, text="Please enter the correct apot number into the entry box.", font=('Arial', 18), bg=bg_color)
#     descriptiom_label.pack(pady=5)


#     spot_number = tk.Entry(spot_window, bg='#ffffff')  # Added bg color
#     spot_number.pack(pady=10)  # Pack the entry widget


#     def save_spot_name():
#         global spot_name_global
#         spot_name = spot_number.get().strip()
#         if not spot_name:
#             update_display_func("Spot name cannot be found")
#             return
        
#         config_data = load_config(file_path)
#         config_data[spot_name] = []
#         save_config(config_data, file_path)
#         update_display_func(f"Spot '{spot_name}' has been saved as a key.")
#         spot_name_global = spot_name

#     def clear_entry_box():
#         spot_number.delete(0, tk.END)

#     button_frame = tk.Frame(spot_window, bg=bg_color)
#     button_frame.pack(padx=20, pady=20)
#     button_frame.rowconfigure(1, weight=1)
#     button_frame.columnconfigure(1, weight=1)
#     button_frame.columnconfigure(1, weight=1)

#     # Auto mode button
#     spot_save_button = tk.Button(button_frame, text="Confirm", font=('Arial'), command=lambda:[save_spot_name(), open_image_window(spot_number)],  bg=upper_btn_bg_color, fg=btn_fg_color)
#     spot_save_button.grid(row=0, column=0, pady=10, padx=10, sticky='ew')

#     # Auto mode button
#     spot_clear_button = tk.Button(button_frame, text="Clear Entry", font=('Arial'), command=clear_entry_box,  bg=upper_btn_bg_color, fg=btn_fg_color)
#     spot_clear_button.grid(row=0, column=1, pady=10, padx=10, sticky='ew')


#     # Footer LOGO and other details
#     logo_frame = tk.Frame(spot_window, bg=bg_color)
#     logo_frame.pack(side='bottom', fill='x', padx=20, pady=40)
#     logo_frame.rowconfigure(0, weight=1)
#     logo_frame.columnconfigure(0, weight=1)
#     logo_frame.columnconfigure(1, weight=1)
#     logo_frame.columnconfigure(2, weight=1)

#     footer_frame = tk.Frame(logo_frame, bg=bg_color)
#     footer_frame_2 = tk.Frame(logo_frame, bg=bg_color)
#     footer_frame.grid(row=0, column=0, sticky='ew', pady=10)
#     footer_frame_2.grid(row=0, column=1, sticky='ew', pady=10)
#     footer_frame_3 = tk.Frame(logo_frame, bg=bg_color)
#     footer_frame_3.grid(row=0, column=2, sticky='ew', pady=10)

#     try:
#         # Load and resize logos
#         logo1_img = Image.open(logo1_path).convert("RGBA")
#         logo2_img = Image.open(logo2_path).convert("RGBA")
#         logo3_img = Image.open(logo3_path).convert("RGBA")

#         logo1_img = logo1_img.resize((100, 75), Image.ANTIALIAS)  # Resize as needed
#         logo2_img = logo2_img.resize((100, 75), Image.ANTIALIAS)  # Resize as needed
#         logo3_img = logo3_img.resize((100, 75), Image.ANTIALIAS)  # Resize as needed

#         # Convert to ImageTk.PhotoImage
#         logo1_photo = ImageTk.PhotoImage(logo1_img)
#         logo2_photo = ImageTk.PhotoImage(logo2_img)
#         logo3_photo = ImageTk.PhotoImage(logo3_img)

#         # Create labels for logos and text
#         logo1_label = tk.Label(footer_frame, image=logo1_photo, bg=bg_color)
#         logo1_label.image = logo1_photo  # Keep a reference to the image
#         logo2_label = tk.Label(footer_frame_2, image=logo2_photo, bg=bg_color)
#         logo2_label.image = logo2_photo  # Keep a reference to the image
#         logo3_label = tk.Label(footer_frame_3, image=logo3_photo, bg=bg_color)
#         logo3_label.image = logo3_photo  # Keep a reference to the image

#         # Create a container frame to center the logos
#         logo_container = tk.Frame(footer_frame)
#         logo_container.pack(expand=True)  # Expand to fill available space

#         # Pack the logos into the container frame horizontally centered
#         logo1_label.pack(side='right', padx=10)
#         logo2_label.pack(side='top', padx=10)
#         logo3_label.pack(side='left', padx=15)

#         # Pack the container frame into the footer frame
#         logo_container.pack()

#         # update_display_func("Footer logos and text loaded successfully.")
#     except Exception as e:
#         update_display_func(f"Error loading footer logos: {e}")

#     return spot_window


