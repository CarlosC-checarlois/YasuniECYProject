# webapp/forms.py
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu usuario'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Ingresa tu contraseña'})
    )

    def clean_username(self):
        data = self.cleaned_data['username']
        if not data:
            raise forms.ValidationError('El nombre de usuario es obligatorio.')  # Mensaje de error personalizado
        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        if not data:
            raise forms.ValidationError('La contraseña es obligatoria.')  # Mensaje de error personalizado
        return data

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