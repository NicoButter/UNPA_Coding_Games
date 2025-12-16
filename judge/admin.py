from django.contrib import admin
from .models import Submission, TestCaseResult


class TestCaseResultInline(admin.TabularInline):
    model = TestCaseResult
    extra = 0
    readonly_fields = ('test_case', 'status', 'passed', 'execution_time', 'memory_used', 'executed_at')
    fields = ('test_case', 'status', 'passed', 'execution_time', 'memory_used')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'tributo', 'reto', 'lenguaje', 'veredicto', 'puntos_obtenidos', 'porcentaje_exito', 'fecha_envio']
    list_filter = ['veredicto', 'lenguaje', 'fecha_envio']
    search_fields = ['tributo__personaje__first_name', 'tributo__personaje__last_name', 'reto__titulo']
    readonly_fields = ['fecha_envio', 'fecha_evaluacion', 'stdout', 'stderr', 'detalles_ejecucion', 'porcentaje_exito']
    inlines = [TestCaseResultInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('tributo', 'reto', 'lenguaje', 'codigo')
        }),
        ('Resultados', {
            'fields': ('veredicto', 'puntos_obtenidos', 'casos_pasados', 'casos_totales', 'porcentaje_exito', 'tiempo_ejecucion', 'memoria_usada')
        }),
        ('Detalles de Ejecución', {
            'fields': ('stdout', 'stderr', 'detalles_ejecucion'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_envio', 'fecha_evaluacion')
        })
    )


@admin.register(TestCaseResult)
class TestCaseResultAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'submission', 'test_case', 'status', 'passed', 'execution_time', 'executed_at']
    list_filter = ['status', 'passed', 'executed_at']
    search_fields = ['submission__id', 'test_case__challenge__title']
    readonly_fields = ['executed_at']
    
    fieldsets = (
        ('Relaciones', {
            'fields': ('submission', 'test_case')
        }),
        ('Resultado', {
            'fields': ('status', 'passed', 'actual_output')
        }),
        ('Métricas', {
            'fields': ('execution_time', 'memory_used')
        }),
        ('Errores', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('executed_at',)
        })
    )
