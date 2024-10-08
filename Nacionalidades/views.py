from django.shortcuts import render, get_object_or_404, redirect
from .models import Nacionalidad
from .forms import NacionalidadForm

def editar_nacionalidad(request, nacCodigo):
    nacionalidad = get_object_or_404(Nacionalidad, nacCodigo=nacCodigo)
    if request.method == 'POST':
        form = NacionalidadForm(request.POST, instance=nacionalidad)
        if form.is_valid():
            form.save()
            return redirect('paginaActividades')
    else:
        form = NacionalidadForm(instance=nacionalidad)
    return render(request, 'Nacionalidades/editar_nacionalidad.html', {'form': form})

def eliminar_nacionalidad(request, nacCodigo):
    nacionalidad = get_object_or_404(Nacionalidad, nacCodigo=nacCodigo)
    nacionalidad.delete()
    return redirect('paginaActividades')

def gestionar_nacionalidades(request):
    nacionalidades = Nacionalidad.objects.all()
    form = NacionalidadForm()  # Si estás usando un formulario para añadir/editar
    return render(request, 'Nacionalidades/gestionarNacionalidad.html', {
        'nacionalidades': nacionalidades,
        'form': form
    })
def informacion_nacionalidad(request):
    nacionalidades = Nacionalidad.objects.all()
    return render(request, 'Nacionalidades/gestionarNacionalidad.html', {
        'nacionalidades': nacionalidades
    })

def crear_nacionalidad(request):
    if request.method == 'POST':
        form = NacionalidadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('informacion_nacionalidad')
    else:
        form = NacionalidadForm()
    return render(request, 'Nacionalidades/crear-nacionalidad.html', {'form': form})

def detalle_nacionalidad(request, titulo, codigo):
    # Buscar la nacionalidad con el título y código proporcionados
    nacionalidad = get_object_or_404(Nacionalidad, nacTitulo_1=titulo, nacCodigo=codigo)

    # Renderizar la plantilla con los datos de la nacionalidad
    return render(request, 'Nacionalidades/detalle_nacionalidad.html', {
        'nacionalidad': nacionalidad
    })