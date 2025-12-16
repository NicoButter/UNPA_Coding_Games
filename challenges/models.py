from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify


class Challenge(models.Model):
    """
    Modelo base de un reto de programación.
    Independiente de torneos - puede reutilizarse en múltiples competencias.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Fácil'),
        ('medium', 'Medio'),
        ('hard', 'Difícil'),
        ('expert', 'Experto'),
    ]
    
    # Identificación
    title = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(unique=True, max_length=220)
    
    # Descripción del problema
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción general del problema'
    )
    statement = models.TextField(
        verbose_name='Enunciado Completo',
        help_text='Enunciado detallado con ejemplos y explicaciones'
    )
    
    # Clasificación
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy',
        verbose_name='Dificultad'
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Categoría',
        help_text='Ej: Algoritmos, Estructuras de Datos, Matemáticas, etc.'
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Etiquetas',
        help_text='Tags para filtrado: ["arrays", "recursion", "dynamic-programming"]'
    )
    
    # Configuración de ejecución
    time_limit = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Límite de Tiempo (segundos)',
        help_text='Tiempo máximo de ejecución por caso de prueba'
    )
    memory_limit = models.PositiveIntegerField(
        default=128,
        validators=[MinValueValidator(64)],
        verbose_name='Límite de Memoria (MB)',
        help_text='Memoria máxima permitida'
    )
    
    # Lenguajes permitidos
    allowed_languages = models.JSONField(
        default=list,
        verbose_name='Lenguajes Permitidos',
        help_text='Lista de lenguajes: ["python", "java", "javascript", "cpp"]'
    )
    
    # Configuración de puntuación (base - puede ser sobrescrito por TorneoChallenge)
    base_points = models.PositiveIntegerField(
        default=100,
        verbose_name='Puntos Base'
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Si está activo y disponible para usar'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Público',
        help_text='Si es visible públicamente o solo en torneos específicos'
    )
    
    # Archivos de soporte
    input_format_description = models.TextField(
        blank=True,
        verbose_name='Formato de Entrada',
        help_text='Descripción del formato de entrada esperado'
    )
    output_format_description = models.TextField(
        blank=True,
        verbose_name='Formato de Salida',
        help_text='Descripción del formato de salida esperado'
    )
    constraints = models.TextField(
        blank=True,
        verbose_name='Restricciones',
        help_text='Restricciones del problema (rangos de valores, etc.)'
    )
    
    # Plantillas de código inicial (opcional)
    code_templates = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Plantillas de Código',
        help_text='Código inicial por lenguaje: {"python": "def solve():\\n    pass", ...}'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'capitol.Personaje',
        on_delete=models.SET_NULL,
        null=True,
        related_name='challenges_created',
        verbose_name='Creado por'
    )
    
    class Meta:
        verbose_name = 'Challenge'
        verbose_name_plural = 'Challenges'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def total_test_cases(self):
        """Retorna el número total de casos de prueba"""
        return self.test_cases.count()
    
    @property
    def visible_test_cases(self):
        """Retorna el número de casos de prueba visibles"""
        return self.test_cases.filter(is_visible=True).count()


class TestCase(models.Model):
    """
    Caso de prueba para un challenge.
    Cada challenge puede tener múltiples test cases.
    """
    challenge = models.ForeignKey(
        Challenge,
        related_name='test_cases',
        on_delete=models.CASCADE,
        verbose_name='Challenge'
    )
    
    # Datos del test
    input_data = models.TextField(
        verbose_name='Entrada',
        help_text='Datos de entrada para el test'
    )
    expected_output = models.TextField(
        verbose_name='Salida Esperada',
        help_text='Salida correcta esperada'
    )
    
    # Metadatos del test
    name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Nombre del Test',
        help_text='Nombre descriptivo del caso de prueba'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción opcional de qué prueba este caso'
    )
    
    # Configuración
    is_visible = models.BooleanField(
        default=False,
        verbose_name='Visible',
        help_text='Si el tributo puede ver este test case (test de ejemplo)'
    )
    is_sample = models.BooleanField(
        default=False,
        verbose_name='Es Ejemplo',
        help_text='Si es un caso de ejemplo mostrado en el enunciado'
    )
    weight = models.PositiveIntegerField(
        default=1,
        verbose_name='Peso',
        help_text='Peso del test case para el cálculo de puntuación'
    )
    
    # Orden
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de ejecución del test'
    )
    
    # Configuración específica (puede sobrescribir la del challenge)
    custom_time_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Límite de Tiempo Personalizado (segundos)',
        help_text='Si se especifica, sobrescribe el límite del challenge'
    )
    custom_memory_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Límite de Memoria Personalizado (MB)',
        help_text='Si se especifica, sobrescribe el límite del challenge'
    )
    
    class Meta:
        verbose_name = 'Caso de Prueba'
        verbose_name_plural = 'Casos de Prueba'
        ordering = ['challenge', 'order', 'id']
        unique_together = ['challenge', 'order']
    
    def __str__(self):
        name = self.name or f"Test #{self.id}"
        return f"{self.challenge.title} - {name}"
    
    @property
    def time_limit(self):
        """Retorna el límite de tiempo efectivo (custom o del challenge)"""
        return self.custom_time_limit or self.challenge.time_limit
    
    @property
    def memory_limit(self):
        """Retorna el límite de memoria efectivo (custom o del challenge)"""
        return self.custom_memory_limit or self.challenge.memory_limit
