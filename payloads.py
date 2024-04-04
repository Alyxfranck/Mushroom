import requests
import time
import random

server_url = 'http://127.0.0.1:5000/update-js'

js_files = [
    'master.js',
    'tokyo.js',
    'north_america.js',
    'south_america.js',
    'ch.js',
    'antartica.js',
    'australia.js',
    'africa.js',
]

response = requests.get('http://127.0.0.1:5000/mushrooms')
if response.status_code == 200:
    data = response.json()
    mushrooms = data

    mushroom_sizes = []
    new_n_values = []

    for mushroom in mushrooms:
        size = mushroom['size']
        mushroom_sizes.append(size)
        random.seed(size)
        new_n_value = random.uniform(1.8, 2.9)
        new_n_values.append(new_n_value)

    print('New n values:', new_n_values)

else:
    print('Error:', response.status_code)



update_interval = random(60, 600)  # every 60 seconds

def update_js_files():
    for file_name, new_n_value in zip(js_files, new_n_values):
        payload = {
            "file_name": file_name,
            "n": new_n_value
        }
        response = requests.post(server_url, json=payload)
      
        if response.status_code == 200:
            print(f"Successfully updated {file_name}")
        else:
            print(f"Failed to update {file_name}. Response: {response.text}")

# Main loop 
while True:
    update_js_files()
    time.sleep(update_interval)
