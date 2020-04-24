from django.test import TestCase
from produtos.models import Produto
from lojistas.models import Lojista
from model_mommy import mommy


class ProdutoModelTest(TestCase):

    def setUp(self):
        
        lojista = Lojista(nome = "Francisco", email="test@teste.com", sobrenome = "de Assis")
        lojista.save()
        
        self.obj = Produto(
            nome='Lanterna',
            slug='lanterna',
            codigo='123',
            valor=10,
            aplicacao="Gol, Corolla",
            lojista=lojista,
        )

        self.obj.save()

    def test_create(self):
        "Testa criação do model"
        self.assertTrue(Produto.objects.exists())

    def test_se_valor_maior_que_zero(self):
        self.assertGreater(self.obj.valor, 0)
        