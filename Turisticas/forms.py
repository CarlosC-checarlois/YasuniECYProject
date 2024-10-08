from django import forms
from .models import Turistica, CategoriasTuristicas

class TuristicaForm(forms.ModelForm):
    class Meta:
        model = Turistica
        fields = [
            'catXturNombre',
            'turTitulo_1', 'turDescripcion_1', 'turURLImagen_1',
            'turTitulo_2', 'turDescripcion_2', 'turURLImagen_2',
            'turTitulo_3', 'turDescripcion_3', 'turURLImagen_3'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Verifica si las categorías están disponibles
        self.fields['catXturNombre'].queryset = CategoriasTuristicas.objects.all()
