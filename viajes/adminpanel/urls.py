from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.panel_administracion, name='panel'),
    path('usuarios/', views.GestionUsuariosView.as_view(), name='usuarios'),
    path('usuarios/<int:pk>/editar/', views.EditarUsuarioView.as_view(), name='usuario_editar'),
    path('usuarios/<int:pk>/eliminar/', views.EliminarUsuarioView.as_view(), name='usuario_eliminar'),
    path('viajes/', views.GestionViajesView.as_view(), name='viajes'),
    path('comentarios/', views.GestionComentariosView.as_view(), name='comentarios'),
    path('comentarios/aprobar/<int:pk>/', views.aprobar_comentario, name='aprobar_comentario'),
    path('comentarios/eliminar/<int:pk>/', views.EliminarComentarioView.as_view(), name='eliminar_comentario'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
]