from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, ProfileUpdateView
from django.conf import settings
from django.conf.urls.static import static


app_name = 'users'

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('perfil/', ProfileUpdateView.as_view(), name='perfil'),
]
