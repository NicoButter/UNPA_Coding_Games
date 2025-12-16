from django.db import models
from django.core.validators import MinValueValidator
from capitol.models import TributoInfo
from arena.models import Reto


class Submission(models.Model):
    """
    Representa una entrega de código por parte de un tributo para evaluación automática.
    Almacena el código enviado, el lenguaje usado y los resultados de la ejecución.
    """
    VEREDICTO_CHOICES = [
        ('AC', 'Accepted'),  # Todos los tests pasaron
        ('WA', 'Wrong Answer'),  # Output incorrecto
        ('TLE', 'Time Limit Exceeded'),  # Excedió el tiempo límite
        ('MLE', 'Memory Limit Exceeded'),  # Excedió el límite de memoria
        ('RE', 'Runtime Error'),  # Error durante la ejecución
        ('CE', 'Compilation Error'),  # Error de compilación (Java)
        ('SE', 'System Error'),  # Error del sistema de evaluación
        ('PE', 'Pending'),  # Aún no evaluado
    ]
    
    LENGUAJE_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('javascript', 'JavaScript'),
    ]
    
    # Relaciones
    tributo = models.ForeignKey(
        TributoInfo,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Tributo'
    )
    reto = models.ForeignKey(
        Reto,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Reto'
    )
    
    # Código enviado
    lenguaje = models.CharField(
        max_length=20,
        choices=LENGUAJE_CHOICES,
        verbose_name='Lenguaje de Programación'
    )
    codigo = models.TextField(
        verbose_name='Código Fuente',
        help_text='Código enviado por el tributo'
    )
    
    # Resultados de evaluación
    veredicto = models.CharField(
        max_length=3,
        choices=VEREDICTO_CHOICES,
        default='PE',
        verbose_name='Veredicto'
    )
    puntos_obtenidos = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Puntos Obtenidos'
    )
    casos_pasados = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Casos de Prueba Pasados'
    )
    casos_totales = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Casos de Prueba Totales'
    )
    
    # Métricas de ejecución
    tiempo_ejecucion = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo de Ejecución (segundos)',
        help_text='Tiempo total de ejecución de todos los tests'
    )
    memoria_usada = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Memoria Usada (MB)'
    )
    
    # Salidas de ejecución
    stdout = models.TextField(
        blank=True,
        verbose_name='Salida Estándar',
        help_text='Output del programa (stdout)'
    )
    stderr = models.TextField(
        blank=True,
        verbose_name='Salida de Error',
        help_text='Errores del programa (stderr)'
    )
    
    # Detalles adicionales (JSON con resultados por cada test)
    detalles_ejecucion = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Detalles de Ejecución',
        help_text='Resultados detallados de cada caso de prueba (no visible para tributos)'
    )
    
    # Fechas
    fecha_envio = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Envío'
    )
    fecha_evaluacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Evaluación'
    )
    
    class Meta:
        verbose_name = 'Entrega de Código'
        verbose_name_plural = 'Entregas de Código'
        ordering = ['-fecha_envio']
        indexes = [
            models.Index(fields=['tributo', 'reto']),
            models.Index(fields=['veredicto']),
            models.Index(fields=['fecha_envio']),
        ]
    
    def __str__(self):
        return f"Submission #{self.id} - {self.tributo.personaje.get_full_name()} - {self.reto.titulo} ({self.veredicto})"
    
    @property
    def es_aceptado(self):
        """Verifica si la solución fue aceptada (AC)"""
        return self.veredicto == 'AC'
    
    @property
    def porcentaje_exito(self):
        """Calcula el porcentaje de tests pasados"""
        if self.casos_totales == 0:
            return 0
        return round((self.casos_pasados / self.casos_totales) * 100, 2)


class TestCaseResult(models.Model):
    """
    Resultado de la ejecución de un caso de prueba individual.
    Almacena el resultado detallado de cada test case ejecutado.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('RUNNING', 'Ejecutando'),
        ('PASSED', 'Pasado'),
        ('FAILED', 'Fallido'),
        ('TIMEOUT', 'Tiempo Excedido'),
        ('MEMORY_ERROR', 'Error de Memoria'),
        ('RUNTIME_ERROR', 'Error de Ejecución'),
        ('ERROR', 'Error del Sistema'),
    ]
    
    # Relaciones
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='test_results',
        verbose_name='Entrega'
    )
    test_case = models.ForeignKey(
        'challenges.TestCase',
        on_delete=models.CASCADE,
        related_name='execution_results',
        verbose_name='Caso de Prueba'
    )
    
    # Resultado
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='Estado'
    )
    passed = models.BooleanField(
        default=False,
        verbose_name='Pasado'
    )
    
    # Datos de ejecución
    actual_output = models.TextField(
        blank=True,
        verbose_name='Salida Real',
        help_text='Output generado por el código del tributo'
    )
    execution_time = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Tiempo de Ejecución (segundos)'
    )
    memory_used = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Memoria Usada (MB)'
    )
    
    # Errores
    error_message = models.TextField(
        blank=True,
        verbose_name='Mensaje de Error',
        help_text='Mensaje de error si el test falló'
    )
    
    # Metadatos
    executed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Ejecutado en'
    )
    
    class Meta:
        verbose_name = 'Resultado de Test Case'
        verbose_name_plural = 'Resultados de Test Cases'
        ordering = ['submission', 'test_case__order']
        unique_together = ['submission', 'test_case']
    
    def __str__(self):
        return f"Test Result - Submission #{self.submission.id} - Test #{self.test_case.id} ({self.status})"
