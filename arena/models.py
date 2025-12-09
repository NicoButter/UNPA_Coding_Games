from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from capitol.models import Personaje, TributoInfo


class Torneo(models.Model):
    """Representa un torneo/competencia anual de programación"""
    ESTADO_CHOICES = [
        ('configuracion', 'En Configuración'),
        ('inscripcion', 'Inscripción Abierta'),
        ('en_curso', 'En Curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    nombre = models.CharField(max_length=200, verbose_name='Nombre del Torneo')
    descripcion = models.TextField(blank=True, null=True)
    edicion = models.IntegerField(verbose_name='Número de Edición', help_text='Ej: 75 para "75th Hunger Games"')
    
    # Fechas
    fecha_inicio = models.DateTimeField(verbose_name='Fecha de Inicio')
    fecha_fin = models.DateTimeField(verbose_name='Fecha de Finalización')
    fecha_inscripcion_inicio = models.DateTimeField(verbose_name='Inicio de Inscripciones', blank=True, null=True)
    fecha_inscripcion_fin = models.DateTimeField(verbose_name='Fin de Inscripciones', blank=True, null=True)
    
    # Estado y configuración
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='configuracion')
    is_activo = models.BooleanField(default=True, verbose_name='Torneo Activo')
    
    # Reglas y configuración
    puntos_minimos_ganar = models.IntegerField(default=0, help_text='Puntos mínimos para ganar')
    permite_equipos = models.BooleanField(default=False, help_text='Permite competencia por equipos')
    puntuacion_por_distrito = models.BooleanField(default=True, help_text='Los puntos suman al distrito')
    
    # Meta información
    creado_por = models.ForeignKey(Personaje, on_delete=models.SET_NULL, null=True, related_name='torneos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Imagen del torneo
    imagen = models.ImageField(upload_to='torneos/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Torneo'
        verbose_name_plural = 'Torneos'
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.nombre} - Edición {self.edicion}"
    
    @property
    def esta_en_inscripcion(self):
        """Verifica si el torneo está en periodo de inscripción"""
        now = timezone.now()
        if self.fecha_inscripcion_inicio and self.fecha_inscripcion_fin:
            return self.fecha_inscripcion_inicio <= now <= self.fecha_inscripcion_fin
        return False
    
    @property
    def esta_en_curso(self):
        """Verifica si el torneo está actualmente en curso"""
        now = timezone.now()
        return self.fecha_inicio <= now <= self.fecha_fin and self.estado == 'en_curso'


class MentorDistrito(models.Model):
    """Asignación de mentores a distritos para un torneo específico"""
    mentor = models.ForeignKey(
        Personaje, 
        on_delete=models.CASCADE, 
        limit_choices_to={'rol': 'mentor'},
        related_name='distritos_asignados'
    )
    distrito = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(13)],
        verbose_name='Número de Distrito'
    )
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='asignaciones_mentores')
    
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    asignado_por = models.ForeignKey(
        Personaje,
        on_delete=models.SET_NULL,
        null=True,
        related_name='asignaciones_realizadas'
    )
    
    class Meta:
        verbose_name = 'Asignación de Mentor'
        verbose_name_plural = 'Asignaciones de Mentores'
        unique_together = [['mentor', 'torneo'], ['distrito', 'torneo']]
        ordering = ['torneo', 'distrito']
    
    def __str__(self):
        return f"{self.mentor.get_full_name()} - Distrito {self.distrito} ({self.torneo.nombre})"


