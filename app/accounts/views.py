# coding=utf-8

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from .models import User
from .forms import UserAdminForm, UserEditAdminForm
from django.db.models import Q
from core import list_paginator, list_filter, search_filter
from django.contrib import messages
from django.shortcuts import HttpResponse, redirect, reverse, render, \
    get_object_or_404, HttpResponse

from accounts.service import envia_dados_user
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy


@login_required(login_url=reverse_lazy('core:home'))
def lista(request):
    
    kwargs = list_filter(['cliente__pk'], request, data_inicio='created_at__gte', data_fim='created_at__lte')
    nome = search_filter('name', request)
    
    object_list = User.objects.\
        filter(**kwargs).\
        filter(Q(**nome)).\
        order_by('name')
    
    dados = {
        'titulo': "Pesquisadores",
        'atendentes': list_paginator(request, object_list, 50),
    }
    
    return render(request, 'accounts/lista.html', dados)


@login_required(login_url=reverse_lazy('core:home'))
def novo(request):

    if request.method == 'POST':
    
        form = UserAdminForm(request.POST)
        
        if form.is_valid():

            user = form.save()

            envia_dados_user(user, request.POST.get('password'))

            messages.success(request, 'Cadastrado com sucesso!')
            return redirect(reverse('accounts:lista'))
        
    else:
        form = UserAdminForm()

    return render(request, 'accounts/novo.html', {'form': form, 'titulo': 'Novo'})


@login_required(login_url=reverse_lazy('core:home'))
def sair(request):
    logout(request)
    return redirect(reverse('core:home'))


@login_required(login_url=reverse_lazy('core:home'))
def editar(request, id):

    user = User.objects.get(pk=id)

    if request.method == 'POST':
    
        form = UserEditAdminForm(request.POST, instance=user)
        
        if form.is_valid():

            form.save()
            
            messages.success(request, 'Atualizado com sucesso!')
            return redirect(reverse('accounts:lista'))
        
    else:
        form = UserEditAdminForm(instance=user)

    dados = {'form': form, 'titulo': 'Editar', 'obj': user}
    return render(request, 'accounts/novo.html', dados)


@login_required(login_url=reverse_lazy('core:home'))
def editar_senha(request, id):

    user = User.objects.get(pk=id)

    if request.method == 'POST':
    
        form = PasswordChangeForm(request.POST, instance=user)
        
        if form.is_valid():

            form.save()
            
            messages.success(request, 'Atualizado com sucesso!')
            return redirect(reverse('accounts:lista'))
        
    else:
        form = PasswordChangeForm(user)

    dados = {'form': form, 'titulo': 'Editar', 'obj': user}
    return render(request, 'accounts/update_password.html', dados)