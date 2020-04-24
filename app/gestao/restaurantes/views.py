from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import RestauranteForm
from restaurantes.models import Restaurante


def lista(request):
    
    restaurantes = Restaurante.objects.all()

    dados = {
        'restaurantes': restaurantes
    }
    
    return render(request, 'restaurantes/lista.html', dados)


def add(request):
    
    if request.method == 'POST':
        
        form = RestauranteForm(request.POST, request.FILES)
        
        if form.is_valid():

            obj = form.save()
            messages.success(request, 'Cadastrado com sucesso!')
            return redirect(reverse('gestao:restaurantes:lista'))
        
    else:
        form = RestauranteForm()

    dados = {
        'form': form
    }

    return render(request, 'restaurantes/add.html', dados)


def editar(request, id):
    
    noticia = Restaurante.objects.get(pk=id)

    if request.method == 'POST':
        
        form = RestauranteForm(request.POST, request.FILES, instance=noticia)
        
        if form.is_valid():

            obj = form.save()
            messages.success(request, 'Atualizado com sucesso!')
            return redirect(reverse('gestao:restaurantes:lista'))
        
    else:
        form = RestauranteForm(instance=noticia)

    dados = {
        'form': form
    }

    return render(request, 'restaurantes/add.html', dados)