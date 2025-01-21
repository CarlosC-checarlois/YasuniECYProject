from Nacionalidades import views as nacionalidades_views
from Turisticas import views as turisticas_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from webapp import views as webapp_views

urlpatterns = [
    path('', webapp_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', webapp_views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('estudiantes/', webapp_views.estudiantes, name='estudiantes'),
    path('procesar_imagen_2d_nacionalidades/', webapp_views.procesar_imagen_2d_nacionalidades,
         name='procesar_imagen_2d_nacionalidades'),
    path('procesar_imagen_2d_turisticas/', webapp_views.procesar_imagen_2d_turisticas,
         name='procesar_imagen_2d_turisticas'),
    path('quienes-somos/', webapp_views.quienes_somos, name='quienes_somos'),
    path('quienes-somos/<str:titulo>/<int:codigo>/', nacionalidades_views.detalle_nacionalidad,
         name='detalle_nacionalidad'),
    path('detalle-turismo/<str:titulo>/<int:codigo>/', turisticas_views.detalle_turismo, name='detalle_turismo'),

    path('mas_informacion/', webapp_views.mas_informacion, name='mas_informacion'),
    path('paginaActividades/', webapp_views.pagina_actividades, name='paginaActividades'),
    path('paginaActividades/documentacion/', webapp_views.documentacion, name='documentacion'),

    path('paginaActividades/datos/', webapp_views.panel_datos, name='informacion_datos'),
    path('obtener_imagen/<str:imgCodigo>/', webapp_views.obtener_imagen, name='obtener_imagen'),

    path('editar_nacionalidad/<int:nacCodigo>/', nacionalidades_views.editar_nacionalidad, name='editar_nacionalidad'),
    path('eliminar_nacionalidad/<int:nacCodigo>/', nacionalidades_views.eliminar_nacionalidad,
         name='eliminar_nacionalidad'),
    path('crear-nacionalidad/', nacionalidades_views.crear_nacionalidad, name='crear_nacionalidad'),

    path('guardar-tiempo-visualizacion/<int:nacCodigo>/',
         nacionalidades_views.guardar_tiempo_visualizacion_nacionalidad,
         name='guardar_tiempo_visualizacion_nacionalidad'),

    path('guardar-tiempo-visualizacion-turistica/<int:turCodigo>/',
         turisticas_views.guardar_tiempo_visualizacion_turistica, name='guardar_tiempo_visualizacion_turistica'),

    path('editar_turismo/<int:turCodigo>', turisticas_views.editar_turismo, name='editar_turismo'),
    path('eliminar_turismo/<int:turCodigo>/', turisticas_views.eliminar_turismo, name='eliminar_turismo'),
    path('crear-turismo/', turisticas_views.crear_turismo, name='crear_turismo'),

    path('informacion-nacionalidad/', webapp_views.informacion_nacionalidad, name='informacion_nacionalidad'),
    path('informacion_turismo/', webapp_views.informacion_turismo, name='informacion_turismo'),
    path('gestionar-turismo/', turisticas_views.gestionar_turismo, name='gestionar_turismo'),


    path('grafico_tiempo_visualizacion_nacionalidad/',
         nacionalidades_views.visualizar_tiempo_visualizacion_nacionalidad,
         name='visualizar_tiempo_visualizacion_nacionalidad'),
    path('grafico_tiempo_visualizacion_turistica/', turisticas_views.visualizar_tiempo_visualizacion_turistica,
         name='visualizar_tiempo_visualizacion_turistica'),
    # Gráficos 2D
    path('grafico_2d_nacionalidad/', nacionalidades_views.visualizar_analisis_2d_nacionalidad,
         name='visualizar_analisis_2d_nacionalidad'),
    path('grafico_2d_turistica/', turisticas_views.visualizar_analisis_2d_turistica,
         name='visualizar_analisis_2d_turistica'),
    path('grafico_pastel_nacionalidad/', nacionalidades_views.visualizar_pastel_nacionalidad,
         name='visualizar_pastel_nacionalidad'),
    path('grafico_pastel_turistica/', turisticas_views.visualizar_pastel_turistica, name='visualizar_pastel_turistica'),

    # API para fechas y nombres de Nacionalidades
    path('api/obtener_fechas_nacionalidades/', webapp_views.obtener_fechas_nacionalidades,
         name='obtener_fechas_nacionalidades'),
    path('api/obtener_nombres_nacionalidades/', webapp_views.obtener_nombres_nacionalidades,
         name='obtener_nombres_nacionalidades'),
    # API para fechas y nombres de Turísticas
    path('api/obtener_fechas_turisticas/', webapp_views.obtener_fechas_turisticas, name='obtener_fechas_turisticas'),
    path("actualizar-imagenes/", webapp_views.manejador_actualizacion_imagenes, name="actualizar_imagenes"),

    path('api/obtener_nombres_turisticas/', webapp_views.obtener_nombres_turisticas, name='obtener_nombres_turisticas'),
    path('actualizar-imagenes/', webapp_views.actualizar_imagenes, name='actualizar_imagenes'),
    path('obtener-imagen/<str:imgCodigo>/', webapp_views.obtener_imagen, name='obtener_imagen'),
    path('procesar_imagen_3d_nacionalidades/', webapp_views.procesar_imagen_3d_nacionalidades,
         name='procesar_imagen_3d_nacionalidades'),
    path('procesar_imagen_3d_turisticas/', webapp_views.procesar_imagen_3d_turisticas,
         name='procesar_imagen_3d_turisticas'),

]
urlpatterns += staticfiles_urlpatterns()
