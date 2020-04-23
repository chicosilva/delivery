from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import NotificaForm
from noticias.models import New, Category


def lista(request):
    
    noticia = New.objects.all()

    dados = {
        'noticias': noticia
    }
    
    return render(request, 'noticias/lista.html', dados)


def add(request):
    
    #Category(title="Teste", status=1, slug="teste").save()
    #Category(title="Teste 2", status=1, slug="teste2").save()

    if request.method == 'POST':
        
        form = NotificaForm(request.POST, request.FILES)
        
        if form.is_valid():

            obj = form.save()
            messages.success(request, 'Cadastrado com sucesso!')
            return redirect(reverse('gestao:noticias:editar', kwargs={'id': obj.pk}))
        
    else:
        form = NotificaForm()

    dados = {
        'form': form
    }

    return render(request, 'noticias/add.html', dados)


def editar(request, id):
    
    noticia = New.objects.get(pk=id)

    if request.method == 'POST':
        
        form = NotificaForm(request.POST, request.FILES, instance=noticia)
        
        if form.is_valid():

            obj = form.save()
            messages.success(request, 'Cadastrado com sucesso!')
        
    else:
        form = NotificaForm(instance=noticia)

    dados = {
        'form': form
    }

    return render(request, 'noticias/add.html', dados)