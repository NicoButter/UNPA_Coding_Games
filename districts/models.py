from django.db import models
from django.conf import settings


class District(models.Model):
    """
    Representa un distrito del Capitolio.
    En la narrativa de Hunger Games, hay 12 distritos + el Distrito 13.
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre del Distrito',
        help_text='Ej: Distrito 12, Comisión A, Grupo 3'
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código',
        help_text='Código único del distrito (D01, D02, COM-A, etc.)'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción opcional del distrito (especialidad, característica, etc.)'
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Si el distrito está activo'
    )
    
    # Colores para visualización
    color_primary = models.CharField(
        max_length=7,
        default='#d4af37',
        verbose_name='Color Primario',
        help_text='Color hex para representación visual (#RRGGBB)'
    )
    color_secondary = models.CharField(
        max_length=7,
        default='#c0c0c0',
        verbose_name='Color Secundario',
        help_text='Color secundario para UI'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Distrito'
        verbose_name_plural = 'Distritos'
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def total_members(self):
        """Retorna el total de miembros activos en el distrito"""
        return self.memberships.filter(is_active=True).count()
    
    @property
    def total_tributes(self):
        """Retorna el total de tributos en el distrito"""
        return self.memberships.filter(
            is_active=True,
            user__rol='tributo'
        ).count()


class DistrictMembership(models.Model):
    """
    Relación entre un usuario (Personaje) y un distrito.
    Permite historial de cambios de distrito y multi-distrito futuro.
    """
    user = models.ForeignKey(
        'capitol.Personaje',
        on_delete=models.CASCADE,
        related_name='district_memberships',
        verbose_name='Personaje'
    )
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name='Distrito'
    )
    
    # Periodo de pertenencia
    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Ingreso'
    )
    left_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Salida',
        help_text='Si está vacío, está activo en el distrito'
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Si la membresía está activa'
    )
    
    # Razón del cambio (opcional)
    notes = models.TextField(
        blank=True,
        verbose_name='Notas',
        help_text='Notas sobre la asignación o cambio de distrito'
    )
    
    class Meta:
        verbose_name = 'Membresía de Distrito'
        verbose_name_plural = 'Membresías de Distrito'
        ordering = ['-joined_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['district', 'is_active']),
        ]
    
    def __str__(self):
        status = "Activo" if self.is_active else "Inactivo"
        return f"{self.user.get_full_name()} → {self.district.code} ({status})"
    
    def deactivate(self):
        """Desactiva la membresía (el usuario sale del distrito)"""
        from django.utils import timezone
        self.is_active = False
        self.left_at = timezone.now()
        self.save()


class Season(models.Model):
    """
    Representa una temporada/edición de competencias.
    Permite agrupar torneos por ciclo académico o periodo.
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre de la Temporada',
        help_text='Ej: 2025 - Primer Semestre, 75° Hunger Games'
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Código',
        help_text='Código único (2025-1, HG75, etc.)'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    
    # Fechas
    start_date = models.DateField(
        verbose_name='Fecha de Inicio'
    )
    end_date = models.DateField(
        verbose_name='Fecha de Fin'
    )
    
    # Estado
    is_active = models.BooleanField(
        default=False,
        verbose_name='Temporada Activa',
        help_text='Solo una temporada puede estar activa a la vez'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def save(self, *args, **kwargs):
        # Si se marca como activa, desactivar otras temporadas
        if self.is_active:
            Season.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class SeasonDistrict(models.Model):
    """
    Relación entre temporada y distrito.
    Permite activar/desactivar distritos por temporada.
    """
    season = models.ForeignKey(
        Season,
        on_delete=models.CASCADE,
        related_name='districts',
        verbose_name='Temporada'
    )
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='seasons',
        verbose_name='Distrito'
    )
    
    # Configuración específica de la temporada
    is_participating = models.BooleanField(
        default=True,
        verbose_name='Participa',
        help_text='Si el distrito participa en esta temporada'
    )
    
    # Puntos/ranking de la temporada
    total_points = models.IntegerField(
        default=0,
        verbose_name='Puntos Totales',
        help_text='Puntos acumulados del distrito en esta temporada'
    )
    
    class Meta:
        verbose_name = 'Distrito en Temporada'
        verbose_name_plural = 'Distritos en Temporada'
        unique_together = ['season', 'district']
        ordering = ['-total_points']
    
    def __str__(self):
        return f"{self.district.code} en {self.season.code}"
