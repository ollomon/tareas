from dataclasses import fields
#from django.forms import ModelForm
from django import forms
from .models import Tarea

class FormularioTarea(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['tarea', 'notas', 'estado', 'importante', 'fechafin']
        widgets = {
            'tarea': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escribe el nombre para la tarea' }),
            'notas': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Describe brevemente la tarea'  }),
            'estado': forms.TextInput(attrs={'class':'form-select'}),
            'importante': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'fechafin': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Este campo se cubre de forma automática al finalizar la tarea'  }),
        }