class Reto(models.Model):
    """Representa un desafío/reto de programación dentro de un torneo"""
    DIFICULTAD_CHOICES = [
        ('novato', 'Novato'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('experto', 'Experto'),
    ]
    
    TIPO_CHOICES = [
        ('individual', 'Individual'),
        ('equipo', 'Por Equipo'),
        ('distrito', 'Por Distrito'),
    ]
    
    # Relación con torneo
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='retos')
    
    # Información básica
    titulo = models.CharField(max_length=200, verbose_name='Título del Reto')
    descripcion = models.TextField(verbose_name='Descripción del Problema')
    enunciado = models.TextField(verbose_name='Enunciado Completo', help_text='Descripción detallada del problema')
    
    # Clasificación
    dificultad = models.CharField(max_length=15, choices=DIFICULTAD_CHOICES, default='novato')
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='individual')
    categoria = models.CharField(max_length=100, blank=True, null=True, help_text='Ej: Algoritmos, Estructuras de Datos, etc.')
    
    # Puntuación
    puntos_base = models.IntegerField(default=100, validators=[MinValueValidator(0)])
    puntos_bonus = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text='Puntos extra por completar rápido')
    
    # Fechas
    fecha_publicacion = models.DateTimeField(verbose_name='Fecha de Publicación')
    fecha_limite = models.DateTimeField(verbose_name='Fecha Límite', blank=True, null=True)
    
    # Estado
    is_activo = models.BooleanField(default=True, verbose_name='Reto Activo')
    is_visible = models.BooleanField(default=True, verbose_name='Visible para Tributos')
    
    # Validación automática
    tiene_validacion_automatica = models.BooleanField(default=False)
    lenguajes_permitidos = models.CharField(
        max_length=200,
        default='python,java,cpp,javascript',
        help_text='Lenguajes permitidos separados por comas'
    )
    
    # Meta información
    creado_por = models.ForeignKey(Personaje, on_delete=models.SET_NULL, null=True, related_name='retos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Archivos adjuntos
    archivo_datos = models.FileField(upload_to='retos/datos/', blank=True, null=True, help_text='Archivos de datos de prueba')
    
    class Meta:
        verbose_name = 'Reto'
        verbose_name_plural = 'Retos'
        ordering = ['-fecha_publicacion']
    
    def __str__(self):
        return f"{self.titulo} ({self.torneo.nombre})"
    
    @property
    def esta_disponible(self):
        """Verifica si el reto está disponible para resolverse"""
        now = timezone.now()
        publicado = self.fecha_publicacion <= now
        no_vencido = not self.fecha_limite or now <= self.fecha_limite
        return self.is_activo and self.is_visible and publicado and no_vencido


class CasoDePrueba(models.Model):
    """Casos de prueba para validación automática de soluciones"""
    reto = models.ForeignKey(Reto, on_delete=models.CASCADE, related_name='casos_prueba')
    
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Caso')
    entrada = models.TextField(verbose_name='Entrada/Input')
    salida_esperada = models.TextField(verbose_name='Salida Esperada/Output')
    
    is_visible = models.BooleanField(default=True, help_text='Visible para los tributos (ejemplos)')
    es_ejemplo = models.BooleanField(default=False, help_text='Es un caso de ejemplo en el enunciado')
    puntos = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    
    orden = models.IntegerField(default=0, help_text='Orden de ejecución')
    
    class Meta:
        verbose_name = 'Caso de Prueba'
        verbose_name_plural = 'Casos de Prueba'
        ordering = ['reto', 'orden']
    
    def __str__(self):
        return f"{self.reto.titulo} - {self.nombre}"


class ParticipacionTributo(models.Model):
    """Registro de participación de un tributo en un reto"""
    ESTADO_CHOICES = [
        ('no_iniciado', 'No Iniciado'),
        ('en_progreso', 'En Progreso'),
        ('enviado', 'Enviado'),
        ('validando', 'En Validación'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
        ('tiempo_agotado', 'Tiempo Agotado'),
    ]
    
    tributo = models.ForeignKey(TributoInfo, on_delete=models.CASCADE, related_name='participaciones')
    reto = models.ForeignKey(Reto, on_delete=models.CASCADE, related_name='participaciones')
    
    # Estado y fechas
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='no_iniciado')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    fecha_completado = models.DateTimeField(blank=True, null=True)
    
    # Solución
    lenguaje = models.CharField(max_length=50, blank=True, null=True, help_text='Lenguaje de programación usado')
    codigo_solucion = models.TextField(blank=True, null=True, verbose_name='Código de la Solución')
    
    # Resultados
    puntos_obtenidos = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    casos_pasados = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    casos_totales = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    tiempo_ejecucion = models.FloatField(blank=True, null=True, help_text='Tiempo en segundos')
    
    # Retroalimentación
    output_validacion = models.TextField(blank=True, null=True, help_text='Resultado de la validación')
    comentarios_mentor = models.TextField(blank=True, null=True)
    
    # Intentos
    numero_intento = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    
    class Meta:
        verbose_name = 'Participación en Reto'
        verbose_name_plural = 'Participaciones en Retos'
        ordering = ['-fecha_inicio']
        unique_together = [['tributo', 'reto', 'numero_intento']]
    
    def __str__(self):
        return f"{self.tributo.personaje.get_full_name()} - {self.reto.titulo}"
    
    def calcular_puntos(self):
        """Calcula los puntos obtenidos basado en casos pasados"""
        if self.casos_totales > 0:
            porcentaje = self.casos_pasados / self.casos_totales
            self.puntos_obtenidos = int(self.reto.puntos_base * porcentaje)
            
            # Bonus por completar todos los casos
            if self.casos_pasados == self.casos_totales:
                self.puntos_obtenidos += self.reto.puntos_bonus
        
        return self.puntos_obtenidos


class RankingDistrito(models.Model):
    """Tabla de ranking por distrito en un torneo"""
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='rankings_distrito')
    distrito = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(13)])
    
    puntos_totales = models.IntegerField(default=0)
    retos_completados = models.IntegerField(default=0)
    tributos_activos = models.IntegerField(default=0)
    
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Ranking de Distrito'
        verbose_name_plural = 'Rankings de Distritos'
        unique_together = [['torneo', 'distrito']]
        ordering = ['-puntos_totales']
    
    def __str__(self):
        return f"Distrito {self.distrito} - {self.puntos_totales} pts ({self.torneo.nombre})"
