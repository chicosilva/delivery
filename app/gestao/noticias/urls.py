from .views import *
from django.urls import path

urlpatterns = [
    path(r'', lista, name='lista'),
    path('add/', add, name='add'),
    path('editar/<int:id>/', editar, name='editar'),
]