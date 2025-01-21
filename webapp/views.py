from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from Nacionalidades.models import Nacionalidad
from Turisticas.models import Turistica
from django.contrib.auth.decorators import login_required
from django.db import connection
from webapp.forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from webapp.models import imagenes
from Nacionalidades.views import (visualizar_tiempo_visualizacion_nacionalidad, visualizar_analisis_2d_nacionalidad,
                                  visualizar_pastel_nacionalidad)
from Turisticas.views import (visualizar_tiempo_visualizacion_turistica, visualizar_analisis_2d_turistica,
                              visualizar_pastel_turistica)

_user = None


def home(request):
    return render(request, 'webapp/index.html')


def quienes_somos(request):
    nacionalidades = Nacionalidad.objects.all()
    return render(request, 'webapp/quienesSomos.html', {'nacionalidades': nacionalidades})


def informe_turisticas(request):
    return render(request, 'informe_turisticas.html')


def mas_informacion(request):
    actividades_turisticas = Turistica.objects.all()
    return render(request, 'webapp/masInformacion.html', {'actividades_turisticas': actividades_turisticas})


def user_login(request):
    global _user
    _user = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data  # obtiene un diccionario con los campos respectivos
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    _user['username'] = cd['username']
                    login(request, user)  # Inicia la sesión del usuario
                    return redirect('paginaActividades')
                else:
                    return render(request, 'webapp/login.html',
                                  {'form': form, 'error_message': 'Cuenta de usuario inactiva.'})
            else:
                return render(request, 'webapp/login.html',
                              {'form': form, 'error_message': 'Usuario o contraseña incorrectos.'})
    else:
        form = LoginForm()

    return render(request, 'webapp/login.html', {'form': form})


def estudiantes(request):
    return render(request, 'webapp/estudiantes.html')

@login_required
def pagina_actividades(request):
    global _user
    # Datos para la sección de nacionalidades
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM nacionalidades_analisis();")
    #     datos_nacionalidades = cursor.fetchone()
    #
    # contexto_nacionalidades = {
    #     'nombre_articulo_nacionalidades': datos_nacionalidades[0],
    #     'mayor_tiempo_visualizacion_nacionalidades': datos_nacionalidades[1],
    #     'dia_visualizacion_nacionalidades': datos_nacionalidades[2],
    #     'categoria_nacionalidades': datos_nacionalidades[3],
    #     'tiempo_visualizacion_nacionalidades_categoria': datos_nacionalidades[4],
    # }
    #
    # # Datos para la sección de turísticas
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT * FROM turistica_analisis();")
    #     datos_turisticas = cursor.fetchone()
    #
    # contexto_turistica = {
    #     'nombre_articulo_turistica': datos_turisticas[0],
    #     'mayor_tiempo_visualizacion_turistica': datos_turisticas[1],
    #     'dia_visualizacion_turistica': datos_turisticas[2],
    #     'categoria_turistica': datos_turisticas[3],
    #     'tiempo_visualizacion_turistica_categoria': datos_turisticas[4],
    # }

    # # Renderizamos la plantilla con ambos contextos
    # return render(request, 'webapp/paginaActividades.html', {
    #     'contexto_nacionalidades': contexto_nacionalidades,
    #     'contexto_turistica': contexto_turistica,
    #     'usuario': _user,
    # })
    return render(request, 'webapp/paginaActividades.html', {'usuario': _user})

@login_required
def documentacion(request):
    return render(request, 'webapp/documentacion.html')

