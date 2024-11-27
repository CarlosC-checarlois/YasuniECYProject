from django.shortcuts import render, get_object_or_404, redirect
from .forms import TuristicaForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from .models import Turistica, TiempoVisualizacion
from django.http import HttpResponse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.db import connection
from webapp.models import imagenes


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


def obtener_fecha_mas_reciente(tabla):
    """
    Obtiene la fecha más reciente de una tabla.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT fecha_visualizacion FROM {} ORDER BY fecha_visualizacion DESC LIMIT 1;".format(tabla))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener la fecha más reciente de {tabla}: {e}")
        return None


def visualizar_tiempo_visualizacion_turistica(request):
    import matplotlib
    mensaje = ""
    matplotlib.use('Agg')  # Usar backend no interactivo para evitar problemas con GUI

    # Obtener el parámetro 'dias' de la solicitud GET, con valor por defecto 7
    dias = int(request.GET.get('dias', 7))  # Por defecto, 7 días

    # Llamar al procedimiento almacenado para actualizar los datos
    with connection.cursor() as cursor:
        try:
            cursor.execute("CALL actualizar_table_cube_turistica(%s);", [dias])
        except Exception as e:
            print(f"Error al actualizar datos: {str(e)}")

    # Consultar los datos del cubo actualizado
    with connection.cursor() as cursor:
        try:
            cursor.execute("""SELECT * FROM table_cube_turistica;""")
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

        # Si todos los valores son 0, mostrar un mensaje en lugar del gráfico
        if np.all(dz == 0):
            ax.text2D(0.5, 0.5, "Todos los valores son 0. No hay datos para mostrar.",
                      transform=ax.transAxes, ha='center', va='center', fontsize=14)
        else:
            # Normalización de colores
            norm = plt.Normalize(dz.min(), dz.max())
            colors = cm.viridis(norm(dz))

            ax.bar3d(xpos, ypos, zpos, 0.5, 0.5, dz, color=colors, alpha=0.7)

            # Configuración de los ejes
            ax.set_xlabel('Fecha de Visualización')
            ax.set_ylabel('Turística')
            ax.set_zlabel('Tiempo Total Visualizado (segundos)')

            # Etiquetas personalizadas para los ejes X y Y
            ax.set_xticks(np.arange(len(fechas_unicas)))
            ax.set_xticklabels(fechas_unicas, rotation=45, ha='right')
            ax.set_yticks(np.arange(len(turisticas_unicas)))
            ax.set_yticklabels(turisticas_unicas, rotation=45, ha='right')

            # Ajustar el ángulo de la cámara
            ax.view_init(elev=30, azim=120)

            # Barra de colores
            mappable = cm.ScalarMappable(cmap='viridis', norm=norm)
            mappable.set_array(dz)
            fig.colorbar(mappable, shrink=0.6, aspect=5)
    else:
        # Mostrar mensaje si no hay datos
        ax.text2D(0.5, 0.5, "No hay datos para mostrar.", transform=ax.transAxes, ha='center', va='center', fontsize=14)
        # Guardar el gráfico en memoria como binario
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    # Intentar actualizar la imagen en la base de datos
    try:
        imagen = imagenes.objects.get(imgCodigo='IMG-1')  # Identificar la imagen por su código único
        imagen.imgContenido = buffer.read()
        imagen.imgTamanio = buffer.getbuffer().nbytes
        imagen.save()
        mensaje = "Imagen actualizada correctamente."
    except imagenes.DoesNotExist:
        # Crear la imagen si no existe
        imagenes.objects.create(
            imgCodigo='IMG-1',
            imgNombre='Gráfico 3D Turísticas',
            imgTipo='image/png',
            imgTamanio=buffer.getbuffer().nbytes,
            imgContenido=buffer.read()
        )
        mensaje = "Imagen creada correctamente."

    return HttpResponse(mensaje)


def visualizar_analisis_2d_turistica(request):
    import matplotlib
    mensaje = ""
    matplotlib.use('Agg')  # Usar backend no interactivo

    # Obtener el modo y valor desde los parámetros GET
    modo = int(request.GET.get('modo', 1))  # Predeterminado: modo 1
    valor = request.GET.get('valor', None)

    # Si no se pasa valor, obtener la fecha más reciente
    if not valor:
        valor = obtener_fecha_mas_reciente("table_cube_turistica")
        if not valor:
            return HttpResponse("No hay datos disponibles para generar el gráfico.")

    # Consultar los datos para la visualización bidimensional
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "SELECT * FROM visualizacion_bidimensional_dinamica_turistica(%s, %s);",
                [modo, valor]
            )
            resultados = cursor.fetchall()
        except Exception as e:
            print(f"Error al cargar datos de análisis 2D de turísticas: {str(e)}")
            return HttpResponse("Error al cargar datos para el gráfico bidimensional.")

    # Preparar datos para el gráfico
    if resultados:
        eje_x = [fila[0] for fila in resultados]
        eje_y = [fila[1] for fila in resultados]
    else:
        eje_x, eje_y = [], []

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    if eje_x and eje_y:
        ax.bar(eje_x, eje_y, color='orange')
        ax.set_xlabel("Turística")
        ax.set_ylabel("Tiempo Total Visualizado (segundos)")
        ax.set_title("Análisis Bidimensional - Turísticas")
        plt.xticks(rotation=45, ha='right')
    else:
        ax.text(0.5, 0.5, "No hay datos disponibles", transform=ax.transAxes, ha="center", va="center")
        ax.set_axis_off()

    # Guardar el gráfico en memoria como binario
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    # Guardar o actualizar la imagen en la base de datos
    try:
        imagen = imagenes.objects.get(imgCodigo='IMG-2')  # Buscar por el código único
        imagen.imgContenido = buffer.read()
        imagen.imgTamanio = buffer.getbuffer().nbytes
        imagen.save()
        mensaje = "Imagen actualizada correctamente."
    except imagenes.DoesNotExist:
        # Crear la imagen si no existe
        imagenes.objects.create(
            imgCodigo='IMG-2',
            imgNombre='Gráfico 2D Turísticas',
            imgTipo='image/png',
            imgTamanio=buffer.getbuffer().nbytes,
            imgContenido=buffer.read()
        )
        mensaje = "Imagen creada correctamente."

    return HttpResponse(mensaje)


def visualizar_pastel_turistica(request):
    """
    Generar el gráfico de pastel para turísticas.
    """
    # Llamar al procedimiento para actualizar la vista de pastel
    mensaje = ""
    with connection.cursor() as cursor:
        try:
            cursor.execute("CALL vista_pastel_turistica();")
        except Exception as e:
            return HttpResponse(f"Error al actualizar vista de pastel de turísticas: {str(e)}")

    # Consultar los datos de la vista de pastel
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM view_pastel_turistica;")
            resultados = cursor.fetchall()
        except Exception as e:
            return HttpResponse(f"Error al obtener datos de la vista de pastel de turísticas: {str(e)}")

    if not resultados:
        return HttpResponse("No hay datos para generar el gráfico de pastel de turísticas.")

    # Separar los datos
    labels = [fila[0] for fila in resultados]
    sizes = [fila[1] for fila in resultados]

    # Crear el gráfico de pastel
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Para un círculo perfecto

    # Guardar el gráfico en memoria como binario
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    # Guardar o actualizar la imagen en la base de datos
    try:
        imagen = imagenes.objects.get(imgCodigo='IMG-3')  # Buscar por el código único
        imagen.imgContenido = buffer.read()
        imagen.imgTamanio = buffer.getbuffer().nbytes
        imagen.save()
        mensaje = "Imagen actualizada correctamente."
    except imagenes.DoesNotExist:
        # Crear la imagen si no existe
        imagenes.objects.create(
            imgCodigo='IMG-3',
            imgNombre='Gráfico de Pastel Turísticas',
            imgTipo='image/png',
            imgTamanio=buffer.getbuffer().nbytes,
            imgContenido=buffer.read()
        )
        mensaje = "Imagen creada correctamente."

    return HttpResponse(mensaje)
