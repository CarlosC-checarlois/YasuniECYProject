from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from Nacionalidades.models import Nacionalidad
from Turisticas.models import Turistica
from webapp.forms import LoginForm
from webapp.models import UsuariosYasuni
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render, redirect
from django.db import connection
from webapp.forms import LoginForm  # Asegúrate de tener este formulario definido correctamente
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
import os
from django.conf import settings
from Nacionalidades.views import (
    visualizar_tiempo_visualizacion_nacionalidad,
    visualizar_analisis_2d_nacionalidad,
    visualizar_pastel_nacionalidad
)
from Turisticas.views import (
    visualizar_tiempo_visualizacion_turistica,
    visualizar_analisis_2d_turistica,
    visualizar_pastel_turistica
)
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


@login_required
def pagina_actividades(request):
    global _user
    # Datos para la sección de nacionalidades
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM nacionalidades_analisis();")
        datos_nacionalidades = cursor.fetchone()

    contexto_nacionalidades = {
        'nombre_articulo_nacionalidades': datos_nacionalidades[0],
        'mayor_tiempo_visualizacion_nacionalidades': datos_nacionalidades[1],
        'dia_visualizacion_nacionalidades': datos_nacionalidades[2],
        'categoria_nacionalidades': datos_nacionalidades[3],
        'tiempo_visualizacion_nacionalidades_categoria': datos_nacionalidades[4],
    }

    # Datos para la sección de turísticas
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM turistica_analisis();")
        datos_turisticas = cursor.fetchone()

    contexto_turistica = {
        'nombre_articulo_turistica': datos_turisticas[0],
        'mayor_tiempo_visualizacion_turistica': datos_turisticas[1],
        'dia_visualizacion_turistica': datos_turisticas[2],
        'categoria_turistica': datos_turisticas[3],
        'tiempo_visualizacion_turistica_categoria': datos_turisticas[4],
    }

    # Renderizamos la plantilla con ambos contextos
    return render(request, 'webapp/paginaActividades.html', {
        'contexto_nacionalidades': contexto_nacionalidades,
        'contexto_turistica': contexto_turistica,
        'usuario': _user,
    })


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


def actualizar_cubo_turisticas(dias):
    """
    Actualiza el cubo de turísticas con la cantidad de días indicada.
    """
    with connection.cursor() as cursor:
        try:
            cursor.execute("CALL actualizar_table_cube_turistica(%s);", [dias])
        except Exception as e:
            print(f"Error al actualizar cubo de turísticas: {e}")


def generar_html_imagen_static(folder, filename):
    """
    Genera la URL para acceder a una imagen en la carpeta static.
    """
    # Usar os.path.join para construir la ruta a partir de STATIC_URL
    return os.path.join(settings.STATIC_URL, folder, 'images', filename)


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
            elif 'dias_turisticas' in request.POST:
                dias_turistica = int(request.POST.get('dias_turisticas', 7))
        except ValueError as ve:
            print(f"Error al procesar el formulario: {ve}")
        except Exception as e:
            print(f"Error inesperado al procesar el formulario: {e}")

    # Llamar a las funciones de generación de gráficos
    visualizar_tiempo_visualizacion_nacionalidad(request)
    visualizar_tiempo_visualizacion_turistica(request)
    visualizar_analisis_2d_nacionalidad(request)
    visualizar_analisis_2d_turistica(request)
    visualizar_pastel_nacionalidad(request)
    visualizar_pastel_turistica(request)

    # Obtener fechas más recientes de las tablas
    fecha_nacionalidad = obtener_fecha_mas_reciente("table_cube_nacionalidad") or '2024-11-23'
    fecha_turistica = obtener_fecha_mas_reciente("table_cube_turistica") or '2024-11-23'

    # Generar URLs de los gráficos desde la carpeta static
    context = {
        "grafico_3d_nacionalidades": generar_html_imagen_static('Nacionalidades', 'cubo_nacionalidad.png'),
        "grafico_3d_turisticas": generar_html_imagen_static('Turisticas', 'cubo_turistica.png'),
        "grafico_2d_nacionalidades": generar_html_imagen_static('Nacionalidades', 'analisis_2d_nacionalidad.png'),
        "grafico_2d_turisticas": generar_html_imagen_static('Turisticas', 'analisis_2d_turistica.png'),
        "grafico_pastel_nacionalidades": generar_html_imagen_static('Nacionalidades', 'pastel_nacionalidad.png'),
        "grafico_pastel_turisticas": generar_html_imagen_static('Turisticas', 'pastel_turistica.png'),
        "dias_nacionalidad": dias_nacionalidad,
        "dias_turistica": dias_turistica,
        "fecha_nacionalidad": fecha_nacionalidad,
        "fecha_turistica": fecha_turistica,
    }

    # Renderizar el template y pasar el contexto
    return render(request, 'webapp/panel_datos.html', context)

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
            cursor.execute("SELECT DISTINCT fecha_visualizacion FROM table_cube_nacionalidad ORDER BY fecha_visualizacion DESC;")
            resultados = cursor.fetchall()
        fechas = [{"valor": str(fila[0])} for fila in resultados]
        return JsonResponse({"resultados": fechas})
    except Exception as e:
        return JsonResponse({"error": str(e)})

# API para obtener los nombres únicos de Nacionalidades
def obtener_nombres_nacionalidades(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT nacionalidad_nombre FROM table_cube_nacionalidad ORDER BY nacionalidad_nombre DESC;")
            resultados = cursor.fetchall()
        nombres = [{"valor": fila[0]} for fila in resultados]
        return JsonResponse({"resultados": nombres})
    except Exception as e:
        return JsonResponse({"error": str(e)})

# API para obtener las fechas únicas de Turísticas
def obtener_fechas_turisticas(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT fecha_visualizacion FROM table_cube_turistica ORDER BY fecha_visualizacion DESC;")
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
