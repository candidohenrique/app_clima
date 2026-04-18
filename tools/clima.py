from geopy.geocoders import Nominatim
import requests

locator = Nominatim(user_agent="myGeocoder") 

def get_coordinates(city_name):
    location = locator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return 'Cidade não encontrada'

def get_climate_info(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast"

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': True,
        'timezone': 'America/Sao_Paulo'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['current_weather']
    else:
        return 'Erro ao obter informações climáticas'

def get_climate_by_city(city_name):
    coordinates = get_coordinates(city_name)
    if isinstance(coordinates, tuple):
        latitude, longitude = coordinates
        climate_info = get_climate_info(latitude, longitude)
        return climate_info
    else:
        return coordinates 

