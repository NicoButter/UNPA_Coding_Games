from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Personaje, TributoInfo


@admin.register(Personaje)
class PersonajeAdmin(UserAdmin):
    """Admin personalizado para Personaje con campos específicos por rol"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'rol', 'unidad_academica', 'distrito_asignado']
    list_filter = ['rol', 'is_staff', 'is_active', 'distrito_asignado']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'unidad_academica']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información del Rol', {
            'fields': ('rol', 'telefono', 'fecha_nacimiento', 'foto')
        }),
        ('Información de Mentor', {
            'fields': ('unidad_academica', 'distrito_asignado'),
            'classes': ('collapse',),
            'description': 'Solo para usuarios con rol de Mentor'
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si es un mentor, solo ve a sus tributos
        if request.user.rol == 'mentor':
            return qs.filter(tributo_info__mentor=request.user)
        return qs


@admin.register(TributoInfo)
class TributoInfoAdmin(admin.ModelAdmin):
    """Admin para información de tributos con asignación de mentores"""
    list_display = ['codigo_tributo', 'get_nombre_completo', 'mentor', 'distrito', 'nivel', 'estado', 'tipo', 'fecha_registro']
    list_filter = ['estado', 'nivel', 'tipo', 'distrito', 'mentor']
    search_fields = ['codigo_tributo', 'personaje__first_name', 'personaje__last_name', 'personaje__username']
    readonly_fields = ['codigo_tributo', 'qr_token', 'fecha_registro', 'fecha_acreditacion', 'qr_code']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('personaje', 'codigo_tributo', 'mentor', 'estado')
        }),
        ('Jerarquía y Asignación', {
            'fields': ('distrito', 'nivel'),
        }),
        ('Tipo y Procedencia', {
            'fields': ('tipo', 'unidad_academica', 'carrera', 'año_carrera', 'institucion_origen', 'ciudad', 'provincia')
        }),
        ('Habilidades', {
            'fields': ('lenguajes_programacion', 'experiencia_previa', 'motivacion'),
            'classes': ('collapse',)
        }),
        ('Sistema de Acreditación', {
            'fields': ('qr_code', 'qr_token', 'fecha_registro', 'fecha_acreditacion', 'credencial_generada'),
            'classes': ('collapse',)
        }),
    )
    
    def get_nombre_completo(self, obj):
        return obj.personaje.get_full_name()
    get_nombre_completo.short_description = 'Nombre Completo'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si es un mentor, solo ve a sus tributos asignados
        if request.user.rol == 'mentor':
            return qs.filter(mentor=request.user)
        return qs
    
    actions = ['acreditar_tributos_seleccionados']
    
    def acreditar_tributos_seleccionados(self, request, queryset):
        """Acción masiva para acreditar tributos"""
        count = 0
        for tributo in queryset.filter(estado='pendiente'):
            tributo.acreditar()
            count += 1
        self.message_user(request, f'{count} tributo(s) acreditado(s) exitosamente.')
    acreditar_tributos_seleccionados.short_description = 'Acreditar tributos seleccionados'
