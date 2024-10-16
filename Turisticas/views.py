from django.shortcuts import render, get_object_or_404, redirect
from .forms import TuristicaForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from .models import Turistica, TiempoVisualizacion
from django.http import HttpResponse
from django.db import connection
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from io import BytesIO
from django.contrib.auth.decorators import login_required

# Vista para gestionar las entradas turísticas
@login_required
def gestionar_turismo(request):
    turismos = Turistica.objects.all()
    context = {
        'turismos': turismos,
        # 'form': form, # Asegúrate de no incluir el formulario en esta vista.
    }
    return render(request, 'Turisticas/gestionarTurismo.html', context)

@login_required
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
@login_required
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
@login_required
def eliminar_turismo(request, turCodigo):
    turistica = get_object_or_404(Turistica, pk=turCodigo)
    turistica.delete()
    return redirect('gestionar_turismo')


def detalle_turismo(request, titulo, codigo):
    actividad_turistica = get_object_or_404(Turistica, turTitulo_1=titulo, turCodigo=codigo)
    return render(request, 'Turisticas/detalle_Turismo.html', {'actividad_turistica': actividad_turistica})

@login_required
@csrf_exempt
def guardar_tiempo_visualizacion_turistica(request, turCodigo):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tiempo_visualizado = data.get('tiempo')

            # Buscar la turistica utilizando el código
            turistica = Turistica.objects.get(turCodigo=turCodigo)

            # Crear el registro de tiempo de visualización en la base de datos
            TiempoVisualizacion.objects.create(
                turistica=turistica,
                tiempo_visualizado=tiempo_visualizado,
                fecha_visualizacion=timezone.now()
            )

            return JsonResponse({'status': 'ok'})
        except Turistica.DoesNotExist:
            return JsonResponse({'error': 'Turística no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def visualizar_tiempo_visualizacion_turistica(request):
    with connection.cursor() as cursor:
        try:
            # Ejecutar la consulta SQL
            cursor.execute("""SELECT * FROM turistica_cube();""")

            # Obtener los resultados
            resultados = cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener resultados: {str(e)}")
            resultados = []

    # Separar los datos en listas
    if resultados:
        turisticas_unicas = list(set(fila[0] for fila in resultados))  # Nombres únicos de las turísticas
        fechas_unicas = list(set(fila[1] for fila in resultados))  # Fechas únicas
        fechas_unicas.sort()  # Ordenar fechas
        tiempos = []

        # Crear una matriz para los tiempos
        for turistica in turisticas_unicas:
            tiempo_por_turistica = []
            for fecha in fechas_unicas:
                # Buscar el tiempo de esa turística en esa fecha
                tiempo = next((fila[2] for fila in resultados if fila[0] == turistica and fila[1] == fecha), 0)
                tiempo_por_turistica.append(tiempo)
            tiempos.append(tiempo_por_turistica)

    else:
        turisticas_unicas, fechas_unicas, tiempos = [], [], []

    # Crear el gráfico 3D con Matplotlib
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    if fechas_unicas and turisticas_unicas and tiempos:
        fechas_num = np.arange(len(fechas_unicas))
        xpos, ypos = np.meshgrid(fechas_num, np.arange(len(turisticas_unicas)))
        xpos = xpos.flatten()
        ypos = ypos.flatten()
        zpos = np.zeros_like(xpos)
        dz = np.array(tiempos).flatten()
        norm = plt.Normalize(dz.min(), dz.max())
        colors = cm.viridis(norm(dz))
        ax.bar3d(xpos, ypos, zpos, 0.5, 0.5, dz, color=colors, alpha=0.7)

        # Configurar los ejes
        ax.set_xlabel('Fecha de Visualización')
        ax.set_ylabel('Turística')
        ax.set_zlabel('Tiempo Total Visualizado (segundos)')

        # Etiquetas personalizadas para los ejes X y Y
        ax.set_xticks(np.arange(len(fechas_unicas)))
        ax.set_xticklabels(fechas_unicas, rotation=45, ha='right')
        ax.set_yticks(np.arange(len(turisticas_unicas)))
        ax.set_yticklabels(turisticas_unicas)

        # Ajustar el ángulo de la cámara para obtener la perspectiva adecuada
        ax.view_init(elev=30, azim=120)

        # Agregar una barra de colores para la escala de los valores
        mappable = cm.ScalarMappable(cmap='viridis', norm=norm)
        mappable.set_array(dz)
        fig.colorbar(mappable, shrink=0.6, aspect=5)

    else:
        # Mostrar mensaje si no hay datos
        ax.text2D(0.5, 0.5, "No hay datos para mostrar", transform=ax.transAxes)

    # Guardar el gráfico en un buffer para devolverlo como imagen
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')
