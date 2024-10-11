from django.shortcuts import render, get_object_or_404, redirect
from .forms import NacionalidadForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .models import Nacionalidad, TiempoVisualizacion
import json
from django.db import connection
from django.http import HttpResponse
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

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

@csrf_exempt
def guardar_tiempo_visualizacion_nacionalidad(request, nacCodigo):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tiempo_visualizado = data.get('tiempo')

            # Buscar la nacionalidad utilizando el código
            nacionalidad = Nacionalidad.objects.get(nacCodigo=nacCodigo)

            # Crear el registro de tiempo de visualización en la base de datos
            TiempoVisualizacion.objects.create(
                nacionalidad=nacionalidad,
                tiempo_visualizado=tiempo_visualizado,
                fecha_visualizacion=timezone.now()
            )

            return JsonResponse({'status': 'ok'})
        except Nacionalidad.DoesNotExist:
            return JsonResponse({'error': 'Nacionalidad no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def visualizar_tiempo_visualizacion_nacionalidad(request):
    with connection.cursor() as cursor:
        try:
            # Ejecutar la consulta SQL
            cursor.execute("""SELECT * FROM nacionalidades_cube();""")

            # Obtener los resultados
            resultados = cursor.fetchall()

        except Exception as e:
            print(f"Error al obtener resultados: {str(e)}")
            resultados = []

    # Separar los datos en listas
    if resultados:
        nacionalidades_unicas = list(set(fila[0] for fila in resultados))  # Nombres únicos de las nacionalidades
        fechas_unicas = list(set(fila[1] for fila in resultados))  # Fechas únicas
        fechas_unicas.sort()  # Ordenar fechas
        tiempos = []

        # Crear una matriz para los tiempos
        for nacionalidad in nacionalidades_unicas:
            tiempo_por_nacionalidad = []
            for fecha in fechas_unicas:
                # Buscar el tiempo de esa nacionalidad en esa fecha
                tiempo = next((fila[2] for fila in resultados if fila[0] == nacionalidad and fila[1] == fecha), 0)
                tiempo_por_nacionalidad.append(tiempo)
            tiempos.append(tiempo_por_nacionalidad)

    else:
        nacionalidades_unicas, fechas_unicas, tiempos = [], [], []

    # Crear el gráfico 3D con Matplotlib
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    if fechas_unicas and nacionalidades_unicas and tiempos:
        fechas_num = np.arange(len(fechas_unicas))
        xpos, ypos = np.meshgrid(fechas_num, np.arange(len(nacionalidades_unicas)))
        xpos = xpos.flatten()
        ypos = ypos.flatten()
        zpos = np.zeros_like(xpos)
        dz = np.array(tiempos).flatten()
        norm = plt.Normalize(dz.min(), dz.max())
        colors = cm.viridis(norm(dz))
        ax.bar3d(xpos, ypos, zpos, 0.5, 0.5, dz, color=colors, alpha=0.7)

        # Configurar los ejes
        ax.set_xlabel('Fecha de Visualización')
        ax.set_ylabel('Nacionalidad')
        ax.set_zlabel('Tiempo Total Visualizado (segundos)')

        # Etiquetas personalizadas para los ejes X y Y
        ax.set_xticks(np.arange(len(fechas_unicas)))
        ax.set_xticklabels(fechas_unicas, rotation=45, ha='right')
        ax.set_yticks(np.arange(len(nacionalidades_unicas)))
        ax.set_yticklabels(nacionalidades_unicas)

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

