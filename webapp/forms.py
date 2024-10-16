# webapp/forms.py
from django import forms
from .models import UsuariosYasuni  # Asegúrate de que sea el modelo correcto
from django import forms
from django.contrib.auth.models import User


"""
class LoginForm(forms.Form):
    Usuario = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario'})
    )
    Contraseña = forms.CharField(
        max_length=15,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
"""
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            return forms.ValidationError('Las contraseñas no son iguales')
        return cd['password2']