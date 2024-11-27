from django.db import models

class UsuariosYasuni(models.Model):
    usuario = models.CharField(max_length=100)
    clave = models.CharField(max_length=15)
    email = models.CharField(max_length=150)

class imagenes(models.Model):
    imgCodigo = models.CharField(
        max_length=5,
        primary_key=True,
        choices=[
            ('IMG-1', 'IMG-1'),
            ('IMG-2', 'IMG-2'),
            ('IMG-3', 'IMG-3'),
            ('IMG-4', 'IMG-4'),
            ('IMG-5', 'IMG-5'),
            ('IMG-6', 'IMG-6'),
        ]
    )
    imgNombre = models.CharField(max_length=255)
    imgTipo = models.CharField(max_length=50)  # Ej: 'image/png', 'image/jpeg'
    imgTamanio = models.IntegerField()
    imgContenido = models.BinaryField()  # Almacena los datos binarios de la imagen

    def __str__(self):
        return self.imgNombre
