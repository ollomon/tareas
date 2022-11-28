"""tareas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apptareas import views
from apptareas.views import page_not_found_404
handler404 = page_not_found_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('tareas/', views.tareas, name='tareas'),
    path('tareas_todas/', views.tareas_todas, name='tareas_todas'),
    path('tareas_fin/', views.tareas_finalizadas, name='tareas_fin'),
    path('tareas/crear/', views.crearTarea, name='crear_tarea'),
    path('tareas/buscar/', views.buscar_tarea, name='buscar_tarea'),
    path('tareas/<int:tarea_id>/', views.detalleTarea, name='detalle_tarea'),
    path('tareas/<int:tarea_id>/activar', views.activarTarea, name='activar_tarea'),
    path('tareas/<int:tarea_id>/finalizar', views.finalizarTarea, name='finalizar_tarea'),
    path('tareas/<int:tarea_id>/eliminar', views.eliminarTarea, name='eliminar_tarea'),
    path('logout/', views.cerrarSesion, name='logout'),
    path('login/', views.iniciarSesion, name='login'),
]
