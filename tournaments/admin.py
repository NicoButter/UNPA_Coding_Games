from django.contrib import admin
from django.utils.html import format_html
from .models import Tournament, TournamentMentor, TournamentVigilante, TournamentStatus
class TournamentMentorInline(admin.TabularInline):
    model = TournamentMentor
    extra = 1
    fields = ['mentor', 'distrito', 'es_activa', 'fecha_asignacion']
    readonly_fields = ['fecha_asignacion', 'asignado_por']


class TournamentVigilanteInline(admin.TabularInline):
    model = TournamentVigilante
    extra = 1
    fields = ['vigilante', 'rol_en_torneo', 'es_activa', 'fecha_asignacion']
    readonly_fields = ['fecha_asignacion', 'asignado_por']


class TournamentStatusInline(admin.TabularInline):
    model = TournamentStatus
    extra = 0
    fields = ['estado_anterior', 'estado_nuevo', 'cambio_por', 'fecha_cambio']
    readonly_fields = ['estado_anterior', 'estado_nuevo', 'cambio_por', 'fecha_cambio']
    can_delete = False


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'numero_edicion',
        'estado_badge',
        'fecha_acreditacion_inicio',
        'fecha_competencia_inicio',
        'mentores_count',
        'vigilantes_count',
        'es_activo'
    ]
    list_filter = [
        'estado',
        'es_activo',
        'permite_equipos',
        'puntuacion_por_unidad',
        'fecha_creacion'
    ]
    search_fields = ['nombre', 'descripcion', 'numero_edicion']
    readonly_fields = ['creado_por', 'fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'numero_edicion', 'descripcion', 'imagen')
        }),
        ('Fechas de Acreditación', {
            'fields': ('fecha_acreditacion_inicio', 'fecha_acreditacion_fin'),
            'description': 'Define el período en que los participantes se acreditan'
        }),
        ('Fechas de Competencia', {
            'fields': ('fecha_competencia_inicio', 'fecha_competencia_fin'),
            'description': 'Define el período en que ocurre la competencia'
        }),
        ('Fecha de Entrega de Premios', {
            'fields': ('fecha_premios',),
            'description': 'Fecha y hora de entrega de premios'
        }),
        ('Configuración', {
            'fields': (
                'estado',
                'es_activo',
                'permite_equipos',
                'puntuacion_por_unidad',
                'puntos_minimos_ganar'
            )
        }),
        ('Metadatos', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [TournamentMentorInline, TournamentVigilanteInline, TournamentStatusInline]
    
    def estado_badge(self, obj):
        """Muestra el estado con color"""
        colores = {
            'planificacion': '#FFA500',      # Naranja
            'acreditacion': '#4169E1',       # Azul
            'competencia': '#FF4500',        # Rojo-Naranja
            'entrega_premios': '#228B22',    # Verde
            'finalizado': '#808080',         # Gris
            'cancelado': '#FF0000',          # Rojo
        }
        color = colores.get(obj.estado, '#000000')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; '
            'border-radius: 5px;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def mentores_count(self, obj):
        """Cuenta de mentores activos"""
        count = obj.mentores_asignados.filter(es_activa=True).count()
        return format_html(
            '<span style="background-color: #E8F4F8; padding: 3px 8px; '
            'border-radius: 3px;">{}</span>',
            count
        )
    mentores_count.short_description = 'Mentores'
    
    def vigilantes_count(self, obj):
        """Cuenta de vigilantes activos"""
        count = obj.vigilantes_asignados.filter(es_activa=True).count()
        return format_html(
            '<span style="background-color: #F0F8E8; padding: 3px 8px; '
            'border-radius: 3px;">{}</span>',
            count
        )
    vigilantes_count.short_description = 'Vigilantes'
    
    def save_model(self, request, obj, form, change):
        """Registra cambios de estado"""
        if change:
            # Es una actualización, verificar si cambió el estado
            original = Tournament.objects.get(pk=obj.pk)
            if original.estado != obj.estado:
                TournamentStatus.objects.create(
                    torneo=obj,
                    estado_anterior=original.estado,
                    estado_nuevo=obj.estado,
                    cambio_por=request.user,
                    razon='Cambio realizado desde admin'
                )
        
        if not change:
            obj.creado_por = request.user
        
        super().save_model(request, obj, form, change)


@admin.register(TournamentMentor)
class TournamentMentorAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'torneo', 'distrito', 'es_activa', 'fecha_asignacion']
    list_filter = ['es_activa', 'torneo', 'distrito', 'fecha_asignacion']
    search_fields = ['mentor__first_name', 'mentor__last_name', 'torneo__nombre', 'distrito__name']
    readonly_fields = ['fecha_asignacion', 'asignado_por']
    
    fieldsets = (
        ('Asignación', {
            'fields': ('torneo', 'mentor', 'distrito')
        }),
        ('Estado', {
            'fields': ('es_activa',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Auditoría', {
            'fields': ('fecha_asignacion', 'asignado_por'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.asignado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(TournamentVigilante)
class TournamentVigilanteAdmin(admin.ModelAdmin):
    list_display = ['vigilante', 'torneo', 'rol_en_torneo', 'es_activa', 'fecha_asignacion']
    list_filter = ['es_activa', 'torneo', 'rol_en_torneo', 'fecha_asignacion']
    search_fields = ['vigilante__first_name', 'vigilante__last_name', 'torneo__nombre']
    readonly_fields = ['fecha_asignacion', 'asignado_por']
    
    fieldsets = (
        ('Asignación', {
            'fields': ('torneo', 'vigilante', 'rol_en_torneo')
        }),
        ('Estado', {
            'fields': ('es_activa',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',)
        }),
        ('Auditoría', {
            'fields': ('fecha_asignacion', 'asignado_por'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.asignado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(TournamentStatus)
class TournamentStatusAdmin(admin.ModelAdmin):
    list_display = ['torneo', 'estado_anterior', 'estado_nuevo', 'cambio_por', 'fecha_cambio']
    list_filter = ['torneo', 'estado_anterior', 'estado_nuevo', 'fecha_cambio']
    search_fields = ['torneo__nombre']
    readonly_fields = ['torneo', 'estado_anterior', 'estado_nuevo', 'cambio_por', 'fecha_cambio']
    
    def has_add_permission(self, request):
        # Los cambios de estado se registran automáticamente
        return False
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar historial
        return False
