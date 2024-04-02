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

new_n_value = round(random.uniform(2.0, 2.7), 10)

update_interval = 60  # every 60 seconds

def update_js_files():
    for file_name in js_files:
        payload = {
            "file_name": file_name,
            "n": new_n_value
        }
        response = requests.post(server_url, json=payload)
        print(new_n_value)
        
        if response.status_code == 200:
            print(f"Successfully updated {file_name}")
        else:
            print(f"Failed to update {file_name}. Response: {response.text}")

# Main loop 
while True:
    update_js_files()
    time.sleep(update_interval)
