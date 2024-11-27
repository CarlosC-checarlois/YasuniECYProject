import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from django.db import connection
from io import BytesIO
import json
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NacionalidadForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import Nacionalidad, TiempoVisualizacion
from django.contrib.auth.decorators import login_required
from webapp.models import imagenes



@login_required
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


@login_required
def eliminar_nacionalidad(request, nacCodigo):
    nacionalidad = get_object_or_404(Nacionalidad, nacCodigo=nacCodigo)
    nacionalidad.delete()
    return redirect('paginaActividades')


@login_required
def gestionar_nacionalidades(request):
    nacionalidades = Nacionalidad.objects.all()
    form = NacionalidadForm()  # Si estás usando un formulario para añadir/editar
    return render(request, 'Nacionalidades/gestionarNacionalidad.html', {
        'nacionalidades': nacionalidades,
        'form': form
    })


@login_required
def informacion_nacionalidad(request):
    nacionalidades = Nacionalidad.objects.all()
    return render(request, 'Nacionalidades/gestionarNacionalidad.html', {
        'nacionalidades': nacionalidades
    })


@login_required
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


def visualizar_tiempo_visualizacion_nacionalidad(request):
    import matplotlib
    matplotlib.use('Agg')  # Usar backend no interactivo para evitar problemas con GUI

    # Obtener el parámetro 'dias' de la solicitud GET, con valor por defecto 7
    try:
        dias = int(request.GET.get('dias', 7))  # Por defecto, 7 días
        print(f"[INFO] Número de días solicitado: {dias}")
    except ValueError:
        dias = 7
        print("[ERROR] Parámetro 'dias' no válido, usando valor por defecto: 7")

    # Llamar al procedimiento almacenado para actualizar los datos
    with connection.cursor() as cursor:
        try:
            cursor.execute("CALL actualizar_table_cube_nacionalidad(%s);", [dias])
            print(f"[INFO] Procedimiento 'actualizar_table_cube_nacionalidad({dias})' ejecutado correctamente.")
        except Exception as e:
            print(f"[ERROR] Error al ejecutar procedimiento almacenado: {str(e)}")
            return HttpResponse(f"Error al actualizar datos: {str(e)}", status=500)

    # Consultar los datos del cubo actualizado
    with connection.cursor() as cursor:
        try:
            cursor.execute("""SELECT * FROM table_cube_nacionalidad;""")
            resultados = cursor.fetchall()
            print(f"[INFO] Datos obtenidos de 'table_cube_nacionalidad': {resultados}")
        except Exception as e:
            print(f"[ERROR] Error al consultar datos de 'table_cube_nacionalidad': {str(e)}")
            return HttpResponse(f"Error al obtener datos: {str(e)}", status=500)

    # Separar los datos en listas
    if resultados:
        try:
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

            print(f"[INFO] Nacionalidades únicas: {nacionalidades_unicas}")
            print(f"[INFO] Fechas únicas: {fechas_unicas}")
            print(f"[INFO] Matriz de tiempos: {tiempos}")
        except Exception as e:
            print(f"[ERROR] Error al procesar datos: {str(e)}")
            return HttpResponse(f"Error al procesar datos: {str(e)}", status=500)
    else:
        nacionalidades_unicas, fechas_unicas, tiempos = [], [], []
        print("[WARNING] No se encontraron datos en 'table_cube_nacionalidad'.")

    # Crear el gráfico 3D con Matplotlib
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    if fechas_unicas and nacionalidades_unicas and tiempos:
        try:
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
        except Exception as e:
            print(f"[ERROR] Error al generar el gráfico 3D: {str(e)}")
            return HttpResponse(f"Error al generar gráfico: {str(e)}", status=500)
    else:
        # Mostrar mensaje si no hay datos
        ax.text2D(0.5, 0.5, "No hay datos para mostrar", transform=ax.transAxes)
        print("[WARNING] No se encontraron datos para generar el gráfico.")
    # Guardar el gráfico en memoria como binario
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    # Guardar o actualizar la imagen en la base de datos
    try:
        imagen = imagenes.objects.get(imgCodigo='IMG-4')  # Buscar por el código único
        imagen.imgContenido = buffer.read()
        imagen.imgTamanio = buffer.getbuffer().nbytes
        imagen.save()
        mensaje = "Imagen actualizada correctamente."
    except imagenes.DoesNotExist:
        # Crear la imagen si no existe
        imagenes.objects.create(
            imgCodigo='IMG-4',
            imgNombre='Gráfico 3D Nacionalidades',
            imgTipo='image/png',
            imgTamanio=buffer.getbuffer().nbytes,
            imgContenido=buffer.read()
        )
        mensaje = "Imagen creada correctamente."

    return HttpResponse(mensaje)


