from django.contrib import admin
from .models import (Torneo, MentorDistrito, Reto, CasoDePrueba, ParticipacionTributo, 
                     RankingDistrito, AyudaMentor, PresupuestoMentor)


@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'edicion', 'estado', 'fecha_inicio', 'fecha_fin', 'is_activo', 'get_vigilantes_count']
    list_filter = ['estado', 'is_activo', 'permite_equipos']
    search_fields = ['nombre', 'descripcion']
    date_hierarchy = 'fecha_inicio'
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    filter_horizontal = ['vigilantes_asignados']
    
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
        ('Personal Asignado', {
            'fields': ('creado_por', 'vigilantes_asignados'),
            'description': 'Asignar Vigilantes (Peacekeepers) para este torneo'
        }),
        ('Meta Información', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_vigilantes_count(self, obj):
        return obj.vigilantes_asignados.count()
    get_vigilantes_count.short_description = 'Vigilantes'


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
    list_display = ['titulo', 'torneo', 'dificultad', 'tipo', 'puntos_base', 'tiene_validacion_automatica', 'fecha_publicacion', 'is_activo']
    list_filter = ['dificultad', 'tipo', 'is_activo', 'tiene_validacion_automatica', 'torneo']
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
        ('Configuración Básica', {
            'fields': ('is_activo', 'is_visible', 'archivo_datos')
        }),
        ('⚙️ Sistema de Juez Automático', {
            'fields': ('tiene_validacion_automatica', 'lenguajes_permitidos', 'tests_ocultos', 'limite_tiempo', 'limite_memoria'),
            'description': '⚠️ IMPORTANTE: Los tests_ocultos NUNCA serán visibles para tributos. Solo para evaluación automática.',
            'classes': ('wide',)
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


@admin.register(AyudaMentor)
class AyudaMentorAdmin(admin.ModelAdmin):
    """Admin para el sistema de ayudas/patrocinio de mentores"""
    list_display = ['titulo', 'tipo', 'mentor', 'tributo', 'reto', 'fecha_envio', 'leida', 'fecha_lectura']
    list_filter = ['tipo', 'leida', 'fecha_envio', 'mentor']
    search_fields = ['titulo', 'contenido', 'tributo__personaje__first_name', 'tributo__personaje__last_name']
    readonly_fields = ['fecha_envio', 'fecha_lectura']
    date_hierarchy = 'fecha_envio'
    
    fieldsets = (
        ('Información de la Ayuda', {
            'fields': ('tipo', 'titulo', 'contenido')
        }),
        ('Destinatarios', {
            'fields': ('mentor', 'tributo', 'reto')
        }),
        ('Estado', {
            'fields': ('leida', 'fecha_envio', 'fecha_lectura', 'costo_puntos')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si es un mentor, solo ve sus propias ayudas
        if request.user.rol == 'mentor':
            return qs.filter(mentor=request.user)
        return qs
    
    def save_model(self, request, obj, form, change):
        # Si es un mentor creando una ayuda, asignarlo automáticamente
        if not change and request.user.rol == 'mentor':
            obj.mentor = request.user
        super().save_model(request, obj, form, change)


@admin.register(PresupuestoMentor)
class PresupuestoMentorAdmin(admin.ModelAdmin):
    """Admin para gestionar presupuestos de patrocinio de mentores"""
    list_display = ['mentor', 'puntos_disponibles_display', 'puntos_totales', 'puntos_usados', 
                    'total_ayudas_enviadas', 'max_ayudas_por_dia', 'ultima_ayuda_enviada']
    list_filter = ['fecha_creacion']
    search_fields = ['mentor__first_name', 'mentor__last_name', 'mentor__username']
    readonly_fields = ['puntos_usados', 'total_ayudas_enviadas', 'ultima_ayuda_enviada', 
                       'fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Mentor', {
            'fields': ('mentor',)
        }),
        ('Presupuesto', {
            'fields': ('puntos_totales', 'puntos_usados', 'max_ayudas_por_dia')
        }),
        ('Estadísticas', {
            'fields': ('total_ayudas_enviadas', 'ultima_ayuda_enviada', 'fecha_creacion', 'fecha_actualizacion')
        }),
    )
    
    def puntos_disponibles_display(self, obj):
        return f"{obj.puntos_disponibles} pts"
    puntos_disponibles_display.short_description = 'Puntos Disponibles'
    
    actions = ['recargar_puntos_100', 'recargar_puntos_500', 'recargar_puntos_1000']
    
    def recargar_puntos_100(self, request, queryset):
        for presupuesto in queryset:
            presupuesto.recargar_puntos(100)
        self.message_user(request, f'Recargados 100 puntos a {queryset.count()} mentor(es)')
    recargar_puntos_100.short_description = 'Recargar 100 puntos'
    
    def recargar_puntos_500(self, request, queryset):
        for presupuesto in queryset:
            presupuesto.recargar_puntos(500)
        self.message_user(request, f'Recargados 500 puntos a {queryset.count()} mentor(es)')
    recargar_puntos_500.short_description = 'Recargar 500 puntos'
    
    def recargar_puntos_1000(self, request, queryset):
        for presupuesto in queryset:
            presupuesto.recargar_puntos(1000)
        self.message_user(request, f'Recargados 1000 puntos a {queryset.count()} mentor(es)')
    recargar_puntos_1000.short_description = 'Recargar 1000 puntos'



@admin.register(RankingDistrito)
class RankingDistritoAdmin(admin.ModelAdmin):
    list_display = ['distrito', 'torneo', 'puntos_totales', 'retos_completados', 'tributos_activos', 'fecha_actualizacion']
    list_filter = ['torneo']
    ordering = ['-puntos_totales']
    readonly_fields = ['fecha_actualizacion']
