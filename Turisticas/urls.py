from django.urls import path
from . import views
from django.shortcuts import render
from django.conf.urls import handler404

urlpatterns = [
    path('gestionar-turismo/', views.gestionar_turismo, name='gestionar_turismo'),
    path('crear-turismo/', views.crear_turismo, name='crear_turismo'),
    path('editar-turismo/<int:turCodigo>/', views.editar_turismo, name='editar_turismo'),
    path('eliminar-turismo/<int:turCodigo>/', views.eliminar_turismo, name='eliminar_turismo'),
    path('detalle-turismo/<str:titulo>/<int:codigo>/', views.detalle_turismo, name='detalle_turismo'),
    path('guardar-tiempo-visualizacion-turistica/<int:turCodigo>/', views.guardar_tiempo_visualizacion_turistica, name='guardar_tiempo_visualizacion_turistica'),

]
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404_view
