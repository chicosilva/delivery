from django import forms
from noticias.models import New


class NotificaForm(forms.ModelForm):

    class Meta:
        model = New
        fields = ['title', 'category', 'summary', 'text']

   