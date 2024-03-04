# Python mushroom calculator 

import time
import uuid
import requests
import configparser
import os 
import sys
import logging
import json
import random
import math 
import datetime

class Mushroom:
    id_counter = 0
    def __init__(self, name, location, description):
        self.name = name
        self.location = location
        self.description = description
        self.id = Mushroom.id_counter
        Mushroom.id_counter += 1
        self.age = 0
        self.dead = False
        self.size = 0.1
        self.growth_factor = 0
        
    def update(self):
        if not self.dead:
            self.age += 1
            # Adjust growth factor based on age
            if self.age < 100:
                # Young mushrooms grow faster
                self.size += self.growth_factor * 1.5
            elif 100 <= self.age < 500:
                # Middle-aged mushrooms grow at normal rate
                self.size += self.growth_factor
            else:
                # Older mushrooms grow slower
                self.size += self.growth_factor * 0.8

            if self.size <= 0 or self.age >= 10000:
                self.dead = True
                self.size = 0

    def __str__(self):
        return f"{self.name} is {'dead' if self.dead else 'alive'} and has a size of {self.size}"

def apply_weather(mushroom, weather_data):
    # Extract relevant data from weather_data

    weather_data['current_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    temperature_kelvin = weather_data.get('main', {}).get('temp', 273.15)  # Default to 0°C if not available
    humidity = weather_data.get('main', {}).get('humidity', 0)  # Default to 0% if not available
    cloud_cover = weather_data.get('clouds', {}).get('all', 0)  # Default to 0% if not available
    wind_speed = weather_data.get('wind', {}).get('speed', 0)  # Default to 0 m/s if not available
    pressure = weather_data.get('main', {}).get('pressure', 1013)  # Default to average sea-level pressure if not available
    rain = weather_data.get('rain', {}).get('1h', 0)  # Default to 0 mm if not available, assuming '1h' key for 1-hour rain volume
    
    temperature_celsius = temperature_kelvin - 273.15

    # Temperature factor
    temp_factor = 0.5 if temperature_celsius < 10 else \
                  1.5 if 10 <= temperature_celsius <= 24 else \
                  0.7  # Above 24°C

    # Humidity factor
    humidity_factor = 0.3 if humidity < 30 else \
                      1.0 if 30 <= humidity <= 60 else \
                      1.5  # Above 60%

    # Cloud cover factor
    cloud_factor = 1.5 if cloud_cover < 50 else 0.5
     
    # Wind speed factor
    wind_factor = 0.7 if wind_speed < 3 else \
                  1.5 if 3 <= wind_speed <= 6 else \
                  0.5  # Above 6 m/s

    # Precipitation factor
    rain_factor = 0.8 if rain < 0 else \
                  1.5 if rain == 0 else \
                  0.7  # Above average rainfall

    # Introduce randomness
    random_factor = random.uniform(0.8, 1.2)

    # Calculate growth factor with non-linear interactions
    mushroom.growth_factor = (temp_factor * humidity_factor * cloud_factor * wind_factor * rain_factor * random_factor)  

    # Update mushroom's size and age
    mushroom.update()

def get_weather(api_key, location):
    lat, lon = location
    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Request to OpenWeatherMap API failed: {e}")
        return None

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.cfg")
    config = configparser.ConfigParser()
    config.read(config_path)
    weather_api_key = config["WEATHER"]["API_KEY"]

    locations = []
    for i in range(1, 2):
        lat = config.getfloat('WEATHER', f"LAT_{i}")
        lon = config.getfloat('WEATHER', f"LON_{i}")
        locations.append((lat, lon))

    return weather_api_key, locations

def export_mushroom_data(mushrooms, file_path):
    mushroom_data = []
    for mushroom in mushrooms:
        mushroom_dict = mushroom.__dict__.copy()  # Create a copy of the mushroom's dictionary
        mushroom_data.append(mushroom_dict)

    with open(file_path, "w") as file:
       json.dump(mushroom_data, file)

def main():
    logging.basicConfig(level=logging.INFO)
    weather_api_key, locations = load_config()
    mushrooms = [Mushroom(f"Mushroom{i}", loc, "Description") for i, loc in enumerate(locations, 1)]
    
    while True:
        
       # print("-" * 100)    
       # print(f"{'Mushroom Name':<15} | {'Country':<10} | {'Status':<10} | {'Size':<10} | {'Age':<10} | {'Growth Factor':<15}")
       
        for mushroom in mushrooms:
            weather_data = get_weather(weather_api_key, mushroom.location)
            if weather_data:
                apply_weather(mushroom, weather_data)
                country = weather_data.get('sys', {}).get('country', 'Unknown')
                status = 'dead' if mushroom.dead else 'alive'
                size = f"{ mushroom.size:.2f}"  # Format size to two decimal places
                age = mushroom.age 
                growth_factor = f"{mushroom.growth_factor:.2f}"
       
        #print(f"{mushroom.name:<15} | {country:<10} | {status:<10} | {size:<10} | {age:<10} | {growth_factor:<15}")
        
        export_mushroom_data(mushrooms, "static/data.json")

        time.sleep(5)

if __name__ == "__main__":

    main()