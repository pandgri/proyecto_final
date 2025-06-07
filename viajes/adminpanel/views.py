from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, ListView, UpdateView

from .forms import CustomUserForm, ViajeForm, ComentarioForm
from django.contrib.admin.views.decorators import staff_member_required
from users.models import CustomUser
from info.models import Viaje, Comentario
from django.contrib import messages

class StaffRequiredMixin:
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

@staff_member_required
def panel_administracion(request):
    return render(request, 'adminpanel/panel.html')

class GestionUsuariosView(StaffRequiredMixin, ListView):
    model = CustomUser
    template_name = 'adminpanel/usuarios.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        return CustomUser.objects.all()

class EditarUsuarioView(StaffRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'adminpanel/formulario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Usuario'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'edicion_usuario_success')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('adminpanel:usuarios')

class EliminarUsuarioView(StaffRequiredMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('adminpanel:usuarios')

    def form_valid(self, form):
        messages.success(self.request, 'Usuario eliminado exitosamente.')
        return super().form_valid(form)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class GestionViajesView(StaffRequiredMixin, ListView):
    model = Viaje
    template_name = 'adminpanel/viajes.html'
    context_object_name = 'viajes'
    paginate_by = 10

    def get_queryset(self):
        return Viaje.objects.all()

class GestionComentariosView(StaffRequiredMixin, ListView):
    model = Comentario
    template_name = 'adminpanel/comentarios.html'
    context_object_name = 'comentarios'
    paginate_by = 10

    def get_queryset(self):
        return Comentario.objects.all().order_by('-fecha')

@staff_member_required
def aprobar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    comentario.aprobado = True
    comentario.save()
    messages.success(request, 'comentario_aprobado_success')
    return redirect('adminpanel:comentarios')

class EliminarComentarioView(StaffRequiredMixin, DeleteView):
    model = Comentario
    success_url = reverse_lazy('adminpanel:comentarios')

    def form_valid(self, form):
        messages.success(self.request, 'comentario_eliminado_success')
        return super().form_valid(form)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

@staff_member_required
def estadisticas(request):
    context = {
        'usuarios': CustomUser.objects.count(),
        'viajes': Viaje.objects.count(),
        'comentarios': Comentario.objects.count(),
        'comentarios_pendientes': Comentario.objects.filter(aprobado=False).count(),
    }
    return render(request, 'adminpanel/estadisticas.html', context)
