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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data # obtiene un diccionario con los campos respectivos
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)  # Inicia la sesión del usuario
                    return redirect('paginaActividades')
                else:
                    return render(request, 'webapp/login.html', {'form': form, 'error_message': 'Cuenta de usuario inactiva.'})
            else:
                return render(request, 'webapp/login.html', {'form': form, 'error_message': 'Usuario o contraseña incorrectos.'})
    else:
        form = LoginForm()

    return render(request, 'webapp/login.html', {'form': form})

@login_required
def pagina_actividades(request):
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
    })

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
    return redirect('login')