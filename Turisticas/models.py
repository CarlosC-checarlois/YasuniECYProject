from django.db import models

class CategoriasTuristicas(models.Model):
    catXturNombre = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.catXturNombre}"

class Turistica(models.Model):
    turCodigo = models.AutoField(primary_key=True)
    catXturNombre = models.ForeignKey(CategoriasTuristicas,on_delete=models.CASCADE)
    turTitulo_1 = models.CharField(max_length=255)
    turDescripcion_1 = models.TextField(max_length=2000)
    turURLImagen_1 = models.CharField(max_length=1000)
    turTitulo_2 = models.CharField(max_length=255)
    turDescripcion_2 = models.TextField(max_length=2000)
    turURLImagen_2 = models.CharField(max_length=1000)
    turTitulo_3 = models.CharField(max_length=255)
    turDescripcion_3 = models.TextField(max_length=2000)
    turURLImagen_3 = models.CharField(max_length=1000)
    turFechaCreacion = models.DateTimeField(auto_now_add=True)  # Toma la hora actual por defecto


class TiempoVisualizacion(models.Model):
    turistica = models.ForeignKey(Turistica, on_delete=models.CASCADE)  # Relación con la Turistica
    tiempo_visualizado = models.FloatField()  # Tiempo en segundos
    fecha_visualizacion = models.DateTimeField(auto_now_add=True)  # Fecha en que se registró la visualización

    def __str__(self):
        return f'{self.Turistica.turTitulo_1} - {self.tiempo_visualizado} segundos'
