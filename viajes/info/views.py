from math import trunc
import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from info.forms import ViajeForm, ImagenForm
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


class ListaViajesView(LoginRequiredMixin, ListView):
   model = Viaje
   template_name = 'info/lista_viajes.html'
   context_object_name = 'viajes'
   login_url = '/users/login/'

   def get_queryset(self):
       return Viaje.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')


class DetalleViajeView(LoginRequiredMixin, DetailView):
   model = Viaje
   template_name = 'info/detalle_viaje.html'
   context_object_name = 'viaje'

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       viaje = self.object
       context['actividades'] = Actividad.objects.filter(viaje=viaje).order_by('fecha', 'tiempo')
       context['imagenes'] = Imagen.objects.filter(viaje=viaje)
       return context


class CrearViajeView(LoginRequiredMixin, CreateView):
   model = Viaje
   form_class = ViajeForm
   template_name = 'info/form_viaje.html'

   def form_valid(self, form):
       form.instance.usuario = self.request.user
       messages.success(self.request, 'creacion_viaje_success')
       return super().form_valid(form)

   def get_success_url(self):
       return reverse_lazy('info:detalle_viaje', kwargs={'pk': self.object.pk})


class EditarViajeView(LoginRequiredMixin, UpdateView):
   model = Viaje
   form_class = ViajeForm
   template_name = 'info/form_viaje.html'

   def form_valid(self, form):
       messages.success(self.request, 'edicion_viaje_success')
       return super().form_valid(form)

   def get_success_url(self):
       return reverse_lazy('info:detalle_viaje', kwargs={'pk': self.object.pk})


class EliminarViajeView(LoginRequiredMixin, DeleteView):
    model = Viaje
    success_url = reverse_lazy('info:lista_viajes')

    def form_valid(self, form):
        messages.success(self.request, 'eliminacion_viaje_success')
        return super().form_valid(form)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class SubirImagenView(LoginRequiredMixin, View):
    template_name = 'info/subir_imagen.html'

    def get(self, request, *args, **kwargs):
        form = ImagenForm()
        viaje = get_object_or_404(Viaje, pk=self.kwargs['pk'])
        return render(request, self.template_name, {
            'form': form,
            'viaje': viaje
        })

    def post(self, request, *args, **kwargs):
        form = ImagenForm(request.POST, request.FILES)
        viaje = get_object_or_404(Viaje, pk=self.kwargs['pk'])

        if form.is_valid():
            archivos = request.FILES.getlist('imagenes')

            if len(archivos) > 10:
                messages.error(request, "Máximo 10 imágenes por subida")
                return redirect('info:subir_imagen', pk=viaje.pk)

            # Crear registros
            for archivo in archivos:
                Imagen.objects.create(
                    viaje=viaje,
                    imagen=archivo,
                    comentario=form.cleaned_data['comentario']
                )

            messages.success(request, f"{len(archivos)} imágenes subidas!")
            return redirect('info:detalle_viaje', pk=viaje.pk)

        return render(request, self.template_name, {
            'form': form,
            'viaje': viaje
        })