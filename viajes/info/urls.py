from django.urls import path
from . import views

app_name = 'info'

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar/', views.buscar_ciudad, name='buscar_ciudad'),
    path('viajes/', views.lista_viajes, name='lista_viajes'),
    path('nuevo/', views.crear_viaje, name='crear_viaje'),
    path('<int:viaje_id>/', views.detalle_viaje, name='detalle_viaje'),
    path('<int:viaje_id>/editar/', views.editar_viaje, name='editar_viaje'),
    path('<int:viaje_id>/eliminar/', views.eliminar_viaje, name='eliminar_viaje'),
]