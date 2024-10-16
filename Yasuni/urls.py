from django.contrib import admin
from django.urls import path
from webapp import views as webapp_views
from Nacionalidades import views as nacionalidades_views
from Turisticas import views as turisticas_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views  # Importar las vistas genéricas de autenticación
from webapp import views as webapp_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', webapp_views.home, name='home'),
    path('login/', webapp_views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),



    path('quienes-somos/', webapp_views.quienes_somos, name='quienes_somos'),
    path('quienes-somos/<str:titulo>/<int:codigo>/', nacionalidades_views.detalle_nacionalidad,
         name='detalle_nacionalidad'),
    path('detalle-turismo/<str:titulo>/<int:codigo>/', turisticas_views.detalle_turismo, name='detalle_turismo'),

    path('mas_informacion/', webapp_views.mas_informacion, name='mas_informacion'),
    path('paginaActividades/', webapp_views.pagina_actividades, name='paginaActividades'),

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
    path('grafico_tiempo_visualizacion_nacionalidad/', nacionalidades_views.visualizar_tiempo_visualizacion_nacionalidad, name='visualizar_tiempo_visualizacion_nacionalidad'),
    path('grafico_tiempo_visualizacion_turistica/', turisticas_views.visualizar_tiempo_visualizacion_turistica, name='visualizar_tiempo_visualizacion_turistica'),
]
urlpatterns += staticfiles_urlpatterns()
