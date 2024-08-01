from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Personaje

class CustomAuthenticationForm(AuthenticationForm):
    pass  # Agregar campos personalizados

class PersonajeCreationForm(UserCreationForm):
    class Meta:
        model = Personaje
        fields = ('username', 'email', 'first_name', 'last_name', 'rol')
