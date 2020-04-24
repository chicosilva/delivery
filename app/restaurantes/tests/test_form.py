from django.test import TestCase
from produtos.forms import ProdutoForm
from lojistas.models import Lojista
from produtos.models import Produto


class ProdutoModelTest(TestCase):

    def setUp(self):

        lojista = Lojista(nome = "Francisco", email="test@teste.com", sobrenome= "de Assis")
        lojista.save()
        self.lojista = lojista

        produto = Produto()
        produto.nome = "teste"
        produto.valor = 10
        produto.lojista = lojista
        produto.codigo = 10
        produto.slug = 'teste'
        produto.save()

    def test_campos_corretos(self):

        form = ProdutoForm()
        campos = ['lojista', 'nome', 'descricao', 
            'quantidade', 'codigo', 'valor', 'aplicacao', 'imagem']

        self.assertSequenceEqual(campos, list(form.fields))

    def test_codigo_existe(self):
        
        form = self.dados_form(codigo=10)
        self.assertListEqual(['codigo'], list(form.errors))

    def test_valor_menor_zero(self):
        
        form = self.dados_form(valor=0, codigo=10)

        self.assertListEqual(['codigo', 'valor'], list(form.errors))

    def dados_form(self, **kwargs):

        lojista = self.lojista

        validos = dict(nome="Lanterna", quantidade=10, 
            codigo="554", valor=100, aplicacao="Corolla, Gol", imagem="produtos/imagem", lojista=lojista.pk)

        dados = dict(validos, **kwargs)
        form = ProdutoForm(dados)
        form.is_valid()

        return form