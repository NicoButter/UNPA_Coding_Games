from django.contrib.auth.models import AbstractUser
from django.db import models

class Personaje(AbstractUser):
    ROL_CHOICES = [
        ('tributo', 'Tributo'),
        ('vigilante', 'Vigilante'),
        ('jefe_capitolio', 'Jefe del Capitolio'),
    ]
    rol = models.CharField(max_length=15, choices=ROL_CHOICES, default='tributo')
