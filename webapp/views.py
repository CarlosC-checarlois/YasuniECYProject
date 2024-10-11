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


value = True

def home(request):
    return render(request, 'webapp/index.html')


def quienes_somos(request):
    nacionalidades = Nacionalidad.objects.all()
    return render(request, 'webapp/quienesSomos.html', {'nacionalidades': nacionalidades})

def mas_informacion(request):
    actividades_turisticas = Turistica.objects.all()
    return render(request, 'webapp/masInformacion.html', {
        'actividades_turisticas': actividades_turisticas
    })


def login_view(request):
    global value
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('Usuario')
            password = form.cleaned_data.get('Contraseña')

            try:
                usuario = UsuariosYasuni.objects.get(usuario=username)
                if usuario.clave == password:
                    # Inicia la sesión usando el login manual
                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_nombre'] = usuario.usuario
                    value = True



                    return redirect(request.GET.get('next', 'paginaActividades'))  # Redirige a la página de actividades
                else:
                    error_message = "Usuario o contraseña incorrectos."
            except UsuariosYasuni.DoesNotExist:
                error_message = "Usuario o contraseña incorrectos."
    else:
        form = LoginForm()

    return render(request, 'webapp/login.html', {'form': form, 'error_message': error_message})



def informe_turisticas(request):

    return render(request, 'informe_turisticas.html', context)


def pagina_actividades(request):
    global value
    # Verifica si la sesión tiene un usuario activo
    if not value:
        return redirect('login')  # Redirige a la página de login si no hay usuario en la sesión

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

    # Datos para turísticas
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

    # Pasar los dos contextos al render
    return render(request, 'webapp/paginaActividades.html', {
        'contexto_nacionalidades': contexto_nacionalidades,
        'contexto_turistica': contexto_turistica,
    })

    return render(request, 'webapp/paginaActividades.html')

def informacion_nacionalidad(request):
    global value
    if not value:
        return redirect('login')

    nacionalidades = Nacionalidad.objects.all()
    return render(request, 'Nacionalidades/gestionarNacionalidad.html', {
        'nacionalidades': nacionalidades
    })

def informacion_turismo(request):
    global value
    if not value:
        return redirect('login')

    turismos = Turistica.objects.all()
    return render(request, 'Turisticas/gestionarTurismo.html', {
        'turismos': turismos
    })

def logout_view(request):
    global value
    value = False
    return redirect('login')  # Redirigir a la página de inicio de sesión

def detalle_nacionalidad(request, titulo, codigo):
    nacionalidad = get_object_or_404(Nacionalidad, nacTitulo_1=titulo, nacCodigo=codigo)
    return render(request, 'webapp/detalleNacionalidad.html', {'nacionalidad': nacionalidad})
