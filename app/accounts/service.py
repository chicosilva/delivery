# -*- coding: utf-8 -*-

from django.conf import settings
from core.models import envia_email


def envia_dados_user(user, senha):

    dados = {
        
        'user': user,
        'senha': senha,
        'assunto_email': u"Dados de acesso",
        'html': 'accounts/email-dados-acesso.html',
        'email_destino': user.email,
        'nome_remetente': "CTMS",
    }
     
    envia_email(dados)