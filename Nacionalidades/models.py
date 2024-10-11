from django.db import models

class CategoriasNacionalidades(models.Model):
    catXnacNombre = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.catXnacNombre}"

class Nacionalidad(models.Model):
    nacCodigo = models.AutoField(primary_key=True)
    catXnacNombre = models.ForeignKey(CategoriasNacionalidades, on_delete=models.CASCADE)
    nacTitulo_1 = models.CharField(max_length=255)
    nacDescripcion_1 = models.TextField(max_length=2000)
    nacURLImagen_1 = models.CharField(max_length=1000)
    nacTitulo_2 = models.CharField(max_length=255)
    nacDescripcion_2 = models.TextField(max_length=2000)
    nacURLImagen_2 = models.CharField(max_length=1000)
    nacTitulo_3 = models.CharField(max_length=255)
    nacDescripcion_3 = models.TextField(max_length=2000)
    nacURLImagen_3 = models.CharField(max_length=1000)
    nacFechaCreacion = models.DateTimeField(auto_now_add=True)

class TiempoVisualizacion(models.Model):
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE)  # Relación con la Nacionalidad
    tiempo_visualizado = models.FloatField()  # Tiempo en segundos
    fecha_visualizacion = models.DateTimeField(auto_now_add=True)  # Fecha en que se registró la visualización

    def __str__(self):
        return f'{self.Nacionalidad.nacTitulo_1} - {self.tiempo_visualizado} segundos'
