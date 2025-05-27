from django import forms
from django.core.validators import FileExtensionValidator

from .models import Viaje, Actividad, Imagen

class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        exclude = ['usuario', 'fecha_creacion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'presupuesto': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['titulo', 'fecha', 'tiempo', 'localizacion', 'coste', 'informacion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': None,
                'max': None
            }),
            'tiempo': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'localizacion': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'coste': forms.NumberInput(attrs={'class': 'form-control'}),
            'informacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        viaje = kwargs.pop('viaje', None)
        super().__init__(*args, **kwargs)

        if viaje:
            self.fields['fecha'].widget.attrs['min'] = viaje.fecha_inicio.isoformat()
            self.fields['fecha'].widget.attrs['max'] = viaje.fecha_final.isoformat()

            self.fields['fecha'].validators.append(
                lambda value: self.validate_fecha(value, viaje)
            )

    def validate_fecha(self, value, viaje):
        if not (viaje.fecha_inicio <= value <= viaje.fecha_final):
            raise forms.ValidationError(
                f"La fecha debe estar entre {viaje.fecha_inicio} y {viaje.fecha_final}"
            )

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return [single_file_clean(data, initial)]

class ImagenForm(forms.Form):
    imagenes = MultipleFileField(
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif']
        )],
        label="Selecciona imágenes",
        help_text="Formatos permitidos: JPG, PNG, GIF (Máx. 10 archivos)",
        widget=MultipleFileInput(attrs={'class': 'form-control'}),
    )
    comentario = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Comentario para todas las imágenes'
        })
    )