from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from capitol.models import Personaje
from districts.models import District


class Tournament(models.Model):
    """
    Modelo mejorado para gestionar torneos con:
    - Fechas de acreditación
    - Fechas de competencia
    - Fechas de entrega de premios
    - Flexibilidad para que todo sea el mismo día
    """
    ESTADO_CHOICES = [
        ('planificacion', 'En Planificación'),
        ('acreditacion', 'Período de Acreditación'),
        ('competencia', 'En Competencia'),
        ('entrega_premios', 'Entrega de Premios'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    # Información básica
    nombre = models.CharField(max_length=255, verbose_name='Nombre del Torneo')
    descripcion = models.TextField(blank=True, null=True)
    numero_edicion = models.IntegerField(
        verbose_name='Número de Edición',
        help_text='Ej: 75 para "75 Hunger Games"'
    )
    
    # Fechas de Acreditación
    fecha_acreditacion_inicio = models.DateTimeField(
        verbose_name='Inicio Acreditación',
        help_text='Fecha y hora de inicio del período de acreditación'
    )
    fecha_acreditacion_fin = models.DateTimeField(
        verbose_name='Fin Acreditación',
        help_text='Fecha y hora de fin del período de acreditación'
    )
    
    # Fechas de Competencia
    fecha_competencia_inicio = models.DateTimeField(
        verbose_name='Inicio Competencia',
        help_text='Fecha y hora de inicio de la competencia'
    )
    fecha_competencia_fin = models.DateTimeField(
        verbose_name='Fin Competencia',
        help_text='Fecha y hora de fin de la competencia'
    )
    
    # Fechas de Entrega de Premios
    fecha_premios = models.DateTimeField(
        verbose_name='Entrega de Premios',
        help_text='Fecha y hora de entrega de premios'
    )
    
    # Estado y Configuración
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='planificacion',
        verbose_name='Estado del Torneo'
    )
    es_activo = models.BooleanField(default=True, verbose_name='Torneo Activo')
    permite_equipos = models.BooleanField(
        default=False, 
        verbose_name='Permite Competencia por Equipos'
    )
    puntuacion_por_unidad = models.BooleanField(
        default=True,
        verbose_name='Puntuación por Unidad Académica',
        help_text='Los puntos se suman a la unidad académica'
    )
    
    # Configuración de puntuación
    puntos_minimos_ganar = models.IntegerField(
        default=0,
        help_text='Puntos mínimos requeridos para ganar'
    )
    
    # Metadatos
    creado_por = models.ForeignKey(
        Personaje,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tournaments_creados',
        limit_choices_to={'rol': 'jefe_capitolio'},
        verbose_name='Creado por'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Imagen del torneo
    imagen = models.ImageField(
        upload_to='tournaments/imagenes/', 
        blank=True, 
        null=True,
        verbose_name='Imagen del Torneo'
    )
    
    class Meta:
        verbose_name = 'Torneo'
        verbose_name_plural = 'Torneos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} - Edición {self.numero_edicion}"
    
    def clean(self):
        """Valida que las fechas sean coherentes"""
        errors = {}
        
        # Validar que acreditación sea antes de competencia
        if self.fecha_acreditacion_fin > self.fecha_competencia_inicio:
            errors['fecha_acreditacion_fin'] = 'La acreditación debe finalizarse antes de que comience la competencia.'
        
        # Validar que competencia sea antes de premios
        if self.fecha_competencia_fin > self.fecha_premios:
            errors['fecha_competencia_fin'] = 'La competencia debe finalizarse antes de la entrega de premios.'
        
        # Validar que las fechas de inicio sean antes que las de fin
        if self.fecha_acreditacion_inicio >= self.fecha_acreditacion_fin:
            errors['fecha_acreditacion_inicio'] = 'La fecha de inicio debe ser anterior a la de fin.'
        
        if self.fecha_competencia_inicio >= self.fecha_competencia_fin:
            errors['fecha_competencia_inicio'] = 'La fecha de inicio debe ser anterior a la de fin.'
        
        if errors:
            raise ValidationError(errors)
    
    @property
    def esta_en_acreditacion(self):
        """Verifica si el torneo está en período de acreditación"""
        now = timezone.now()
        return self.fecha_acreditacion_inicio <= now <= self.fecha_acreditacion_fin
    
    @property
    def esta_en_competencia(self):
        """Verifica si el torneo está en período de competencia"""
        now = timezone.now()
        return self.fecha_competencia_inicio <= now <= self.fecha_competencia_fin
    
    @property
    def esta_en_entrega_premios(self):
        """Verifica si está en el período de entrega de premios"""
        now = timezone.now()
        # Consideramos 24 horas después del evento para entrega de premios
        fecha_limite_premios = self.fecha_premios + timezone.timedelta(hours=24)
        return self.fecha_premios <= now <= fecha_limite_premios


class TournamentMentor(models.Model):
    """Asignación de mentores a distritos para un torneo"""
    torneo = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='mentores_asignados',
        verbose_name='Torneo'
    )
    mentor = models.ForeignKey(
        Personaje,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'mentor'},
        related_name='torneos_mentoreo',
        verbose_name='Mentor'
    )
    distrito = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='mentores_torneo',
        verbose_name='Distrito'
    )
    
    # Metadatos de asignación
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    asignado_por = models.ForeignKey(
        Personaje,
        on_delete=models.SET_NULL,
        null=True,
        related_name='asignaciones_mentores_realizadas',
        limit_choices_to={'rol': 'jefe_capitolio'},
        verbose_name='Asignado por'
    )
    
    # Estado de la asignación
    es_activa = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Mentor de Torneo'
        verbose_name_plural = 'Mentores de Torneo'
        unique_together = [['torneo', 'distrito']]
        ordering = ['torneo', 'distrito']
    
    def __str__(self):
        return f"{self.mentor.get_full_name()} - {self.distrito.name} ({self.torneo.nombre})"
    
    def clean(self):
        """Valida que no haya otro mentor activo para el mismo distrito en este torneo"""
        if not self.es_activa:
            return
        
        duplicados = TournamentMentor.objects.filter(
            torneo=self.torneo,
            distrito=self.distrito,
            es_activa=True
        )
        
        if self.pk:
            duplicados = duplicados.exclude(pk=self.pk)
        
        if duplicados.exists():
            raise ValidationError(
                f'Ya existe un mentor activo asignado al {self.distrito.name} '
                f'en el torneo {self.torneo.nombre}'
            )


