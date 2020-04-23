# coding=utf-8

from django.conf.urls import url
from .views import *

urlpatterns = [
    
    url(r'^$', lista, name='lista'),
    url(r'^novo/$', novo, name='novo'),
    url(r'^sair/$', sair, name='sair'),
    url(r'^editar/(?P<id>\d+)$', editar, name='editar'),
    url(r'^editar-senha/(?P<id>\d+)$', editar_senha, name='editar-senha'),
    
]
