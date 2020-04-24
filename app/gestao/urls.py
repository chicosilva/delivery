
from django.urls import path
from django.conf.urls import include

urls_gestao = [
    path('restaurantes/', include(('gestao.restaurantes.urls', 'noticias'), namespace='restaurantes'))
]
