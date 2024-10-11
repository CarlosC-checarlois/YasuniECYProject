from django.urls import path
from . import views

urlpatterns = [
    path('editar_nacionalidad/<int:nacCodigo>/', views.editar_nacionalidad, name='editar_nacionalidad'),
    path('eliminar_nacionalidad/<int:nacCodigo>/', views.eliminar_nacionalidad, name='eliminar_nacionalidad'),
    path('crear-nacionalidad/', views.crear_nacionalidad, name='crear_nacionalidad'),
    path('quienes-somos/<str:titulo>/<int:codigo>/', views.detalle_nacionalidad, name='detalle_nacionalidad'),
    path('guardar-tiempo-visualizacion-nacionalidad/<int:nacCodigo>/', views.guardar_tiempo_visualizacion_nacionalidad,
         name='guardar_tiempo_visualizacion_nacionalidad'),
]