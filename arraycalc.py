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