@login_required
def panel_datos(request):
    """
    Vista principal para renderizar el panel de datos.
    """
    # Valores predeterminados de días
    dias_nacionalidad = 7
    dias_turistica = 7

    # Procesar formularios enviados por POST para actualizar datos
    if request.method == 'POST':
        try:
            if 'dias_nacionalidades' in request.POST:
                dias_nacionalidad = int(request.POST.get('dias_nacionalidades', 7))
            if 'dias_turisticas' in request.POST:
                dias_turistica = int(request.POST.get('dias_turisticas', 7))
        except ValueError as ve:
            print(f"[ERROR] Valor inválido en el formulario: {ve}")
            dias_nacionalidad, dias_turistica = 7, 7  # Restaurar valores por defecto en caso de error
        except Exception as e:
            print(f"[ERROR] Error inesperado al procesar el formulario: {e}")
            dias_nacionalidad, dias_turistica = 7, 7  # Restaurar valores por defecto en caso de error

    # Llamar a las funciones de generación de gráficos con manejo de errores
    try:
        visualizar_tiempo_visualizacion_nacionalidad(request)
    except Exception as e:
        print(f"[ERROR] Falló la generación del gráfico 3D Nacionalidades: {e}")

    try:
        visualizar_tiempo_visualizacion_turistica(request)
    except Exception as e:
        print(f"[ERROR] Falló la generación del gráfico 3D Turísticas: {e}")

    try:
        visualizar_analisis_2d_nacionalidad(request)
    except Exception as e:
        print(f"[ERROR] Falló la generación del gráfico 2D Nacionalidades: {e}")

    try:
        visualizar_analisis_2d_turistica(request)
    except Exception as e:
        print(f"[ERROR] Falló la generación del gráfico 2D Turísticas: {e}")

    try:
        visualizar_pastel_nacionalidad(request)
    except Exception as e:
        print(f"[ERROR] Falló la generación del gráfico de pastel Nacionalidades: {e}")

    try:
        visualizar_pastel_turistica(request)
    except Exception as e:
        print(f"[ERROR] Falló la generación del gráfico de pastel Turísticas: {e}")

    # Obtener fechas más recientes de las tablas con manejo de errores
    try:
        fecha_nacionalidad = obtener_fecha_mas_reciente("table_cube_nacionalidad") or '2024-11-23'
    except Exception as e:
        print(f"[ERROR] Falló al obtener la fecha más reciente de Nacionalidades: {e}")
        fecha_nacionalidad = '2024-11-23'

    try:
        fecha_turistica = obtener_fecha_mas_reciente("table_cube_turistica") or '2024-11-23'
    except Exception as e:
        print(f"[ERROR] Falló al obtener la fecha más reciente de Turísticas: {e}")
        fecha_turistica = '2024-11-23'

    # Generar URLs de los gráficos desde la carpeta static
    def generar_html_imagen_static(categoria, nombre_archivo):
        return f"/obtener_imagen/{categoria}/{nombre_archivo}/"

    context = {
        "grafico_3d_nacionalidades": "/obtener_imagen/IMG-1/",
        "grafico_3d_turisticas": "/obtener_imagen/IMG-4/",
        "grafico_2d_nacionalidades": "/obtener_imagen/IMG-2/",
        "grafico_2d_turisticas": "/obtener_imagen/IMG-5/",
        "grafico_pastel_nacionalidades": "/obtener_imagen/IMG-3/",
        "grafico_pastel_turisticas": "/obtener_imagen/IMG-6/",
        "dias_nacionalidad": dias_nacionalidad,
        "dias_turistica": dias_turistica,
        "fecha_nacionalidad": fecha_nacionalidad,
        "fecha_turistica": fecha_turistica,
    }

    # Renderizar el template y pasar el contexto
    return render(request, 'webapp/panel_datos.html', context)


def obtener_fecha_mas_reciente(tabla):
    """
    Obtiene la fecha más reciente de una tabla.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT fecha_visualizacion FROM {tabla} ORDER BY fecha_visualizacion DESC LIMIT 1;")
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener la fecha más reciente de {tabla}: {e}")
        return None


def actualizar_cubo_nacionalidades(dias):
    """
    Actualiza el cubo de nacionalidades con la cantidad de días indicada.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("CALL actualizar_table_cube_nacionalidad(%s);", [dias])
        except Exception as e:
            print(f"Error al actualizar cubo de nacionalidades: {e}")


def actualizar_imagenes(request):
    """
    Endpoint para manejar la actualización dinámica de gráficos según tipo y parámetros.
    """
    tipo = request.GET.get('tipo')  # Tipo del gráfico
    dias = int(request.GET.get('dias', 7))  # Parámetro días
    modo = request.GET.get('modo', None)  # Modo (para gráficos 2D)
    valor = request.GET.get('valor', None)  # Valor (para gráficos 2D)

    # Diccionario para mapear funciones y códigos
    funciones = {
        'grafico_3d_nacionalidades': visualizar_tiempo_visualizacion_nacionalidad,
        'grafico_2d_nacionalidades': visualizar_analisis_2d_nacionalidad,
        'grafico_pastel_nacionalidades': visualizar_pastel_nacionalidad,
        'grafico_3d_turisticas': visualizar_tiempo_visualizacion_turistica,
        'grafico_2d_turisticas': visualizar_analisis_2d_turistica,
        'grafico_pastel_turisticas': visualizar_pastel_turistica,
    }

    img_codigos = {
        'grafico_3d_nacionalidades': 'IMG-1',
        'grafico_2d_nacionalidades': 'IMG-2',
        'grafico_pastel_nacionalidades': 'IMG-3',
        'grafico_3d_turisticas': 'IMG-4',
        'grafico_2d_turisticas': 'IMG-5',
        'grafico_pastel_turisticas': 'IMG-6',
    }

    # Verificar si el tipo es válido
    if tipo not in funciones or tipo not in img_codigos:
        return JsonResponse({'success': False, 'error': 'Tipo de gráfico no válido.'})

    # Obtener el código de imagen asociado
    img_codigo = img_codigos[tipo]

    # Llamar a la función correspondiente
    try:
        # La función debe actualizar la imagen en la base de datos
        funciones[tipo](img_codigo, dias=dias, modo=modo, valor=valor)
        return JsonResponse({'success': True, 'imgCodigo': img_codigo})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def obtener_imagen(request, imgCodigo):
    """
    Devuelve una imagen almacenada en la base de datos basada en su código.
    """
    imagen = get_object_or_404(imagenes, imgCodigo=imgCodigo)
    return HttpResponse(imagen.imgContenido, content_type=imagen.imgTipo)


