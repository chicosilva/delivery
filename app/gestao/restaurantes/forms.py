from django import forms
from restaurantes.models import Restaurante


class RestauranteForm(forms.ModelForm):

    class Meta:
        model = Restaurante
        fields = ['nome', 'email', 'telefone', 'ativo', 'slug']

   