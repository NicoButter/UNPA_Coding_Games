"""
Sistema de puntos de patrocinio para el sistema de ayudas.
Los mentores tienen un presupuesto limitado de puntos para enviar ayudas.
"""

from django.db import models
from django.utils import timezone
from capitol.models import Personaje
from arena.models import Torneo, AyudaMentor


class PresupuestoMentor(models.Model):
    """
    Maneja el presupuesto de puntos de un mentor para enviar ayudas.
    Similar al sistema de patrocinio de Los Juegos del Hambre.
    """
    mentor = models.OneToOneField(
        Personaje,
        on_delete=models.CASCADE,
        related_name='presupuesto_patrocinio',
        limit_choices_to={'rol': 'mentor'}
    )
    
    # Puntos de patrocinio
    puntos_totales = models.IntegerField(
        default=1000,
        help_text='Puntos totales asignados al mentor'
    )
    puntos_usados = models.IntegerField(
        default=0,
        help_text='Puntos gastados en ayudas'
    )
    
    # Límites
    max_ayudas_por_dia = models.IntegerField(
        default=10,
        help_text='Número máximo de ayudas que puede enviar por día'
    )
    
    # Estadísticas
    total_ayudas_enviadas = models.IntegerField(default=0)
    ultima_ayuda_enviada = models.DateTimeField(blank=True, null=True)
    
    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Presupuesto de Mentor'
        verbose_name_plural = 'Presupuestos de Mentores'
    
    def __str__(self):
        return f"{self.mentor.get_full_name()} - {self.puntos_disponibles}/{self.puntos_totales} pts"
    
    @property
    def puntos_disponibles(self):
        """Puntos restantes para gastar"""
        return self.puntos_totales - self.puntos_usados
    
    def puede_enviar_ayuda(self, costo_puntos=0):
        """Verifica si el mentor puede enviar una ayuda"""
        # Verificar puntos
        if self.puntos_disponibles < costo_puntos:
            return False, "No tienes suficientes puntos de patrocinio"
        
        # Verificar límite diario
        hoy = timezone.now().date()
        ayudas_hoy = AyudaMentor.objects.filter(
            mentor=self.mentor,
            fecha_envio__date=hoy
        ).count()
        
        if ayudas_hoy >= self.max_ayudas_por_dia:
            return False, f"Has alcanzado el límite de {self.max_ayudas_por_dia} ayudas por día"
        
        return True, "OK"
    
    def gastar_puntos(self, cantidad):
        """Gasta puntos del presupuesto"""
        if self.puntos_disponibles >= cantidad:
            self.puntos_usados += cantidad
            self.total_ayudas_enviadas += 1
            self.ultima_ayuda_enviada = timezone.now()
            self.save()
            return True
        return False
    
    def recargar_puntos(self, cantidad):
        """Recarga puntos al presupuesto (usado por admin)"""
        self.puntos_totales += cantidad
        self.save()


# Configuración de costos por tipo de ayuda
COSTOS_AYUDAS = {
    'pista': 50,
    'ejemplo': 100,
    'recurso': 75,
    'motivacion': 25,
    'advertencia': 30,
}


def obtener_costo_ayuda(tipo_ayuda):
    """Retorna el costo en puntos de un tipo de ayuda"""
    return COSTOS_AYUDAS.get(tipo_ayuda, 50)


def crear_presupuesto_mentor(mentor):
    """Crea un presupuesto inicial para un mentor"""
    presupuesto, created = PresupuestoMentor.objects.get_or_create(
        mentor=mentor,
        defaults={
            'puntos_totales': 1000,
            'max_ayudas_por_dia': 10,
        }
    )
    return presupuesto
