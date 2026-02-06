# Suprabrokers Contacts Manager

A Django + DRF project for managing contacts, with CSV import/export, weather info per contact, and a lightweight frontend using Bootstrap & Notyf for notifications. Dockerized for easy setup.

---

## Features

- Full CRUD for contacts  
- CSV import with preview & validation  
- REST API for contacts (`/api/contacts/`)  
- Weather integration with icons (no humidity data, replaced with description + icon)  
- Notyf toast notifications for user actions  
- Dockerized for local development

---

## Setup & Docker

1. Clone the repo:

```
git clone https://github.com/JedrzejSobkow/suprabrokers
cd suprabrokers
```
2.	Build and start the containers:
```
docker-compose up --build -d
docker-compose exec web python manage.py migrate
```
3. Access the app:
- Django: http://localhost:8000/contacts/￼
- Admin: http://localhost:8000/admin/

To access the admin page it is required to have superuser account that can be created via:
```
docker-compose exec web python manage.py createsuperuser
```


---

## Weather Feature

- Weather info is displayed per contact.  
- **Humidity data was removed**, because the external API didn't provide it reliably.  
- Instead, we show a **weather description + an icon**.  
- Weather icons are downloaded via a script (`download_weather_icons.py`) from external sources and mapped using **WMO codes** (`contacts/data/weather_codes.json`).  
- Weather location data is obtained from the contact's **city** field, using the OpenWeatherMap API and Nominatim OpenStreetMap API.


---

## CSV Import / Export

- CSV import allows selecting rows and previewing validation errors.  
- Export downloads all contacts as CSV.  
- Supports headers: first_name,last_name,email,phone_number,city,status


---

## Example CSV

```csv
first_name,last_name,email,phone_number,city,status
John,Doe,john@example.com,+48123456789,Warsaw,active
Jane,Smith,jane@example.com,+48987654321,Krakow,inactive
```

---

## API Endpoints & Example Usage

### Get all contacts

```
curl -X GET http://localhost:8000/api/contacts/
```

### Add a new contacts

```
curl -X POST http://localhost:8000/api/contacts/ \
-H "Content-Type: application/json" \
-d '{"first_name":"Alice","last_name":"Brown","email":"alice@example.com","phone_number":"+48111222333","city":"Gdansk","status_id":1}'
```

### Update a contact

```
curl -X PUT http://localhost:8000/api/contacts/3/ \  
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jane","last_name": "Doe","email": "jane.doe@example.com","phone_number": "987654321","city": "Los Angeles","status_id": 2}'
```

### Delete a contact

```
curl -X DELETE http://localhost:8000/api/contacts/1/
```

---

## Caching & lazy loading

- Location data (city → coordinates) is fetched from an external geocoding API and cached for **24 hours**
- Weather data is fetched from an external weather API using geographic coordinates and cached for **30 minutes**
- Cached data is stored using Django’s caching mechanism to reduce the number of external API calls
- Weather and location data are **loaded lazily on the client side** — they are fetched **after the page has loaded** via a separate request
- This approach improves perceived performance, avoids blocking page rendering, and limits unnecessary API calls while keeping data reasonably fresh
