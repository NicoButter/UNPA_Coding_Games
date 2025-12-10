from django import forms
from capitol.models import Personaje, TributoInfo
from arena.models import Torneo, AyudaMentor


class AsignarMentorForm(forms.ModelForm):
    """Formulario para asignar mentor a un distrito/unidad académica"""
    class Meta:
        model = Personaje
        fields = ['unidad_academica', 'distrito_asignado']
        widgets = {
            'unidad_academica': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: UARG - Río Gallegos'
            }),
            'distrito_asignado': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 13,
                'placeholder': 'Distrito (1-13)'
            }),
        }


class AsignarVigilantesForm(forms.ModelForm):
    """Formulario para asignar vigilantes a un torneo"""
    vigilantes = forms.ModelMultipleChoiceField(
        queryset=Personaje.objects.filter(rol='vigilante'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Seleccionar Vigilantes (Peacekeepers)'
    )
    
    class Meta:
        model = Torneo
        fields = ['vigilantes']


class AsignarTributoMentorForm(forms.ModelForm):
    """Formulario para asignar mentor a un tributo"""
    mentor = forms.ModelChoiceField(
        queryset=Personaje.objects.filter(rol='mentor'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label='Seleccionar Mentor',
        empty_label='Sin mentor asignado'
    )
    
    class Meta:
        model = TributoInfo
        fields = ['mentor']


class EnviarAyudaForm(forms.ModelForm):
    """Formulario para que el mentor envíe ayudas a sus tributos"""
    tributo = forms.ModelChoiceField(
        queryset=TributoInfo.objects.none(),  # Se establece dinámicamente en la vista
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tributo Destinatario'
    )
    
    class Meta:
        model = AyudaMentor
        fields = ['tributo', 'tipo', 'titulo', 'contenido', 'reto']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título breve de la ayuda'
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Escribe aquí la pista, ejemplo o mensaje motivacional...'
            }),
            'reto': forms.Select(attrs={
                'class': 'form-control',
                'required': False
            }),
        }
    
    def __init__(self, *args, mentor=None, **kwargs):
        super().__init__(*args, **kwargs)
        if mentor:
            # Solo mostrar tributos asignados a este mentor
            self.fields['tributo'].queryset = TributoInfo.objects.filter(
                mentor=mentor
            ).select_related('personaje')
