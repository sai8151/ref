import requests
import math

# API endpoint URL
api_url = 'https://saikiranreddy.info/api/getloc.php'

# Specified latitude and longitude values
target_latitude = 15.1711756
target_longitude = 76.8452485

# Function to fetch location data from the API
def fetch_location(user_id):
    params = {'user_id': user_id}
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'latitude' in data and 'longitude' in data:
            latitude = float(data['latitude'])
            longitude = float(data['longitude'])
            check_location(latitude, longitude)
        else:
            print(data['message'])
    else:
        print(f'Error: {response.status_code} - {response.text}')

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
    else:
        print('The user is not at the location')

# Call the fetch_location function with the user ID
fetch_location(1)