class TournamentVigilante(models.Model):
    """Asignación de vigilantes a un torneo"""
    torneo = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='vigilantes_asignados',
        verbose_name='Torneo'
    )
    vigilante = models.ForeignKey(
        Personaje,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'vigilante'},
        related_name='torneos_vigilancia',
        verbose_name='Vigilante'
    )
    
    # Rol específico del vigilante
    ROL_CHOICES = [
        ('general', 'Vigilante General'),
        ('acreditacion', 'Vigilante de Acreditación'),
        ('competencia', 'Vigilante de Competencia'),
        ('premios', 'Vigilante de Entrega de Premios'),
    ]
    
    rol_en_torneo = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default='general',
        verbose_name='Rol en el Torneo'
    )
    
    # Metadatos de asignación
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    asignado_por = models.ForeignKey(
        Personaje,
        on_delete=models.SET_NULL,
        null=True,
        related_name='asignaciones_vigilantes_realizadas',
        limit_choices_to={'rol': 'jefe_capitolio'},
        verbose_name='Asignado por'
    )
    
    # Estado de la asignación
    es_activa = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Vigilante de Torneo'
        verbose_name_plural = 'Vigilantes de Torneo'
        unique_together = [['torneo', 'vigilante']]
        ordering = ['torneo', 'rol_en_torneo']
    
    def __str__(self):
        return f"{self.vigilante.get_full_name()} - {self.get_rol_en_torneo_display()} ({self.torneo.nombre})"


class TournamentStatus(models.Model):
    """Registra el historial de cambios de estado del torneo"""
    torneo = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name='historial_estado',
        verbose_name='Torneo'
    )
    estado_anterior = models.CharField(
        max_length=20,
        choices=Tournament._meta.get_field('estado').choices
    )
    estado_nuevo = models.CharField(
        max_length=20,
        choices=Tournament._meta.get_field('estado').choices
    )
    cambio_por = models.ForeignKey(
        Personaje,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Cambio realizado por'
    )
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    razon = models.TextField(blank=True, null=True, verbose_name='Razón del cambio')
    
    class Meta:
        verbose_name = 'Cambio de Estado de Torneo'
        verbose_name_plural = 'Cambios de Estado de Torneo'
        ordering = ['-fecha_cambio']
    
    def __str__(self):
        return f"{self.torneo.nombre}: {self.estado_anterior} → {self.estado_nuevo}"
