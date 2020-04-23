from django.db import models
import uuid
from core.models import ModelDefault, upload_image
from django.template.defaultfilters import slugify
import datetime
from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from django.template import Context


class Category(models.Model):
    
    title = models.CharField(max_length=150)
    status = models.BooleanField(default=True, blank=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.title


def banner_noticia():
    dia = datetime.date.today().strftime('%d/%m/%Y')
    mes = int(datetime.date.today().strftime('%m'))

    banner = Banner.objects.filter(status=1).filter(Q(dias__contains=dia) | Q(mes__contains=mes)).filter(setor=11).order_by('?').first()

    c = Context({'banner': banner})
    html_content = render_to_string('partials/banner-noticia.html', c)
    
    return html_content

def veja_tambem(noticia):
    return render_to_string('partials/veja-tambem.html', Context({'noticia': noticia}))


class New(models.Model):
    
    link = models.URLField(verbose_name='Link', max_length=800, null=True, blank=True)
    category = models.ForeignKey(Category, blank=False, null=False, on_delete=models.CASCADE)
    relevance = models.CharField(max_length=10, null=False, blank=False)
    author = models.CharField(max_length=255, null=True, blank=True, )
    title = models.CharField( max_length=255)
    cidade = models.CharField( max_length=255, null=True, blank=True, default=u"Patrocínio")
    agendamento = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False, blank=True)
    default_content = models.BooleanField(default=False, blank=True)
    enable_comment = models.BooleanField( default=True, blank=True)
    shared = models.BooleanField(default=True, blank=True)
    championship = models.BooleanField( default=False, blank=True)
    summary = models.CharField( max_length=255, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    nome_programa = models.CharField(max_length=255, null=True, blank=True, )
    ao_vivo = models.BooleanField(default=False, blank=True)
    busca = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_image, blank=True, null=True)
    access_number = models.IntegerField( default=1, null=True, blank=True)
    position = models.IntegerField( default=1, null=True, blank=True)
    total_comments = models.IntegerField( default=0, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField( default=False, blank=True)
    id_externo = models.IntegerField(null=True, blank=True, editable=False)
    posicao_banner = models.IntegerField( null=True, blank=True, )
    posicao_outra_noticia = models.IntegerField(  null=True, blank=True)
    
    def text_view(self):

        soup = BeautifulSoup(self.text, fromEncoding="UTF-8")

        try:
            banner = BeautifulSoup(banner_noticia())
            
            if self.posicao_banner:
                p = soup.findAll("p")[self.posicao_banner - 1]
            else:
                p = soup.findAll("p")[0]

            p.append(banner)

        except:
            pass

        soup = BeautifulSoup(soup.renderContents(), fromEncoding="UTF-8")

        try:
            veja_t = BeautifulSoup(veja_tambem(self))
            
            if self.posicao_outra_noticia:
                p = soup.findAll("p")[self.posicao_outra_noticia - 1]
            else:
                p = soup.findAll("p")[0]

            p.append(veja_t)

        except:
            pass

        return soup


def atualiza_clique_ph(entity):
    entity.access_number = entity.get_clique_redis()
    entity.save()

class Urna(models.Model): pass


class OutraNoticia(models.Model):

    new = models.ForeignKey(New,  on_delete=models.CASCADE)
    nome = models.CharField(max_length=150)
    link = models.CharField(max_length=150)
    position = models.IntegerField(  default=1, null=True, blank=True)


class Canditado(models.Model):
   
    nome = models.CharField(max_length=150)
    position = models.IntegerField( default=1, null=True, blank=True)
    image = models.ImageField(upload_to=upload_image, blank=True, null=True)
    votos = models.IntegerField(  default=1)
    text = models.TextField( blank=False, null=False)
    cor = models.CharField(max_length=150,  null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.nome



class Vereador(models.Model):
    
    nome = models.CharField( max_length=150, blank=True, null=True)
    image = models.ImageField( upload_to=upload_image, blank=True, null=True)
    text = models.TextField( blank=True, null=True)


class Opcao(models.Model):


    new = models.ForeignKey(New, on_delete=models.CASCADE)
    title = models.CharField( max_length=150)
    position = models.IntegerField(  default=1, null=True, blank=True)
    status = models.BooleanField(default=False, blank=True)
    text = models.TextField(blank=False, null=False)
    video = models.TextField( blank=True, null=True)
    image = models.ImageField( upload_to=upload_image, blank=True, null=True)
    positive = models.IntegerField( default=1, editable=False)
    negative = models.IntegerField( default=0, editable=False)



class Vote(models.Model):
   
    opcao = models.ForeignKey(Opcao,  blank=False, null=False, on_delete=models.CASCADE)
    ip = models.CharField( max_length=300)


class Section(models.Model):
   
    status = models.BooleanField( default=False, blank=True)
    title = models.CharField(max_length=255)
    secao = models.CharField( max_length=80)
    slug = models.CharField( max_length=100)
    position = models.IntegerField(  default=1, null=True, blank=True)

 
class Cache(models.Model):
   
    tempo = models.IntegerField(  default=1,
                                null=False, blank=False)


class FanPage(models.Model):
   
    status = models.BooleanField( default=False, blank=True)
