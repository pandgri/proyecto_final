from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from users.forms import CustomUserCreationForm, CustomUserProfileForm
from users.models import CustomUser


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'login_success')
        return response

class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        messages.success(request, 'logout_success')
        return super().post(request, *args, **kwargs)

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'registro_success')
            return redirect('info:home')
        return render(request, 'users/registro.html', {'form': form})
    return render(request, 'users/registro.html', {'form': CustomUserCreationForm()})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserProfileForm
    template_name = 'users/perfil.html'
    success_url = reverse_lazy('users:perfil')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = self.get_object()
        profile_picture = self.request.FILES.get('profile_picture')

        if profile_picture and user.profile_picture and user.profile_picture.name != profile_picture.name:
            user.profile_picture.delete(save=False)

        new_password = form.cleaned_data.get('new_password')
        if new_password:
            current_password = form.cleaned_data.get('current_password')

            if not current_password:
                form.add_error('current_password', 'Debe ingresar la contraseña actual')
                return self.form_invalid(form)

            if not user.check_password(current_password):
                form.add_error('current_password', 'Contraseña incorrecta')
                return self.form_invalid(form)

            user.set_password(new_password)
            user.save()
            login(self.request, user)

        response = super().form_valid(form)

        messages.success(self.request, 'edicion_perfil_success')
        self.request.user.refresh_from_db()
        return response