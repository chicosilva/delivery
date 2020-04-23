from django.shortcuts import render, redirect, reverse
from core.decorators import access_required
from core import list_paginator, list_filter, search_filter
from django.contrib import messages
from .models import Evento


def lista(request):
    
    dados = {}
    
    return render(request, 'eventos/lista.html', dados)