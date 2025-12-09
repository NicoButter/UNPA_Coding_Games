from django import forms
from capitol.models import TributoInfo

class AcreditacionForm(forms.ModelForm):
    class Meta:
        model = TributoInfo
        fields = ['numero_tributo', 'tipo', 'unidad_academica', 'carrera', 'distrito', 'nivel', 'estado']
        widgets = {
            'numero_tributo': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'unidad_academica': forms.TextInput(attrs={'class': 'form-control'}),
            'carrera': forms.TextInput(attrs={'class': 'form-control'}),
            'distrito': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 13}),
            'nivel': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unidad_academica'].required = False
        self.fields['carrera'].required = False
 
