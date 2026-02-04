import requests
import json
import os
from django.core.cache import cache
from django.conf import settings


WEATHER_CODES_PATH = os.path.join(
    settings.BASE_DIR, "contacts", "data", "weather_codes.json"
)

def load_weather_codes():
    cache_key = "weather_codes_mapping"
    data = cache.get(cache_key)

    if not data:
        with open(WEATHER_CODES_PATH, "r", encoding = "utf-8") as f:
            data = json.load(f)
        cache.set(cache_key, data, timeout = None)  # never expires

    return data

def enrich_contacts(contacts):
    for contact in contacts:
            lat, lon = get_coordinates(contact.city)
            contact.coordinates = (lat, lon)
            contact.weather = get_weather(lat, lon, contact.city)

def get_coordinates(city_name):
    cache_key = f"city_{city_name}"
    coordinates = cache.get(cache_key)

    if not coordinates:
        response = requests.get(
            'https://nominatim.openstreetmap.org/search',
            headers = {"User-Agent": "contacts-app/1.0 (your@email.com)"},
            params = {'q': city_name, 'format': 'json', 'limit': 1}
        ).json()
        if response:
            coordinates = (response[0]['lat'], response[0]['lon'])
            cache.set(cache_key, coordinates, timeout = 60 * 60 * 24) # 1 day
        else:
            coordinates = (None, None)
            cache.set(cache_key, coordinates, timeout = 60 * 60 * 1) # 1 hour

    return coordinates


def get_weather(lat, lon, city_name):
    if not lat or not lon:
        return {}

    cache_key = f"weather_{city_name}"
    weather = cache.get(cache_key)

    if not weather:
        response = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params = {'latitude': lat, 'longitude': lon, 'current_weather': True}
        ).json()
        
        
        current = response.get("current_weather", {})
        units = response.get("current_weather_units", {})

        weather_code = str(current.get("weathercode"))
        is_day = current.get("is_day", 1)

        weather_codes = load_weather_codes()
        code_info = weather_codes.get(weather_code, {})

        day_or_night = "day" if is_day else "night"

        description = code_info.get(day_or_night, {}).get("description")
        icon_name = f"{weather_code}_{day_or_night}.png" if weather_code else None

        weather = {
            "current": current,
            "units": units,
            "description": description,
            "icon": f"weather_icons/{icon_name}" if icon_name else None,
        }

        cache.set(cache_key, weather, timeout = 60 * 30) # 30 minutes

    return weather