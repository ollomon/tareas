from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import FormularioTarea
from .models import Tarea
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def inicio(request):
    return render(request, 'inicio.html')

def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registrar usuario
            try:
                usuario = User.objects.create_user(username=request.POST['username'],
                                                   password=request.POST['password1'])
                usuario.save()  # guarda en la base de datos
                login(request, usuario)
                return redirect('tareas')
            except IntegrityError:
                return render(request, 'registro.html', {
                    'form': UserCreationForm,
                    'error': "Usuario ya existe"
                })
        else:
            return render(request, 'registro.html', {
                'form': UserCreationForm,
                'error': "Password no coincide"
            })

@login_required
def tareas(request):
    tareas_lista = Tarea.objects.filter(
        usuario=request.user, estado='Pendiente').order_by('fecha', "hora").reverse()
    paginator = Paginator(tareas_lista, 9)
    pagina = request.GET.get('page')
    tareas = paginator.get_page(pagina)
    return render(request, 'tareas.html', {
        'tareas': tareas,
        'titulo_pagina': 'Tareas Pendientes'
    })

@login_required
def tareas_todas(request):
    tareas_lista = Tarea.objects.filter(
        usuario=request.user).order_by('fecha', "hora").reverse()
    paginator = Paginator(tareas_lista, 9)
    pagina = request.GET.get('page')
    tareas = paginator.get_page(pagina)
    return render(request, 'tareas.html', {
        'tareas': tareas,
        'titulo_pagina': 'Todas las Tareas'
    })

@login_required
def tareas_finalizadas(request):
    tareas_lista = Tarea.objects.filter(
        usuario=request.user, estado='Finalizado').order_by('fecha', "hora").reverse()
    paginator = Paginator(tareas_lista, 9)
    pagina = request.GET.get('page')
    tareas = paginator.get_page(pagina)
    return render(request, 'tareas.html', {
        'tareas': tareas,
        'titulo_pagina': 'Tareas Finalizadas'
    })

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('inicio')


def iniciarSesion(request):
    if request.method == 'GET':
        return render(request, 'iniciarsesion.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'iniciarsesion.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o Contraseña No Válidos'
            })
        else:
            login(request, user)
            return redirect('inicio')

@login_required
def crearTarea(request):
    if request.method == 'GET':
        return render(request, 'crear_tarea.html', {'formulario': FormularioTarea})
    else:
        try:
            form = FormularioTarea(request.POST)
            # para que no lo guarde antes de asignar el usuario
            nueva_tarea = form.save(commit=False)
            nueva_tarea.usuario = request.user  # asignamos el usuario
            nueva_tarea.save()  # guardamos en la base de datos
            return redirect('tareas')
        except Exception as e:
            return render(request, 'crear_tarea.html', {
                'formulario': FormularioTarea,
                'error': 'Se ha producido un Error, por favor, introduzca datos válidos,  Error: ({})'.format(e)
            })

@login_required
def detalleTarea(request, tarea_id):
    if request.method == 'GET':
        tarea = get_object_or_404(Tarea, pk=tarea_id, usuario=request.user)
        formulario = FormularioTarea(instance=tarea)
        return render(request, 'detalle_tarea.html', {
            'tarea': tarea,
            'formulario': formulario
        })
    else:
        try:
            tarea = get_object_or_404(Tarea, pk=tarea_id, usuario=request.user)  # pk es primarky Key
            formulario = FormularioTarea(request.POST, instance=tarea)
            formulario.save()
            return redirect('tareas')
        except Exception as e:
             return render(request, 'detalle_tarea.html', {
            'tarea': tarea,
            'formulario': formulario,
            'error': 'Se ha producido un Error actualizando la tarea, Error: ({})'.format(e)
        })

@login_required
def finalizarTarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.estado = 'Finalizado'
        tarea.fechafin = timezone.now()
        tarea.save()
        return redirect('tareas')

@login_required
def activarTarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.estado = 'Pendiente'
        tarea.fechafin = None
        tarea.save()
        return redirect('tareas')

@login_required
def eliminarTarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tareas')

def page_not_found_404(request, exception):
    return render(request, '404.html')

@login_required
def buscar_tarea(request):
    if request.method == 'GET':
        buscar = request.GET.get('tbuscar')
        print("buscar:", buscar)
        tareas_lista = Tarea.objects.filter(
            usuario=request.user, tarea__icontains=buscar).order_by('fecha', "hora").reverse()
        paginator = Paginator(tareas_lista, 9)
        pagina = request.GET.get('page')
        tareas = paginator.get_page(pagina)
        return render(request, 'tareas.html', {
            'tareas': tareas,
            'titulo_pagina': 'Resultado Buscar Tarea'
        })