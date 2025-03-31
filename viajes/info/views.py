import requests
from django.conf import settings
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'info/home.html')

def buscar_ciudad(request):
    city = request.GET.get('city', '').strip()

    if not city:
        return render(request, 'info/buscar.html', {'city': city})

    context = {'city': city}

    try:
        photo_url = f"https://pixabay.com/api/?key={settings.PIXABAY_KEY}&q={city}+city&image_type=photo&category=city&order=popular"
        photo_response = requests.get(photo_url)
        photo_response.raise_for_status()
        photo_data = photo_response.json()

        if photo_data.get('hits'):
            context['photo'] = photo_data['hits'][0]['webformatURL']

    except Exception:
        pass

    return render(request, 'info/resultados.html', context)