def actualizar_cubo_turisticas(dias):
    """
    Actualiza el cubo de turísticas con la cantidad de días indicada.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("CALL actualizar_table_cube_turistica(%s);", [dias])
        except Exception as e:
            print(f"Error al actualizar cubo de turísticas: {e}")


def manejador_actualizacion_imagenes(request):
    """
    Manejador para actualizar imágenes de gráficos dinámicamente según el tipo solicitado.

    Parámetros esperados:
    - tipo: Indica el gráfico (ejemplo: 'grafico_3d_nacionalidades', 'grafico_2d_turisticas', etc.)
    - dias: Número de días (para gráficos 3D).
    - modo: Modo del análisis (para gráficos 2D).
    - valor: Valor del análisis (para gráficos 2D).
    """
    tipo = request.GET.get("tipo", None)
    dias = request.GET.get("dias", None)
    modo = request.GET.get("modo", None)
    valor = request.GET.get("valor", None)

    if not tipo:
        return JsonResponse({"error": "El parámetro 'tipo' es obligatorio."}, status=400)

    try:
        # Manejador de gráficos 3D
        if tipo == "grafico_3d_nacionalidades":
            if not dias:
                return JsonResponse({"error": "El parámetro 'dias' es obligatorio para este gráfico."}, status=400)
            visualizar_tiempo_visualizacion_nacionalidad(request)

        elif tipo == "grafico_3d_turisticas":
            if not dias:
                return JsonResponse({"error": "El parámetro 'dias' es obligatorio para este gráfico."}, status=400)
            visualizar_tiempo_visualizacion_turistica(request)

        # Manejador de gráficos 2D
        elif tipo == "grafico_2d_nacionalidades":
            if not modo or not valor:
                return JsonResponse({"error": "Los parámetros 'modo' y 'valor' son obligatorios para este gráfico."},
                                    status=400)
            visualizar_analisis_2d_nacionalidad(request)

        elif tipo == "grafico_2d_turisticas":
            if not modo or not valor:
                return JsonResponse({"error": "Los parámetros 'modo' y 'valor' son obligatorios para este gráfico."},
                                    status=400)
            visualizar_analisis_2d_turistica(request)

        # Manejador de gráficos de pastel
        elif tipo == "grafico_pastel_nacionalidades":
            visualizar_pastel_nacionalidad(request)

        elif tipo == "grafico_pastel_turisticas":
            visualizar_pastel_turistica(request)

        else:
            return JsonResponse({"error": f"El tipo de gráfico '{tipo}' no es válido."}, status=400)

        # Si todo va bien, retornar éxito
        return JsonResponse({"success": f"Imagen del gráfico '{tipo}' actualizada correctamente."})

    except Exception as e:
        return JsonResponse({"error": f"Error al actualizar el gráfico '{tipo}': {str(e)}"}, status=500)


@login_required
def informacion_nacionalidad(request):
    nacionalidades = Nacionalidad.objects.all()
    return render(request, 'Nacionalidades/gestionarNacionalidad.html', {'nacionalidades': nacionalidades})


@login_required
def informacion_turismo(request):
    turismos = Turistica.objects.all()
    return render(request, 'Turisticas/gestionarTurismo.html', {'turismos': turismos})


def logout_view(request):
    logout(request)
    _user = None
    return redirect('login')


# API para obtener las fechas únicas de Nacionalidades
def obtener_fechas_nacionalidades(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT fecha_visualizacion FROM table_cube_nacionalidad ORDER BY fecha_visualizacion DESC;")
            resultados = cursor.fetchall()
        fechas = [{"valor": str(fila[0])} for fila in resultados]
        return JsonResponse({"resultados": fechas})
    except Exception as e:
        return JsonResponse({"error": str(e)})


# API para obtener los nombres únicos de Nacionalidades
def obtener_nombres_nacionalidades(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT nacionalidad_nombre FROM table_cube_nacionalidad ORDER BY nacionalidad_nombre DESC;")
            resultados = cursor.fetchall()
        nombres = [{"valor": fila[0]} for fila in resultados]
        return JsonResponse({"resultados": nombres})
    except Exception as e:
        return JsonResponse({"error": str(e)})


# API para obtener las fechas únicas de Turísticas
def obtener_fechas_turisticas(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DISTINCT fecha_visualizacion FROM table_cube_turistica ORDER BY fecha_visualizacion DESC;")
            resultados = cursor.fetchall()
        fechas = [{"valor": str(fila[0])} for fila in resultados]
        return JsonResponse({"resultados": fechas})
    except Exception as e:
        return JsonResponse({"error": str(e)})


# API para obtener los nombres únicos de Turísticas
def obtener_nombres_turisticas(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT turistica_nombre FROM table_cube_turistica ORDER BY turistica_nombre DESC;")
            resultados = cursor.fetchall()
        nombres = [{"valor": fila[0]} for fila in resultados]
        return JsonResponse({"resultados": nombres})
    except Exception as e:
        return JsonResponse({"error": str(e)})


def obtener_imagen(request, imgCodigo):
    """
    Devuelve una imagen almacenada en la base de datos según su código único (imgCodigo).
    """
    # Obtener la imagen de la base de datos o devolver un error 404 si no existe
    imagen = get_object_or_404(imagenes, imgCodigo=imgCodigo)

    # Crear una respuesta con el contenido de la imagen y establecer el tipo MIME
    response = HttpResponse(imagen.imgContenido, content_type=imagen.imgTipo)

    # Opcional: añadir cabecera para indicar el tamaño de la imagen
    response['Content-Length'] = imagen.imgTamanio

    return response


def procesar_imagen_2d_nacionalidades(request):
    try:
        # Obtener la imagen con el código 'IMG-5'
        imagen = imagenes.objects.get(imgCodigo='IMG-5')

        # Crear la respuesta con el contenido binario de la imagen
        response = HttpResponse(imagen.imgContenido, content_type=imagen.imgTipo)
        response['Content-Disposition'] = f'inline; filename="{imagen.imgNombre}"'

        return response
    except imagenes.DoesNotExist:
        return HttpResponse("La imagen con el código 'IMG-5' no existe.", status=404)


def procesar_imagen_2d_turisticas(request):
    try:
        # Obtener la imagen con el código 'IMG-6' o el correspondiente
        imagen = imagenes.objects.get(imgCodigo='IMG-2')

        # Crear la respuesta con el contenido binario de la imagen
        response = HttpResponse(imagen.imgContenido, content_type=imagen.imgTipo)
        response['Content-Disposition'] = f'inline; filename="{imagen.imgNombre}"'
        return response
    except imagenes.DoesNotExist:
        return HttpResponse("La imagen con el código 'IMG-6' no existe.", status=404)


def procesar_imagen_3d_nacionalidades(request):
    try:
        # Obtener la imagen con el código 'IMG-7'
        imagen = imagenes.objects.get(imgCodigo='IMG-4')

        # Crear la respuesta con el contenido binario de la imagen
        response = HttpResponse(imagen.imgContenido, content_type=imagen.imgTipo)
        response['Content-Disposition'] = f'inline; filename="{imagen.imgNombre}"'

        try:
            visualizar_pastel_nacionalidad(request)
        except Exception as e:
            print(f"[ERROR] Falló la generación del gráfico de pastel Nacionalidades: {e}")

        return response
    except imagenes.DoesNotExist:
        return HttpResponse("La imagen con el código 'IMG-4' no existe.", status=404)


def procesar_imagen_3d_turisticas(request):
    try:
        # Obtener la imagen con el código 'IMG-8'
        imagen = imagenes.objects.get(imgCodigo='IMG-1')

        # Crear la respuesta con el contenido binario de la imagen
        response = HttpResponse(imagen.imgContenido, content_type=imagen.imgTipo)
        response['Content-Disposition'] = f'inline; filename="{imagen.imgNombre}"'

        try:
            visualizar_pastel_turistica(request)
        except Exception as e:
            print(f"[ERROR] Falló la generación del gráfico de pastel Turísticas: {e}")

        return response
    except imagenes.DoesNotExist:
        return HttpResponse("La imagen con el código 'IMG-1' no existe.", status=404)
