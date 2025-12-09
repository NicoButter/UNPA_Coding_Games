from django.contrib import admin
from .models import Torneo, MentorDistrito, Reto, CasoDePrueba, ParticipacionTributo, RankingDistrito


@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'edicion', 'estado', 'fecha_inicio', 'fecha_fin', 'is_activo']
    list_filter = ['estado', 'is_activo', 'permite_equipos']
    search_fields = ['nombre', 'descripcion']
    date_hierarchy = 'fecha_inicio'
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'edicion', 'descripcion', 'imagen')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin', 'fecha_inscripcion_inicio', 'fecha_inscripcion_fin')
        }),
        ('Estado y Configuración', {
            'fields': ('estado', 'is_activo', 'puntos_minimos_ganar', 'permite_equipos', 'puntuacion_por_distrito')
        }),
        ('Meta Información', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MentorDistrito)
class MentorDistritoAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'distrito', 'torneo', 'fecha_asignacion']
    list_filter = ['distrito', 'torneo']
    search_fields = ['mentor__first_name', 'mentor__last_name']


class CasoDePruebaInline(admin.TabularInline):
    model = CasoDePrueba
    extra = 1
    fields = ['nombre', 'entrada', 'salida_esperada', 'is_visible', 'es_ejemplo', 'puntos', 'orden']


@admin.register(Reto)
class RetoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'torneo', 'dificultad', 'tipo', 'puntos_base', 'fecha_publicacion', 'is_activo']
    list_filter = ['dificultad', 'tipo', 'is_activo', 'tiene_validacion_automatica']
    search_fields = ['titulo', 'descripcion']
    date_hierarchy = 'fecha_publicacion'
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    inlines = [CasoDePruebaInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('torneo', 'titulo', 'descripcion', 'enunciado')
        }),
        ('Clasificación', {
            'fields': ('dificultad', 'tipo', 'categoria')
        }),
        ('Puntuación', {
            'fields': ('puntos_base', 'puntos_bonus')
        }),
        ('Fechas', {
            'fields': ('fecha_publicacion', 'fecha_limite')
        }),
        ('Configuración', {
            'fields': ('is_activo', 'is_visible', 'tiene_validacion_automatica', 'lenguajes_permitidos', 'archivo_datos')
        }),
        ('Meta Información', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CasoDePrueba)
class CasoDePruebaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'reto', 'is_visible', 'es_ejemplo', 'puntos', 'orden']
    list_filter = ['is_visible', 'es_ejemplo', 'reto__torneo']
    search_fields = ['nombre', 'reto__titulo']
    list_editable = ['is_visible', 'es_ejemplo', 'puntos', 'orden']


@admin.register(ParticipacionTributo)
class ParticipacionTributoAdmin(admin.ModelAdmin):
    list_display = ['tributo', 'reto', 'estado', 'puntos_obtenidos', 'casos_pasados', 'casos_totales', 'fecha_envio']
    list_filter = ['estado', 'reto__torneo', 'lenguaje']
    search_fields = ['tributo__personaje__first_name', 'tributo__personaje__last_name', 'reto__titulo']
    readonly_fields = ['fecha_inicio', 'puntos_obtenidos']
    date_hierarchy = 'fecha_inicio'
    
    fieldsets = (
        ('Participación', {
            'fields': ('tributo', 'reto', 'estado', 'numero_intento')
        }),
        ('Solución', {
            'fields': ('lenguaje', 'codigo_solucion')
        }),
        ('Resultados', {
            'fields': ('puntos_obtenidos', 'casos_pasados', 'casos_totales', 'tiempo_ejecucion', 'output_validacion')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_envio', 'fecha_completado')
        }),
        ('Retroalimentación', {
            'fields': ('comentarios_mentor',),
            'classes': ('collapse',)
        }),
    )


@admin.register(RankingDistrito)
class RankingDistritoAdmin(admin.ModelAdmin):
    list_display = ['distrito', 'torneo', 'puntos_totales', 'retos_completados', 'tributos_activos', 'fecha_actualizacion']
    list_filter = ['torneo']
    ordering = ['-puntos_totales']
    readonly_fields = ['fecha_actualizacion']
