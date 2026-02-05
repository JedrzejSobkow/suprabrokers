import requests
import json
import os
import re
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
            headers = {"User-Agent": "contacts-app/1.0 (jedrzej@email.com)"},
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

PHONE_REGEX = re.compile(r'^\+?\d{7,15}$')

def validate_contact_row(row, existing_emails, existing_phones, valid_statuses):
    errors = []
    email = row.get('email')
    phone = row.get('phone_number')
    status = row.get('status')

        
    # NOT NULL
    if not row.get('first_name'):
        errors.append("First name is required")
    if not row.get('last_name'):
        errors.append("Last name is required")
    if not email:
        errors.append("Email is required")
    if not phone:
        errors.append("Phone number is required")
    if not row.get('city'):
        errors.append("City is required")

    # VALUES LENGTH
    if row.get('first_name') and len(row['first_name']) > 50:
        errors.append("First name too long")
    if row.get('last_name') and len(row['last_name']) > 50:
        errors.append("Last name too long")
    if email and len(email) > 100:
        errors.append("Email too long")
    if row.get('city') and len(row['city']) > 100:
        errors.append("City too long")
    if status and len(status) > 50:
        errors.append("Status too long")
                
    # PHONE REGEX
    if phone and not PHONE_REGEX.match(phone):
        errors.append("Phone number invalid format")

    # UNIQUENESS
    if email in existing_emails:
        errors.append("Email already exists")
    if phone in existing_phones:
        errors.append("Phone number already exists")
                
    # STATUS VALIDATION
    if status and status not in valid_statuses:
        errors.append(f"Status '{status}' does not exist")


    if not errors:
        existing_emails.add(email)
        existing_phones.add(phone)

    return errors