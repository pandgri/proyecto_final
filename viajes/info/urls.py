from django.urls import path
from . import views
from .views import SubirImagenView

app_name = 'info'

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar/', views.buscar_ciudad, name='buscar_ciudad'),
    path('viajes/', views.ListaViajesView.as_view(), name='lista_viajes'),
    path('nuevo/', views.CrearViajeView.as_view(), name='crear_viaje'),
    path('viaje/<int:pk>/', views.DetalleViajeView.as_view(), name='detalle_viaje'),
    path('viaje/<int:pk>/editar/', views.EditarViajeView.as_view(), name='editar_viaje'),
    path('viaje/<int:pk>/eliminar/', views.EliminarViajeView.as_view(), name='eliminar_viaje'),
    path('viaje/<int:pk>/subir-imagen/', views.SubirImagenView.as_view(), name='subir_imagen'),
    path('viaje/<int:pk>/agregar-actividad/', views.AgregarActividadView.as_view(), name='agregar_actividad'),
]