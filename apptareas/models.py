from email.policy import default
from random import choices
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tarea(models.Model):
    fecha = models.DateField(auto_now_add=True, editable=True)
    hora = models.TimeField(auto_now_add=True, editable=True)
    tarea = models.CharField(max_length=200)
    notas = models.TextField(blank=True)
    estados = (
        ('Pendiente','Pendiente',), 
        ('Finalizado','Finalizado')
    )
    estado = models.CharField(max_length=10, choices=estados, default='Pendiente')
    fechafin = models.DateTimeField(null=True, blank=True, verbose_name="Fecha Finalización") 
    importante = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return "{} . . . . {} . . . . {} . . . . {} ".format(self.tarea, '<< Importante >>' if self.importante else '', '   '.join(self.estado), self.fechafin if self.estado =='Finalizado' else '')
