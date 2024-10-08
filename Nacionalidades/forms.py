from django import forms
from .models import Nacionalidad

class NacionalidadForm(forms.ModelForm):
    class Meta:
        model = Nacionalidad
        fields = [
            'catXnacNombre',
            'nacTitulo_1',
            'nacDescripcion_1',
            'nacURLImagen_1',
            'nacTitulo_2',
            'nacDescripcion_2',
            'nacURLImagen_2',
            'nacTitulo_3',
            'nacDescripcion_3',
            'nacURLImagen_3',
        ]
        widgets = {
            'nacDescripcion_1': forms.Textarea(attrs={'rows': 4}),
            'nacDescripcion_2': forms.Textarea(attrs={'rows': 4}),
            'nacDescripcion_3': forms.Textarea(attrs={'rows': 4}),
        }
