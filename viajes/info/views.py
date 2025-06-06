from math import trunc
import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib import messages
from info.forms import ViajeForm, ImagenForm, ActividadForm, ComentarioForm
from info.models import Imagen, Actividad, Viaje, Comentario


def home(request):
    comentarios = Comentario.objects.filter(aprobado=True)
    form = ComentarioForm()
    comentario_pendiente = None

    if request.user.is_authenticated:
        comentario_pendiente = Comentario.objects.filter(usuario=request.user, aprobado=False).first()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.aprobado = False
            comentario.save()
            messages.info(request, 'comentario_enviado_success')
            return redirect('info:home')

    return render(request, 'info/home.html', {
        'comentarios': comentarios,
        'form': form,
        'comentario_pendiente': comentario_pendiente,
    })


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

    try:
        # Paso 1: Obtener coordenadas con la API de geocodificación de OpenWeatherMap
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={settings.OWM_API_KEY}"
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data:
            raise Exception("Ciudad no encontrada")

        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        city_name_english = geo_data[0]['name']
        country = geo_data[0].get('country', '')

        # Paso 2: Obtener datos del clima usando lat/lon
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={settings.OWM_API_KEY}&units=metric&lang=es"
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        context['weather'] = weather_data

        # Icono del clima
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

        # Imagen de fondo con Pixabay (nombre en inglés)
        photo_url = f"https://pixabay.com/api/?key={settings.PIXABAY_KEY}&q={city_name_english}+city&image_type=photo&category=places&order=popular"
        photo_response = requests.get(photo_url)
        photo_response.raise_for_status()
        photo_data = photo_response.json()

        coinciden = [
            foto for foto in photo_data.get('hits', [])
            if city_name_english.lower() in foto.get('tags', '').lower()
        ]

        if coinciden:
            context['photos'] = [foto['webformatURL'] for foto in coinciden[:2]]
        else:
            context['photo_error'] = "No hay imágenes disponibles para esta ciudad."

        # Puntos turísticos con OpenTripMap
        trip_url = (
            f"https://api.opentripmap.com/0.1/en/places/radius"
            f"?radius=10000&lon={lon}&lat={lat}&format=json&apikey={settings.OPENTRIPMAP_KEY}"
        )
        trip_response = requests.get(trip_url)
        trip_response.raise_for_status()
        tourist_data = trip_response.json()

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

        # Enlace general a Google Maps
        context['maps_url'] = f"https://www.google.com/maps?q={lat},{lon}&hl=es"

    except Exception as e:
        context['error'] = f"Error: {str(e)}"

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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        actividades = Actividad.objects.filter(viaje=self.object)

        for actividad in actividades:
            checkbox_name = f"actividad_{actividad.id}"
            actividad.completada = checkbox_name in request.POST
            actividad.save()

        return redirect('info:detalle_viaje', pk=self.object.pk)


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
        return render(request, self.template_name, {'form': form, 'viaje': viaje})

    def post(self, request, *args, **kwargs):
        form = ImagenForm(request.POST, request.FILES)
        viaje = get_object_or_404(Viaje, pk=self.kwargs['pk'])

        if form.is_valid():
            archivos = request.FILES.getlist('imagenes')

            if len(archivos) > 10:
                messages.error(request, "Máximo 10 imágenes por subida")
                return redirect('info:subir_imagen', pk=viaje.pk)

            for archivo in archivos:
                Imagen.objects.create(
                    viaje=viaje,
                    imagen=archivo,
                    comentario=form.cleaned_data['comentario']
                )

            messages.success(request, f"{len(archivos)} imágenes subidas!")
            return redirect('info:detalle_viaje', pk=viaje.pk)

        return render(request, self.template_name, {'form': form, 'viaje': viaje})

class AgregarActividadView(LoginRequiredMixin, View):
    template_name = 'info/agregar_actividad.html'

    def get(self, request, pk):
        viaje = get_object_or_404(Viaje, pk=pk)
        form = ActividadForm(viaje=viaje)
        return render(request, self.template_name, {'form': form, 'viaje': viaje})

    def post(self, request, pk):
        viaje = get_object_or_404(Viaje, pk=pk)
        form = ActividadForm(request.POST)
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.viaje = viaje
            actividad.save()
            messages.success(request, "actividad_agregada_success")
            return redirect('info:detalle_viaje', pk=viaje.pk)
        return render(request, self.template_name, {'form': form, 'viaje': viaje})

class EliminarActividadView(LoginRequiredMixin, DeleteView):
    model = Actividad

    def get_success_url(self):
        viaje_pk = self.object.viaje.pk
        messages.success(self.request, 'eliminacion_actividad_success')
        return reverse_lazy('info:detalle_viaje', kwargs={'pk': viaje_pk})

    def get_queryset(self):
        return super().get_queryset().filter(viaje__usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'eliminacion_actividad_success')
        return super().form_valid(form)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class GaleriaImagenesView(LoginRequiredMixin, DetailView):
    model = Viaje
    template_name = 'info/galeria_imagenes.html'
    context_object_name = 'viaje'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        imagenes = Imagen.objects.filter(viaje=self.object)

        paginator = Paginator(imagenes, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context


class EliminarImagenView(LoginRequiredMixin, DeleteView):
    model = Imagen

    def get_success_url(self):
        viaje_pk = self.object.viaje.pk
        messages.success(self.request, 'eliminacion_imagen_success')
        return reverse_lazy('info:galeria_imagenes', kwargs={'pk': viaje_pk})

    def get_queryset(self):
        return super().get_queryset().filter(viaje__usuario=self.request.user)

class ListaComentariosView(LoginRequiredMixin, ListView):
   model = Comentario
   template_name = 'info/lista_comentarios.html'
   context_object_name = 'comentarios'
   login_url = '/users/login/'

   def get_queryset(self):
       return Comentario.objects.filter(usuario=self.request.user).order_by('-fecha')