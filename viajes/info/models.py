from django.conf import settings
from django.db import models
from users.models import CustomUser

class Viaje(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='viajes'
    )
    titulo = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    descripcion = models.TextField()
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.ciudad}"

class Imagen(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes_viajes/')
    comentario = models.CharField(max_length=255, blank=True)

class Actividad(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    fecha = models.DateField()
    tiempo = models.TimeField(blank=True, null=True)
    localizacion = models.CharField(max_length=255)
    coste = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    informacion = models.TextField(blank=True)

    def __str__(self):
        return self.titulo