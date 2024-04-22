import requests
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
import pickle

# import os
# import time
# import numpy as np
# from picamera import PiCamera


# API endpoint URLs
location_api_url = 'https://saikiranreddy.info/api/getloc.php'
message_api_url = 'https://saikiranreddy.info/api/update_message.php'

# Load the trained model and label encoder
model = load_model('saved_model.h5')
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

#12.956377,77.642000
# Specified latitude and longitude values
#market location
target_latitude = 15.16653801
target_latitude=round(target_latitude, 3)

target_longitude = 76.8498368
target_longitude=round(target_longitude, 3)

print(target_longitude, "\t", target_latitude)

# Function to fetch location data from the API
def fetch_location(user_id):
    params = {'user_id': user_id}
    response = requests.get(location_api_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'latitude' in data and 'longitude' in data:
            latitude = float(data['latitude'])
            longitude = float(data['longitude'])
            print(latitude, longitude)
            check_location(round(latitude, 3), round(longitude, 3))
        else:
            print(data['message'])
    else:
        print(f'Error: {response.status_code} - {response.text}')

# def capture_from_pi():
#     # Define image dimensions
#     img_width, img_height = 150, 150
    
#     # Initialize the camera
#     camera = PiCamera()
#     camera.resolution = (img_width, img_height)
#     camera.framerate = 24
    
#     img = np.empty((img_height, img_width, 3), dtype=np.uint8)
#     camera.capture(img, 'rgb')

#     # Save the image with the predicted class name
#     image_path = f'captured_images/{predicted_class}_{int(time.time())}.jpg'
#     os.makedirs('captured_images', exist_ok=True)
#     camera.capture(image_path)
#     return image_path


# Function to check if the fetched location matches the target location
def check_location(latitude, longitude):
    print(latitude, "=", round(target_latitude, 7), "\t", longitude, "=", round(target_longitude, 7))
    
    # Round the values before comparing
    rounded_latitude = round(latitude, 7)
    rounded_longitude = round(longitude, 7)
    rounded_target_latitude = round(target_latitude, 7)
    rounded_target_longitude = round(target_longitude, 7)
    
    if rounded_latitude == rounded_target_latitude and rounded_longitude == rounded_target_longitude:
        print('The user is at the location')
        fetch_and_send_message()
    else:
        print('The user is not at the location')

# Function to fetch message content from the API, update it, and send SMS
def fetch_and_send_message():
    # Predict class from image
    predicted_class = predict_class_from_image()
    
    # Update message on the API endpoint
    update_message_on_api(predicted_class)

# Function to predict class from the provided image
def predict_class_from_image():
    img_width, img_height = 150, 150
    test_image_path = 'images/Image_101.jpg'
    #test_image_path=capture_from_pi()
    test_image = preprocess_image(test_image_path)
    test_image = np.expand_dims(test_image, axis=0)
    prediction = model.predict(test_image)
    predicted_class_idx = np.argmax(prediction)
    predicted_class = label_encoder.inverse_transform([predicted_class_idx])[0]
    print("the vegetables in refrigerator are : "+predicted_class)
    return "the vegetables in refrigerator are "+predicted_class

# Function to preprocess image
def preprocess_image(img_path, target_size=(150, 150)):
    img = load_img(img_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)
    return img_array

# Function to update message on the API endpoint
def update_message_on_api(message):
    payload = {'message': f'{message}'}
    response = requests.post(message_api_url, data=payload)
    if response.status_code == 200:
        print("Message updated successfully on the API")
    else:
        print(f"Failed to update message on the API: {response.text}")

# Call the fetch_location function with the user ID
fetch_location(1)
