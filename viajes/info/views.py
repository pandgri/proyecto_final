from math import trunc

import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from info.forms import ViajeForm
from info.models import Imagen, Actividad, Viaje


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
                if lugar["addresstype"] == "city":
                    return "ciudad"
                elif lugar["addresstype"] == "town":
                    return "pueblo"

        return False

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return False
def buscar_ciudad(request):
    city = request.GET.get('city', '').strip()
    context = {'city': city}

    pueblo = es_ciudad(city)
    context['pueblo'] = pueblo

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
            for spot in tourist_data:
                name = spot.get('name', '').strip()
                point = spot.get('point')

                if name and point:
                    maps_link = f"https://www.google.com/maps?q={point['lat']},{point['lon']}"
                    context['tourist_spots'].append({
                        'name': name,
                        'maps_link': maps_link
                    })

                if len(context['tourist_spots']) >= 5:
                    break

            # Enlace general a Google Maps para la ciudad
            context['maps_url'] = f"https://www.google.com/maps?q={lat},{lon}&hl=es"


        except Exception as e:
            context['error'] = f"⚠️ Error: {str(e)}"

        return render(request, 'info/resultados.html', context)

# Vista para listar todos los viajes
def lista_viajes(request):
    viajes = Viaje.objects.all().order_by('-fecha_creacion')
    return render(request, 'info/lista_viajes.html', {'viajes': viajes})

# Vista para el detalle de un viaje
def detalle_viaje(request, viaje_id):
    viaje = get_object_or_404(Viaje, pk=viaje_id)
    actividades = Actividad.objects.filter(viaje=viaje).order_by('fecha', 'tiempo')
    imagenes = Imagen.objects.filter(viaje=viaje)
    return render(request, 'info/detalle_viaje.html', {
        'viaje': viaje,
        'actividades': actividades,
        'imagenes': imagenes,
    })

# Vista para crear un nuevo viaje
def crear_viaje(request):
    if request.method == 'POST':
        form = ViajeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalle_viaje', viaje_id=form.instance.id)
    else:
        form = ViajeForm()
    return render(request, 'info/form_viaje.html', {'form': form})

# Vista para editar un viaje existente
def editar_viaje(request, viaje_id):
    viaje = get_object_or_404(Viaje, pk=viaje_id)
    if request.method == 'POST':
        form = ViajeForm(request.POST, instance=viaje)
        if form.is_valid():
            form.save()
            return redirect('detalle_viaje', viaje_id=viaje.id)
    else:
        form = ViajeForm(instance=viaje)
    return render(request, 'info/form_viaje.html', {'form': form})

# Vista para eliminar un viaje
def eliminar_viaje(request, viaje_id):
    viaje = get_object_or_404(Viaje, pk=viaje_id)
    viaje.delete()
    return redirect('lista_viajes')