from django.contrib import admin
from .models import Challenge, TestCase


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1
    fields = ('name', 'is_visible', 'is_sample', 'weight', 'order')
    ordering = ['order']


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'category', 'is_active', 'is_public', 'total_test_cases', 'created_at')
    list_filter = ('difficulty', 'is_active', 'is_public', 'category', 'created_at')
    search_fields = ('title', 'description', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'slug', 'description', 'statement')
        }),
        ('Clasificación', {
            'fields': ('difficulty', 'category', 'tags', 'base_points')
        }),
        ('Configuración de Ejecución', {
            'fields': ('time_limit', 'memory_limit', 'allowed_languages')
        }),
        ('Formato y Restricciones', {
            'fields': ('input_format_description', 'output_format_description', 'constraints'),
            'classes': ('collapse',)
        }),
        ('Plantillas de Código', {
            'fields': ('code_templates',),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('is_active', 'is_public')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [TestCaseInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es nuevo
            obj.created_by = request.user.personaje
        super().save_model(request, obj, form, change)


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'challenge', 'is_visible', 'is_sample', 'weight', 'order')
    list_filter = ('is_visible', 'is_sample', 'challenge')
    search_fields = ('challenge__title', 'name', 'description')
    ordering = ['challenge', 'order']
    
    fieldsets = (
        ('Challenge', {
            'fields': ('challenge',)
        }),
        ('Test Data', {
            'fields': ('input_data', 'expected_output')
        }),
        ('Metadata', {
            'fields': ('name', 'description')
        }),
        ('Configuración', {
            'fields': ('is_visible', 'is_sample', 'weight', 'order')
        }),
        ('Límites Personalizados', {
            'fields': ('custom_time_limit', 'custom_memory_limit'),
            'classes': ('collapse',)
        }),
    )
