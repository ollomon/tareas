from django.contrib import admin
from .models import Tarea

class TareasAdmin(admin.ModelAdmin):
    readonly_fields = ("fecha", "hora")
    
# Register your models here.
admin.site.register(Tarea, TareasAdmin)