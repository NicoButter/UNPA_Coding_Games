from django.contrib import admin
from .models import District, DistrictMembership, Season, SeasonDistrict


class DistrictMembershipInline(admin.TabularInline):
    model = DistrictMembership
    extra = 0
    readonly_fields = ('joined_at', 'left_at')
    fields = ('user', 'is_active', 'joined_at', 'left_at', 'notes')


class SeasonDistrictInline(admin.TabularInline):
    model = SeasonDistrict
    extra = 1
    fields = ('season', 'is_participating', 'total_points')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active', 'total_members', 'total_tributes', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at', 'total_members', 'total_tributes')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'code', 'description')
        }),
        ('Colores', {
            'fields': ('color_primary', 'color_secondary')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Estadísticas', {
            'fields': ('total_members', 'total_tributes'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [DistrictMembershipInline, SeasonDistrictInline]


@admin.register(DistrictMembership)
class DistrictMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'district', 'is_active', 'joined_at', 'left_at')
    list_filter = ('is_active', 'district', 'joined_at')
    search_fields = ('user__first_name', 'user__last_name', 'district__name', 'district__code')
    readonly_fields = ('joined_at', 'left_at')
    date_hierarchy = 'joined_at'
    
    fieldsets = (
        ('Relación', {
            'fields': ('user', 'district')
        }),
        ('Estado', {
            'fields': ('is_active', 'joined_at', 'left_at')
        }),
        ('Notas', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['deactivate_memberships']
    
    def deactivate_memberships(self, request, queryset):
        for membership in queryset:
            membership.deactivate()
        self.message_user(request, f"{queryset.count()} membresías desactivadas exitosamente.")
    deactivate_memberships.short_description = "Desactivar membresías seleccionadas"


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'start_date', 'end_date', 'is_active', 'created_at')
    list_filter = ('is_active', 'start_date')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'code', 'description')
        }),
        ('Periodo', {
            'fields': ('start_date', 'end_date')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [SeasonDistrictInline]


@admin.register(SeasonDistrict)
class SeasonDistrictAdmin(admin.ModelAdmin):
    list_display = ('season', 'district', 'is_participating', 'total_points')
    list_filter = ('is_participating', 'season', 'district')
    search_fields = ('season__name', 'district__name', 'district__code')
    
    fieldsets = (
        ('Relación', {
            'fields': ('season', 'district')
        }),
        ('Configuración', {
            'fields': ('is_participating', 'total_points')
        }),
    )
