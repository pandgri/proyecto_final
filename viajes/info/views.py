from math import trunc

import requests
from django.conf import settings
from django.shortcuts import render

def home(request):
    return render(request, 'info/home.html')


def es_ciudad(ciudad):
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'city': ciudad,
            'format': 'json',
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'PythonApp'
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()

        for lugar in data:
            if 'addresstype' in lugar:
                return lugar["addresstype"] == "city"

        return False

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return False
def buscar_ciudad(request):
    city = request.GET.get('city', '').strip()
    context = {'city': city}

    if not city:
        return render(request, 'info/buscar.html', context)

    if not es_ciudad(city):
        return render(request, 'info/resultados.html', context)
    else:
        try:
            # Consultar datos del clima en OpenWeatherMap
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OWM_API_KEY}&units=metric&lang=es"
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            # Verificar si la ciudad se encontró
            if weather_data.get("cod") != 200:
                raise Exception("Ciudad no encontrada")

            context['weather'] = weather_data

            # Mapear iconos según la condición climática
            weather_main = weather_data['weather'][0]['main'].lower()
            icon_map = {
                'clear': 'sun',
                'clouds': 'cloud',
                'rain': 'cloud-rain',
                'thunderstorm': 'bolt',
                'snow': 'snowflake',
                'drizzle': 'cloud-showers-water',
                'mist': 'smog',
                'haze': 'smog'
            }
            context['weather_icon'] = icon_map.get(weather_main, 'question')

            # Obtener imagen de fondo desde Pixabay
            photo_url = f"https://pixabay.com/api/?key={settings.PIXABAY_KEY}&q={city}+city&image_type=photo&category=places&order=popular"
            photo_response = requests.get(photo_url)
            photo_response.raise_for_status()
            photo_data = photo_response.json()

            if photo_data.get('hits'):
                context['photo'] = photo_data['hits'][0]['webformatURL']

            # Obtener puntos turísticos con OpenTripMap
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            trip_url = (
                f"https://api.opentripmap.com/0.1/en/places/radius"
                f"?radius=10000&lon={lon}&lat={lat}&format=json&apikey={settings.OPENTRIPMAP_KEY}"
            )
            trip_response = requests.get(trip_url)
            trip_response.raise_for_status()
            tourist_data = trip_response.json()

            # Procesar puntos turísticos
            context['tourist_spots'] = []
            for spot in tourist_data[:5]:  # Limitar a 5 resultados
                if 'name' in spot and 'point' in spot:
                    # Crear enlace a Google Maps con coordenadas del punto turístico
                    maps_link = f"https://www.google.com/maps?q={spot['point']['lat']},{spot['point']['lon']}"
                    context['tourist_spots'].append({
                        'name': spot['name'],
                        'maps_link': maps_link
                    })

            # Enlace general a Google Maps para la ciudad
            context['maps_url'] = f"https://www.google.com/maps?q={lat},{lon}&hl=es"


        except Exception as e:
            context['error'] = f"⚠️ Error: {str(e)}"

        return render(request, 'info/resultados.html', context)
