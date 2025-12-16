from django import forms
from django.forms import ModelForm, inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Tournament, TournamentMentor, TournamentVigilante
from districts.models import District
from capitol.models import Personaje
from django.utils import timezone
from datetime import timedelta


class TournamentForm(ModelForm):
    """Formulario para crear/editar un torneo"""
    
    class Meta:
        model = Tournament
        fields = [
            'nombre', 'descripcion', 'numero_edicion',
            'fecha_acreditacion_inicio', 'fecha_acreditacion_fin',
            'fecha_competencia_inicio', 'fecha_competencia_fin',
            'fecha_premios',
            'permite_equipos', 'puntuacion_por_unidad',
            'puntos_minimos_ganar', 'imagen'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Hunger Games 2025',
                'maxlength': '255'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada del torneo'
            }),
            'numero_edicion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 75',
                'min': '1'
            }),
            'fecha_acreditacion_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_acreditacion_fin': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_competencia_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_competencia_fin': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_premios': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'permite_equipos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'puntuacion_por_unidad': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'puntos_minimos_ganar': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si es edición, pre-llenar con valores existentes
        if self.instance.pk:
            pass
        else:
            # Si es creación, sugerir fechas para mismo día
            now = timezone.now()
            today_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
            
            self.fields['fecha_acreditacion_inicio'].initial = today_start
            self.fields['fecha_acreditacion_fin'].initial = today_start + timedelta(hours=2)
            self.fields['fecha_competencia_inicio'].initial = today_start + timedelta(hours=2, minutes=30)
            self.fields['fecha_competencia_fin'].initial = today_start + timedelta(hours=7)
            self.fields['fecha_premios'].initial = today_start + timedelta(hours=8)
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Delegar la validación al modelo
        try:
            self.instance.clean()
        except ValidationError as e:
            raise ValidationError(e.message_dict)
        
        return cleaned_data


class TournamentMentorForm(ModelForm):
    """Formulario para asignar mentores a distritos"""
    
    class Meta:
        model = TournamentMentor
        fields = ['mentor', 'distrito', 'observaciones']
        widgets = {
            'mentor': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_mentor_select'
            }),
            'distrito': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_distrito_select'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales sobre la asignación (opcional)'
            })
        }
    
    def __init__(self, torneo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.torneo = torneo
        
        # Filtrar mentores activos solamente
        self.fields['mentor'].queryset = Personaje.objects.filter(rol='mentor', is_active=True)
        
        # Filtrar distritos activos
        self.fields['distrito'].queryset = District.objects.filter(is_active=True)
        
        # Si hay mentores ya asignados, excluirlos de las opciones disponibles
        mentores_asignados = TournamentMentor.objects.filter(
            torneo=torneo,
            es_activa=True
        ).values_list('mentor_id', flat=True)
        
        self.fields['mentor'].queryset = self.fields['mentor'].queryset.exclude(
            id__in=mentores_asignados
        )
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Delegar validación al modelo
        try:
            self.instance.torneo = self.torneo
            self.instance.clean()
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                raise ValidationError(e.message_dict)
            else:
                raise ValidationError(str(e))
        
        return cleaned_data


class TournamentVigilanteForm(ModelForm):
    """Formulario para asignar vigilantes al torneo"""
    
    class Meta:
        model = TournamentVigilante
        fields = ['vigilante', 'rol_en_torneo', 'observaciones']
        widgets = {
            'vigilante': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_vigilante_select'
            }),
            'rol_en_torneo': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_rol_select'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales sobre la asignación (opcional)'
            })
        }
    
    def __init__(self, torneo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.torneo = torneo
        
        # Filtrar vigilantes activos solamente
        self.fields['vigilante'].queryset = Personaje.objects.filter(rol='vigilante', is_active=True)
        
        # Si hay vigilantes ya asignados, excluirlos
        vigilantes_asignados = TournamentVigilante.objects.filter(
            torneo=torneo,
            es_activa=True
        ).values_list('vigilante_id', flat=True)
        
        self.fields['vigilante'].queryset = self.fields['vigilante'].queryset.exclude(
            id__in=vigilantes_asignados
        )


class TournamentMentorFormSet(forms.BaseInlineFormSet):
    """FormSet para asignar múltiples mentores a un torneo"""
    
    def __init__(self, *args, torneo=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.torneo = torneo
        
        for form in self.forms:
            if torneo:
                form.torneo = torneo
                
                # Actualizar querysets
                form.fields['mentor'].queryset = Personaje.objects.filter(
                    rol='mentor', 
                    is_active=True
                )
                form.fields['distrito'].queryset = District.objects.filter(
                    is_active=True
                )


class TournamentVigilanteFormSet(forms.BaseInlineFormSet):
    """FormSet para asignar múltiples vigilantes a un torneo"""
    
    def __init__(self, *args, torneo=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.torneo = torneo
        
        for form in self.forms:
            if torneo:
                form.torneo = torneo
                
                # Actualizar querysets
                form.fields['vigilante'].queryset = Personaje.objects.filter(
                    rol='vigilante',
                    is_active=True
                )


class AssignMentorsToDistritosForm(forms.Form):
    """
    Formulario para asignar mentores a todos los distritos de un torneo
    """
    torneo = forms.ModelChoiceField(
        queryset=Tournament.objects.filter(es_activo=True),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_torneo_assign'
        }),
        label='Torneo'
    )
    
    mentores = forms.ModelMultipleChoiceField(
        queryset=Personaje.objects.filter(rol='mentor', is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        label='Selecciona los Mentores a Asignar',
        help_text='Se asignarán automáticamente a los distritos'
    )
    
    distritos = forms.ModelMultipleChoiceField(
        queryset=District.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        label='Distritos Destino',
        help_text='Los distritos a los que se asignarán los mentores'
    )


class AssignVigilantesToTournamentForm(forms.Form):
    """Formulario para asignar vigilantes a un torneo"""
    torneo = forms.ModelChoiceField(
        queryset=Tournament.objects.filter(es_activo=True),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_torneo_vigilantes'
        }),
        label='Torneo'
    )
    
    vigilantes = forms.ModelMultipleChoiceField(
        queryset=Personaje.objects.filter(rol='vigilante', is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        label='Selecciona los Vigilantes a Asignar'
    )
    
    rol_por_defecto = forms.ChoiceField(
        choices=TournamentVigilante._meta.get_field('rol_en_torneo').choices,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Rol por Defecto en el Torneo',
        initial='general'
    )
