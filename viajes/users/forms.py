from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'birth_date', 'country']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'birth_date': 'Fecha de nacimiento',
            'country': 'País'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(u'El email ya está registrado, prueba con otro.')
        return email


class CustomUserProfileForm(forms.ModelForm):
    current_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Ingrese su contraseña actual para confirmar cambios"
    )
    new_password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    confirm_password = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'bio', 'birth_date', 'country']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Las contraseñas no coinciden.")

            if not current_password:
                raise forms.ValidationError("Debe ingresar la contraseña actual para cambiar la contraseña.")

        return cleaned_data
