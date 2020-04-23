
from django.urls import path
from django.conf.urls import include

urls_gestao = [
    path('noticias/', include(('gestao.noticias.urls', 'noticias'), namespace='noticias'))
]