def visualizar_analisis_2d_nacionalidad(request):
    import matplotlib
    matplotlib.use('Agg')  # Usar backend no interactivo

    # Obtener el modo y valor desde los parámetros GET
    modo = int(request.GET.get('modo', 1))  # Predeterminado: modo 1
    valor = request.GET.get('valor', None)

    # Si no se pasa valor, obtener la fecha más reciente
    if not valor:
        valor = obtener_fecha_mas_reciente("table_cube_nacionalidad")
        if not valor:
            return HttpResponse("No hay datos disponibles para generar el gráfico.")

    # Consultar los datos para la visualización bidimensional
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                "SELECT * FROM visualizacion_bidimensional_dinamica_nacionalidad(%s, %s);",
                [modo, valor]
            )
            resultados = cursor.fetchall()
        except Exception as e:
            print(f"Error al cargar datos de análisis 2D de nacionalidades: {str(e)}")
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
        ax.bar(eje_x, eje_y, color='skyblue')
        ax.set_xlabel("Nacionalidad")
        ax.set_ylabel("Tiempo Total Visualizado (segundos)")
        ax.set_title("Análisis Bidimensional - Nacionalidades")
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
        imagen = imagenes.objects.get(imgCodigo='IMG-5')  # Buscar por el código único
        imagen.imgContenido = buffer.read()
        imagen.imgTamanio = buffer.getbuffer().nbytes
        imagen.save()
        mensaje = "Imagen actualizada correctamente."
    except imagenes.DoesNotExist:
        # Crear la imagen si no existe
        imagenes.objects.create(
            imgCodigo='IMG-5',
            imgNombre='Gráfico 2D Nacionalidades',
            imgTipo='image/png',
            imgTamanio=buffer.getbuffer().nbytes,
            imgContenido=buffer.read()
        )
        mensaje = "Imagen creada correctamente."

    return HttpResponse(mensaje)


def visualizar_pastel_nacionalidad(request):
    """
    Generar el gráfico de pastel para nacionalidades.
    """
    # Llamar al procedimiento para actualizar la vista de pastel
    with connection.cursor() as cursor:
        try:
            cursor.execute("CALL vista_pastel_nacionalidad();")
        except Exception as e:
            return HttpResponse(f"Error al actualizar vista de pastel de nacionalidades: {str(e)}")

    # Consultar los datos de la vista de pastel
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM view_pastel_nacionalidad;")
            resultados = cursor.fetchall()
        except Exception as e:
            return HttpResponse(f"Error al obtener datos de la vista de pastel de nacionalidades: {str(e)}")

    if not resultados:
        return HttpResponse("No hay datos para generar el gráfico de pastel de nacionalidades.")

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
        imagen = imagenes.objects.get(imgCodigo='IMG-6')  # Buscar por el código único
        imagen.imgContenido = buffer.read()
        imagen.imgTamanio = buffer.getbuffer().nbytes
        imagen.save()
        mensaje = "Imagen de pastel actualizada correctamente."
    except imagenes.DoesNotExist:
        # Crear la imagen si no existe
        imagenes.objects.create(
            imgCodigo='IMG-6',
            imgNombre='Gráfico de Pastel Nacionalidades',
            imgTipo='image/png',
            imgTamanio=buffer.getbuffer().nbytes,
            imgContenido=buffer.read()
        )
        mensaje = "Imagen de pastel creada correctamente."

    return HttpResponse(mensaje)