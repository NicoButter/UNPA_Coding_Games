from django.contrib.auth.models import AbstractUser
from django.db import models

class Personaje(AbstractUser):
    ROL_CHOICES = [
        ('tributo', 'Tributo'),
        ('vigilante', 'Vigilante'),
        ('jefe_capitolio', 'Jefe del Capitolio'),
    ]
    rol = models.CharField(max_length=15, choices=ROL_CHOICES, default='tributo')

class TributoInfo(models.Model):
    TIPOS_CHOICES = [
        ('alumno', 'Alumno de Unidad Académica'),
        ('externo', 'Persona Externa'),
    ]
    
    personaje = models.OneToOneField(Personaje, on_delete=models.CASCADE)
    numero_tributo = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=10, choices=TIPOS_CHOICES, default='externo')
    unidad_academica = models.CharField(max_length=100, blank=True, null=True)
    distrito = models.IntegerField()
    edad = models.IntegerField()
    habilidades = models.TextField()
    fuerza = models.IntegerField()

    def __str__(self):
        return f"{self.personaje.username} - Número de Tributo: {self.numero_tributo} - Tipo: {self.tipo} - Distrito {self.distrito}"