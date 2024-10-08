from django.shortcuts import render, get_object_or_404, redirect
from .models import Turistica
from .forms import TuristicaForm

# Vista para gestionar las entradas turísticas
def gestionar_turismo(request):
    turismos = Turistica.objects.all()
    context = {
        'turismos': turismos,
        # 'form': form, # Asegúrate de no incluir el formulario en esta vista.
    }
    return render(request, 'Turisticas/gestionarTurismo.html', context)

def crear_turismo(request):
    if request.method == 'POST':
        form = TuristicaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestionar_turismo')  # Redirige a la vista de la lista
    else:
        form = TuristicaForm()

    return render(request, 'Turisticas/crear_Turismo.html', {'form': form})



# Vista para editar una entrada turística existente
def editar_turismo(request, turCodigo):
    turistica = get_object_or_404(Turistica, pk=turCodigo)
    if request.method == 'POST':
        form = TuristicaForm(request.POST, request.FILES, instance=turistica)
        if form.is_valid():
            form.save()
            return redirect('gestionar_turismo')
    else:
        form = TuristicaForm(instance=turistica)
    return render(request, 'Turisticas/editar_Turismo.html', {'form': form})

# Vista para eliminar una entrada turística
def eliminar_turismo(request, turCodigo):
    turistica = get_object_or_404(Turistica, pk=turCodigo)
    turistica.delete()
    return redirect('gestionar_turismo')

def detalle_turismo(request, titulo, codigo):
    actividad_turistica = get_object_or_404(Turistica, turTitulo_1=titulo, turCodigo=codigo)
    return render(request, 'Turisticas/detalle_Turismo.html', {'actividad_turistica': actividad_turistica})
