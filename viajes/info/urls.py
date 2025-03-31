from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar/', views.buscar_ciudad, name='buscar_ciudad'),
]