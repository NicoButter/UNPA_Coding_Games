from django import forms
from capitol.models import TributoInfo

class AcreditacionForm(forms.ModelForm):
    class Meta:
        model = TributoInfo
        fields = ['numero_tributo', 'tipo', 'unidad_academica', 'distrito', 'edad', 'habilidades', 'fuerza']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unidad_academica'].required = False 
