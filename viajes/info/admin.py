from django.contrib import admin

from info.models import Viaje, Imagen, Actividad, Comentario

# Register your models here.

admin.site.register(Viaje)
admin.site.register(Imagen)
admin.site.register(Actividad)
admin.site.register(Comentario)

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'texto', 'fecha', 'aprobado']
    list_filter = ['aprobado', 'fecha']
    actions = ['aprobar_comentarios']

    def aprobar_comentarios(self, request, queryset):
        queryset.update(aprobado=True)
    aprobar_comentarios.short_description = "Aprobar comentarios seleccionados"