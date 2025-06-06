from django import forms
from users.models import CustomUser
from info.models import Viaje, Comentario

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'is_active', 'is_staff']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ['titulo', 'descripcion', 'usuario']

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['usuario', 'texto', 'aprobado']
