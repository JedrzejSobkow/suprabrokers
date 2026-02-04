"""
This script automates the download of weather condition icons from external APIs
based on WMO (World Meteorological Organization) weather codes. It retrieves 
day and night icons for all weather conditions defined in the system's configuration.
"""

import os
import json
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "contacts", "static", "weather_icons")
os.makedirs(STATIC_DIR, exist_ok=True)

JSON_FILE = os.path.join(BASE_DIR, "contacts", "data", "weather_codes.json")

with open(JSON_FILE, "r", encoding="utf-8") as f:
    wmo_data = json.load(f)

def download_image(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        path = os.path.join(STATIC_DIR, filename)
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {url}")

for code, info in wmo_data.items():
    for time_of_day in ["day", "night"]:
        img_url = info.get(time_of_day, {}).get("image")
        if img_url:
            ext = os.path.splitext(img_url)[1]
            filename = f"{code}_{time_of_day}{ext}"
            download_image(img_url, filename)
