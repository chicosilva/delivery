from django.test import TestCase, Client
from produtos.forms import ProdutoForm
from lojistas.models import Lojista
from django.shortcuts import resolve_url as r


class ProdutoModelTest(TestCase):

    def setUp(self):
        
        lojista = Lojista(nome = "Francisco", email="test@teste.com", sobrenome= "de Assis")
        lojista.save()

        self.lojista = lojista

        self.client = Client()
        session = self.client.session
        session['lojista_pk'] = self.lojista.pk
        session.save()

        self.resp = self.client.get(r('produtos:novo'))
    
    def test_html(self):
        
        tags = (
            ('<form', 1),
            ('<input', 19),
            ('<textarea', 1),
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)
