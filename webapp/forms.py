# webapp/forms.py
from django import forms
from .models import UsuariosYasuni  # Asegúrate de que sea el modelo correcto

class LoginForm(forms.Form):
    Usuario = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario'})
    )
    Contraseña = forms.CharField(
        max_length=15,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
