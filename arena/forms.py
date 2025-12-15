from django import forms
from .models import Torneo, Reto, MentorDistrito, ParticipacionTributo, CasoDePrueba


class TorneoForm(forms.ModelForm):
    """Formulario para crear y editar torneos"""
    
    class Meta:
        model = Torneo
        fields = [
            'nombre', 'edicion', 'descripcion', 'imagen',
            'fecha_inicio', 'fecha_fin',
            'fecha_inscripcion_inicio', 'fecha_inscripcion_fin',
            'estado', 'is_activo',
            'puntos_minimos_ganar', 'permite_equipos', 'puntuacion_por_distrito'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del torneo'}),
            'edicion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edición'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del torneo'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_inscripcion_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_inscripcion_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'puntos_minimos_ganar': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '100'}),
            'is_activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'permite_equipos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puntuacion_por_distrito': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RetoForm(forms.ModelForm):
    """Formulario para crear y editar retos"""
    
    class Meta:
        model = Reto
        fields = [
            'torneo', 'titulo', 'descripcion', 'enunciado',
            'dificultad', 'tipo', 'categoria',
            'puntos_base', 'puntos_bonus',
            'fecha_publicacion', 'fecha_limite',
            'is_activo', 'is_visible',
            'tiene_validacion_automatica', 'lenguajes_permitidos',
            'tests_ocultos', 'limite_tiempo', 'limite_memoria',
            'archivo_datos'
        ]
        widgets = {
            'torneo': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del reto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción breve'}),
            'enunciado': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Enunciado completo del problema'}),
            'dificultad': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: algoritmos, estructuras de datos'}),
            'puntos_base': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '10'}),
            'puntos_bonus': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5'}),
            'fecha_publicacion': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_limite': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiene_validacion_automatica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lenguajes_permitidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'python,javascript,java'}),
            'tests_ocultos': forms.Textarea(attrs={
                'class': 'form-control font-monospace',
                'rows': 12,
                'placeholder': '{"python": [{"name": "Test 1", "function_call": {"name": "funcion", "args": [2, 3]}, "expected": "5"}]}',
                'style': 'font-family: monospace; font-size: 13px;'
            }),
            'limite_tiempo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '5.0',
                'step': '0.1',
                'min': '0.1'
            }),
            'limite_memoria': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '256',
                'min': '64'
            }),
            'archivo_datos': forms.FileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'tests_ocultos': 'Tests ocultos en formato JSON por lenguaje. NUNCA serán visibles para tributos.',
            'limite_tiempo': 'Tiempo máximo de ejecución en segundos (ej: 5.0)',
            'limite_memoria': 'Memoria máxima en MB (ej: 256)',
        }


class CasoDePruebaForm(forms.ModelForm):
    """Formulario para crear y editar casos de prueba"""
    
    class Meta:
        model = CasoDePrueba
        fields = [
            'reto', 'nombre', 'entrada', 'salida_esperada',
            'is_visible', 'es_ejemplo', 'puntos', 'orden'
        ]
        widgets = {
            'reto': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del caso'}),
            'entrada': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Datos de entrada'}),
            'salida_esperada': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Salida esperada'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'es_ejemplo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'puntos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1'}),
        }


class MentorDistritoForm(forms.ModelForm):
    """Formulario para asignar mentores a distritos"""
    
    class Meta:
        model = MentorDistrito
        fields = ['mentor', 'distrito', 'torneo']
        widgets = {
            'mentor': forms.Select(attrs={'class': 'form-control'}),
            'distrito': forms.Select(attrs={'class': 'form-control'}),
            'torneo': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo mentores activos
        from capitol.models import Personaje
        self.fields['mentor'].queryset = Personaje.objects.filter(rol='mentor', is_active=True)


class ParticipacionTributoForm(forms.ModelForm):
    """Formulario para que tributos envíen sus soluciones"""
    
    class Meta:
        model = ParticipacionTributo
        fields = ['lenguaje', 'codigo_solucion']
        widgets = {
            'lenguaje': forms.Select(attrs={'class': 'form-control'}),
            'codigo_solucion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 20,
                'placeholder': '# Escribe tu código aquí...',
                'style': 'font-family: monospace; font-size: 14px;'
            }),
        }
    
    def __init__(self, *args, reto=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Si se pasa el reto, filtrar lenguajes permitidos
        if reto and reto.lenguajes_permitidos:
            lenguajes = reto.lenguajes_permitidos.split(',')
            choices = [(lang.strip(), lang.strip().capitalize()) for lang in lenguajes]
            self.fields['lenguaje'].widget = forms.Select(
                choices=choices,
                attrs={'class': 'form-control'}
            )