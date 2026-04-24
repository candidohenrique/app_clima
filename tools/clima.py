from geopy.geocoders import Nominatim
import requests

locator = Nominatim(user_agent="myGeocoder") 

WEATHER_CODE_MAP = {
    0: "Limpo",
    1: "Principalmente limpo",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Névoa",
    48: "Névoa com geada",
    51: "Garoa leve",
    53: "Garoa moderada",
    55: "Garoa intensa",
    56: "Garoa congelante leve",
    57: "Garoa congelante intensa",
    61: "Chuva leve",
    63: "Chuva moderada",
    65: "Chuva forte",
    66: "Chuva congelante leve",
    67: "Chuva congelante forte",
    71: "Neve leve",
    73: "Neve moderada",
    75: "Neve forte",
    77: "Grãos de neve",
    80: "Pancadas de chuva leves",
    81: "Pancadas de chuva moderadas",
    82: "Pancadas de chuva violentas",
    85: "Pancadas de neve leves",
    86: "Pancadas de neve fortes",
    95: "Trovoada",
    96: "Trovoada com granizo leve",
    99: "Trovoada com granizo forte",
}

def get_coordinates(city_name):
    location = locator.geocode(city_name)
    if location:
        cidade_formatada = location.raw.get('address', {}).get('city') \
            or location.raw.get('address', {}).get('town') \
            or location.raw.get('address', {}).get('village') \
            or city_name


        cidade_formatada = formatar_nome_cidade(cidade_formatada)

        return location.latitude, location.longitude, cidade_formatada
    else:
        return 'Cidade não encontrada'

def get_climate_info(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast"

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current_weather': True,
        'daily': 'weathercode,temperature_2m_max,temperature_2m_min',
        'forecast_days': 5,
        'timezone': 'America/Sao_Paulo'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        current_weather = data['current_weather']
        weather_code = current_weather.get('weathercode')
        current_weather['tipo_clima'] = WEATHER_CODE_MAP.get(weather_code, 'Condição desconhecida')
        current_weather['previsao_5_dias'] = []

        daily = data.get('daily', {})
        times = daily.get('time', [])
        max_temps = daily.get('temperature_2m_max', [])
        min_temps = daily.get('temperature_2m_min', [])
        weather_codes = daily.get('weathercode', [])

        for i in range(len(times)):
            code = weather_codes[i] if i < len(weather_codes) else None
            current_weather['previsao_5_dias'].append({
                'data': times[i],
                'temp_max': max_temps[i] if i < len(max_temps) else None,
                'temp_min': min_temps[i] if i < len(min_temps) else None,
                'weathercode': code,
                'tipo_clima': WEATHER_CODE_MAP.get(code, 'Condição desconhecida')
            })

        return current_weather
    else:
        return 'Erro ao obter informações climáticas'

def get_climate_by_city(city_name):
    coordinates = get_coordinates(city_name)
    
    if isinstance(coordinates, tuple):
        latitude, longitude, cidade_formatada = coordinates
        climate_info = get_climate_info(latitude, longitude)
        
        if isinstance(climate_info, dict):
            climate_info['cidade_formatada'] = cidade_formatada
        
        return climate_info
    else:
        return coordinates

def formatar_nome_cidade(nome):
    excecoes = {'de', 'da', 'do', 'dos', 'das', 'e'}
    
    palavras = nome.lower().split()
    resultado = []
    
    for i, palavra in enumerate(palavras):
        if palavra in excecoes and i != 0:
            resultado.append(palavra)
        else:
            resultado.append(palavra.capitalize())
    
    return ' '.join(resultado)