from django import forms
from .models import Viaje, Actividad, Imagen

class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ['titulo', 'ciudad', 'fecha_inicio', 'fecha_final', 'descripcion', 'presupuesto']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'type': 'date'}),
        }

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['titulo', 'fecha', 'tiempo', 'localizacion', 'coste', 'informacion']

class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ['imagen', 'comentario']
