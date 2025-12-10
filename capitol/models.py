from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

class Personaje(AbstractUser):
    ROL_CHOICES = [
        ('tributo', 'Tributo'),
        ('vigilante', 'Vigilante'),
        ('mentor', 'Mentor'),
        ('jefe_capitolio', 'Jefe del Capitolio'),
    ]
    rol = models.CharField(max_length=15, choices=ROL_CHOICES, default='tributo')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to='tributos/fotos/', blank=True, null=True)
    
    # Campos específicos para mentores
    unidad_academica = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name='Unidad Académica',
        help_text='Unidad Académica/Sede UNPA que representa (solo para mentores)'
    )
    distrito_asignado = models.IntegerField(
        blank=True, 
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(13)],
        help_text='Distrito asignado al mentor (1-13)'
    )
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

class TributoInfo(models.Model):
    TIPOS_CHOICES = [
        ('alumno_unpa', 'Alumno UNPA'),
        ('externo', 'Participante Externo'),
    ]
    
    NIVEL_CHOICES = [
        ('novato', 'Novato'),
        ('experimentado', 'Experimentado'),
        ('avanzado', 'Avanzado'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de Acreditación'),
        ('acreditado', 'Acreditado'),
        ('activo', 'Activo en Competencia'),
        ('eliminado', 'Eliminado'),
        ('ganador', 'Ganador'),
    ]
    
    # Relación con usuario
    personaje = models.OneToOneField(Personaje, on_delete=models.CASCADE, related_name='tributo_info')
    
    # Relación jerárquica con mentor
    mentor = models.ForeignKey(
        Personaje,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tributos_asignados',
        limit_choices_to={'rol': 'mentor'},
        verbose_name='Mentor Asignado',
        help_text='Mentor que representa al tributo (su "Haymitch")'
    )
    
    # Información de identificación
    codigo_tributo = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    numero_tributo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    # Tipo y origen
    tipo = models.CharField(max_length=15, choices=TIPOS_CHOICES, default='externo')
    unidad_academica = models.CharField(max_length=100, blank=True, null=True, verbose_name='Unidad Académica UNPA')
    carrera = models.CharField(max_length=100, blank=True, null=True)
    año_carrera = models.IntegerField(blank=True, null=True, verbose_name='Año de Carrera')
    
    # Información del tributo
    distrito = models.IntegerField(default=12, help_text='Distrito de procedencia (1-13)')
    nivel = models.CharField(max_length=15, choices=NIVEL_CHOICES, default='novato')
    
    # Información adicional
    institucion_origen = models.CharField(max_length=150, blank=True, null=True, help_text='Para participantes externos')
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    
    # Habilidades y experiencia
    lenguajes_programacion = models.TextField(blank=True, null=True, help_text='Separados por comas')
    experiencia_previa = models.TextField(blank=True, null=True)
    motivacion = models.TextField(blank=True, null=True)
    
    # Sistema de acreditación
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_acreditacion = models.DateTimeField(blank=True, null=True)
    qr_code = models.ImageField(upload_to='tributos/qr_codes/', blank=True, null=True)
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    # Credencial digital
    credencial_generada = models.BooleanField(default=False)
    fecha_generacion_credencial = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Información de Tributo'
        verbose_name_plural = 'Información de Tributos'
        ordering = ['-fecha_registro']
    
    def save(self, *args, **kwargs):
        # Detectar si es una creación nueva
        is_new = self.pk is None
        
        # Generar código de tributo si no existe
        if not self.codigo_tributo:
            self.codigo_tributo = self.generar_codigo_tributo()
        
        # Generar QR code si no existe
        if not self.qr_code:
            self.generar_qr_code()
        
        super().save(*args, **kwargs)
        
        # Si es nuevo y no se ha enviado credencial, enviar email
        if is_new and not self.credencial_generada:
            # Importar aquí para evitar import circular
            from .views import enviar_gafete_email
            enviar_gafete_email(self)
    
    def generar_codigo_tributo(self):
        """Genera un código único para el tributo (ej: T-12-045)"""
        ultimo_tributo = TributoInfo.objects.filter(distrito=self.distrito).order_by('-id').first()
        if ultimo_tributo and ultimo_tributo.numero_tributo:
            try:
                ultimo_numero = int(ultimo_tributo.numero_tributo.split('-')[-1])
                nuevo_numero = ultimo_numero + 1
            except:
                nuevo_numero = 1
        else:
            nuevo_numero = 1
        
        return f"T-{self.distrito:02d}-{nuevo_numero:03d}"
    
    def generar_qr_code(self):
        """Genera el código QR con el token único del tributo"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Datos del QR: token único
        qr_data = f"TRIBUTO:{self.qr_token}"
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Crear imagen del QR
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Guardar en BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Guardar en el campo
        filename = f'qr_{self.qr_token}.png'
        self.qr_code.save(filename, File(buffer), save=False)
    
    def acreditar(self):
        """Acredita al tributo y genera su credencial"""
        self.estado = 'acreditado'
        self.fecha_acreditacion = timezone.now()
        self.save()
    
    def get_color_borde(self):
        """Retorna el color de borde según el tipo de tributo"""
        if self.tipo == 'alumno_unpa':
            return '#FFD700'  # Dorado
        elif self.personaje.rol == 'mentor':
            return '#9B30FF'  # Púrpura
        else:
            return '#C0C0C0'  # Plateado
    
    def __str__(self):
        return f"{self.codigo_tributo} - {self.personaje.get_full_name()} ({self.get_tipo_display()})"