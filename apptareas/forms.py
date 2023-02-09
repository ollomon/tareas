from dataclasses import fields
#from django.forms import ModelForm
from django import forms
from .models import Tarea
from datetime import datetime

class FormularioTarea(forms.ModelForm):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Finalizado', 'Finalizado'),
    ]
    estado = forms.ChoiceField(choices=ESTADO_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Tarea
        fields = ['tarea', 'notas', 'estado', 'importante', 'fechafin']
        widgets = {
            'tarea': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escribe el nombre para la tarea' }),
            'notas': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Describe brevemente la tarea'  }),
            'importante': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'fechafin': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Este campo se cubre de forma automática al finalizar la tarea'  }),
        }
        
    # El método clean se llama de forma automática cuando se valida el formulario en Django
    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')

        if estado == 'Finalizado':
            cleaned_data['fechafin'] = datetime.now()
        else:
            cleaned_data['fechafin'] = None
        
        return cleaned_data