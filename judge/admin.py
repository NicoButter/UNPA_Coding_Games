from django.contrib import admin
from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'tributo', 'reto', 'lenguaje', 'veredicto', 'puntos_obtenidos', 'fecha_envio']
    list_filter = ['veredicto', 'lenguaje', 'fecha_envio']
    search_fields = ['tributo__personaje__nombre', 'tributo__personaje__apellido', 'reto__titulo']
    readonly_fields = ['fecha_envio', 'fecha_evaluacion', 'stdout', 'stderr', 'detalles_ejecucion']
    
    fieldsets = (
        ('Información General', {
            'fields': ('tributo', 'reto', 'lenguaje', 'codigo')
        }),
        ('Resultados', {
            'fields': ('veredicto', 'puntos_obtenidos', 'casos_pasados', 'casos_totales', 'tiempo_ejecucion')
        }),
        ('Detalles de Ejecución', {
            'fields': ('stdout', 'stderr', 'detalles_ejecucion'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_envio', 'fecha_evaluacion')
        })
    )
