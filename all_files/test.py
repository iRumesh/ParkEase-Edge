import cv2

# Replace with your IP camera's URL
# It can look something like 'http://<camera_ip>:<port>/video'
camera_url = 'http://192.168.1.118:8081/video'

# Open the camera stream
cap = cv2.VideoCapture(camera_url)

if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

while True:
    # Read the next frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame")
        break
    
    # Display the frame in a window
    cv2.imshow('IP Camera Stream', frame)
    
    # Wait for the 'q' key to be pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
