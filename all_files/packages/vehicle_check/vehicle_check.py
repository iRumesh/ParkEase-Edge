#!/usr/bin/python3

'''
* declaring package vehicle_check
* @description This package is responsible for detecting vehicles in the middle of the camera frame.
*
'''

'''
* import statement section
* importing module cv2
* importing module numpy
* importing module yaml
* importing module os
* importing module sys
'''
import cv2
import numpy as np
import yaml
import os, sys

# declaring the home directory of the project
HOME_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# declaring package relative import for import sibiling directories of the package vehicle_check
sys.path.insert(1, os.path.join(HOME_DIR, "packages"))

from pyprint import pyprint
from mod import mod

# Load configuration data
config_data_path = os.path.join(HOME_DIR, "config", "config.yaml")
config_data = yaml.load(open(config_data_path, "r"), Loader=yaml.FullLoader)

# Load configuration data
IN_CAM_BOUNDS = config_data['IN_CAM_BOUNDS']
OUT_CAM_BOUNDS = config_data['OUT_CAM_BOUNDS']
VEHICLE_CATEGORIES = config_data['VEHICLE_CATEGORIES']

# Load class names
class_data_path = os.path.join(HOME_DIR, "models", "class_names.yaml")
class_data = yaml.load(open(class_data_path, "r"), Loader=yaml.FullLoader)

CLASSES = class_data['CLASSES']
colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# Load the ONNX model
model_path = os.path.join(HOME_DIR, "models", "yolov8n_640x640.onnx")
model: cv2.dnn.Net = cv2.dnn.readNetFromONNX(model_path)

def detect_objects(input_image):
    """
    Main function to load ONNX model, perform inference, draw bounding boxes, and display the output image.

    Args:
        input_image (str): Path to the input image.

    Returns:
        list: List of dictionaries containing detection information such as class_id, class_name, confidence, etc.
    """

    # Read the input image
    if mod.STATUS:
        original_image: np.ndarray = cv2.imread(input_image)
        [height, width, _] = original_image.shape

        # Prepare a square image for inference
        length = max((height, width))
        image = np.zeros((length, length, 3), np.uint8)
        image[0:height, 0:width] = original_image

        # Calculate scale factor
        scale = length / 640

        # Preprocess the image and prepare blob for model
        blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640), swapRB=True)
        model.setInput(blob)

        # Perform inference
        outputs = model.forward()

        # Prepare output array
        outputs = np.array([cv2.transpose(outputs[0])])
        rows = outputs.shape[1]

        boxes = []
        scores = []
        class_ids = []

    # Iterate through output to collect bounding boxes, confidence scores, and class IDs
    for i in range(rows):
        if mod.STATUS:
            classes_scores = outputs[0][i][4:]
            (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
            if maxScore >= 0.25:
                box = [
                    outputs[0][i][0] - (0.5 * outputs[0][i][2]),
                    outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                    outputs[0][i][2],
                    outputs[0][i][3],
                ]
                boxes.append(box)
                scores.append(maxScore)
                class_ids.append(maxClassIndex)

    if mod.STATUS:
        # Apply NMS (Non-maximum suppression)
        result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

        detections = []

    # Iterate through NMS results to draw bounding boxes and labels
    for i in range(len(result_boxes)):
        if mod.STATUS:
            index = result_boxes[i]
            box = boxes[index]
            detection = {
                "class_id": class_ids[index],
                "class_name": CLASSES[class_ids[index]],
                "confidence": scores[index],
                "box": box,
                "scale": scale,
            }
            detections.append(detection)

    return detections

def image_crop_save(input_image, box, scale=1.0):
    '''
    This function crops the detected vehicle from the input image and saves it to the output directory.
    
    Args:
        input_image (str): Path to the input image.
        box (list): List containing the bounding box coordinates.
        scale (float): Scale factor for resizing the cropped image.
    '''
    original_image = cv2.imread(input_image)
    [height, width, _] = original_image.shape

    x_0, y_0, w, h = box
    x = x_0 + w / 2
    y = y_0 + h / 2

    x_0 = int(x_0 * scale)
    y_0 = int(y_0 * scale)
    w = int(w * scale)
    h = int(h * scale)

    x = int(x * scale)
    y = int(y * scale)

    x_0 = max(0, x_0)
    y_0 = max(0, y_0)
    w = min(width, w)
    h = min(height, h)

    crop = original_image[y_0:y_0 + h, x_0:x_0 + w]
    cv2.imwrite(input_image, crop)

def detect_vehicles_in_the_middle(input_image,detections,camera):
    '''
    This function detects vehicles in the middle of the camera frame.
    
    Args:
        detections (list): List of dictionaries containing detection information such as class_id, class_name, confidence, etc.
        camera (int): Camera name (in=1 or out=0).
        
    Returns: 
        bool: True if vehicles are detected in the middle of the camera frame, False otherwise.
    '''
    if camera:
        if mod.STATUS:
            bounds = IN_CAM_BOUNDS
    else:
        if mod.STATUS:
            bounds = OUT_CAM_BOUNDS
    if mod.STATUS:
        for detection in detections:
            if detection['class_name'] in VEHICLE_CATEGORIES:
                x_0, y_0, w, h = detection['box']
                x = x_0+w/2
                y = y_0+h/2
                if x > bounds[0] and x< bounds[1] and y > bounds[2] and y < bounds[3] and w > bounds[4] and h > bounds[5]:
                    pyprint.print_msg(
                        "vehicle detected by the model",
                        executable_name=os.path.basename(__file__),
                        function_name='vehicle_check',
                    )
                    image_crop_save(input_image, detection['box'], detection['scale'])
                    return True
    pyprint.print_msg(
        "vehicle not detected by the model",
        executable_name=os.path.basename(__file__),
        function_name='vehicle_check',
    )
    return False

def detect_vehicle(input_image,camera):
    '''
    This function detects vehicles in the middle of the camera frame.
    
    Args:
        input_image (str): Path to the input image.
        camera (int): Camera name (in=0 or out=1).
        
    Returns: 
        bool: True if vehicles are detected in the middle of the camera frame, False otherwise.
    '''
    if mod.STATUS:
        return detect_vehicles_in_the_middle(input_image,detect_objects(input_image),camera)
