from django.db import models

class UsuariosYasuni(models.Model):
    usuario = models.CharField(max_length=100)
    clave = models.CharField(max_length=15)
    email = models.CharField(max_length=150)

