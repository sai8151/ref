import os
import time
import numpy as np
from picamera import PiCamera

def capture_from_pi():
    # Define image dimensions
    img_width, img_height = 150, 150
    
    # Initialize the camera
    camera = PiCamera()
    camera.resolution = (img_width, img_height)
    camera.framerate = 24
    
    img = np.empty((img_height, img_width, 3), dtype=np.uint8)
    camera.capture(img, 'rgb')
    
    # Save the image with the predicted class name
    image_path = f'captured_images/{predicted_class}_{int(time.time())}.jpg'
    os.makedirs('captured_images', exist_ok=True)
    camera.capture(image_path)
