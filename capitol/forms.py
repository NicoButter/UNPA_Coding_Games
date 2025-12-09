from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Personaje, TributoInfo

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nombre de usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )

class PersonajeRegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    first_name = forms.CharField(
        required=True,
        label='Nombre',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre'
        })
    )
    last_name = forms.CharField(
        required=True,
        label='Apellido',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu apellido'
        })
    )
    telefono = forms.CharField(
        required=False,
        label='Teléfono',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+54 9 ...'
        })
    )
    fecha_nacimiento = forms.DateField(
        required=False,
        label='Fecha de Nacimiento',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    foto = forms.ImageField(
        required=False,
        label='Foto para Credencial',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )
    
    class Meta:
        model = Personaje
        fields = ('username', 'email', 'first_name', 'last_name', 'telefono', 
                  'fecha_nacimiento', 'foto', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Elige un nombre de usuario'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña segura'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Repite la contraseña'
        })

class TributoInfoForm(forms.ModelForm):
    class Meta:
        model = TributoInfo
        fields = ['tipo', 'unidad_academica', 'carrera', 'año_carrera', 
                  'distrito', 'nivel', 'institucion_origen', 'ciudad', 
                  'provincia', 'lenguajes_programacion', 'experiencia_previa', 
                  'motivacion']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'unidad_academica': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: UACO, UART, etc.'
            }),
            'carrera': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Licenciatura en Sistemas'
            }),
            'año_carrera': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 6
            }),
            'distrito': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 13,
                'value': 12
            }),
            'nivel': forms.Select(attrs={'class': 'form-control'}),
            'institucion_origen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Para participantes externos'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu ciudad'
            }),
            'provincia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu provincia'
            }),
            'lenguajes_programacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Python, Java, C++, JavaScript...'
            }),
            'experiencia_previa': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe tu experiencia en programación competitiva...'
            }),
            'motivacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '¿Por qué quieres participar en los Hunger Games de Código?'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos condicionales según el tipo
        self.fields['unidad_academica'].required = False
        self.fields['carrera'].required = False
        self.fields['año_carrera'].required = False
        self.fields['institucion_origen'].required = False

