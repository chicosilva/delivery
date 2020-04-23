# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from tools.utils import slug_pre_save_title, upload_image
from sorl.thumbnail import ImageField
from django.db.models import signals
from django.core.urlresolvers import reverse
from BeautifulSoup import BeautifulSoup
from caching.base import CachingManager, CachingMixin
from easy_thumbnails.files import get_thumbnailer
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from image_cropping import ImageRatioField
import redis
from django.template import Context
from banner.models import Banner
from django.db.models import Q
import datetime
from django.template.loader import render_to_string

RELEVANCE = (('2', u'Normal'),
             ('1', u'Destaque'),
             ('3', u'Urgente'),)

AUTHOR = (('1', u'Maurício Rocha'),
          ('2', u'Farley Rocha'),)


class Fenamilho(models.Model):
    class Meta:
        verbose_name = _(u'Fenamilho')
        verbose_name_plural = _(u'Fenamilho')
        ordering = ['-pk']

    futebol = models.BooleanField( default=True, editable=False)
    title = models.TextField(verbose_name=_(u'Título'), max_length=255)
    descricao = models.TextField(verbose_name=_(u'Descrição'), max_length=1200, blank=True, null=True)
    status = models.BooleanField(verbose_name=_(u'Status'), default=True, blank=True)
    destaque = models.BooleanField(verbose_name=_(u'Destaque'), default=True, blank=True)
    image = ImageField(verbose_name=_(u'Imagem'), upload_to=upload_image, blank=True, null=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name=_(u'Data de cadastro'), editable=True)
    video = models.CharField(verbose_name=_(u'Video'), max_length=255, blank=True, null=True)
    cropping = ImageRatioField('image', '660x360')
    positive = models.IntegerField(verbose_name=_(u'P'), max_length=11, default=1, null=True, blank=True, editable=False)
    negative = models.IntegerField(verbose_name=_(u'P'), max_length=11, default=1, null=True, blank=True, editable=False)

    def get_absolute_url(self):
        
        if self.futebol:
            return reverse('futebol:detalhes', args=[str(self.slug), str(self.id)])
            
        return reverse('fenamilho:detalhes', args=[str(self.slug), str(self.id)])

    def __unicode__(self):
        return u'%s' % self.title


class Autor(models.Model):
    class Meta:
        verbose_name = _(u'Autor')
        verbose_name_plural = _(u'Autor')
        ordering = ['title']

    title = models.CharField(verbose_name=_(u'Nome'), max_length=150)

    def __unicode__(self):
        return u'%s' % self.title


class Category(CachingMixin, models.Model):
    class Meta:
        verbose_name = _(u'Categoria')
        verbose_name_plural = _(u'Categorias')
        ordering = ['title']
    
    title = models.CharField(verbose_name=_(u'Nome'), max_length=150)
    status = models.BooleanField(verbose_name=_(u'Status'), default=True, blank=True)
    slug = models.SlugField(max_length=100)

    def get_news_by_category(self):
        return reverse('new:get_news_by_category', args=[str(self.slug)])

    def __unicode__(self):
        return u'%s' % self.title

    objects = CachingManager()


class ImageProv(models.Model):
    class Meta:
        verbose_name = _(u'Imagens e Arquivos')
        verbose_name_plural = _(u'Imagens e Arquivos')
        ordering = ['-id']

    image = ImageField(verbose_name=_(u'Arquivo ou imagem'), upload_to=upload_image, blank=True, null=True)
    title = models.CharField(verbose_name=_(u'Descrição'), max_length=150, blank=True, null=True)

    def get_full_image(self):
        return self.image.url

    get_full_image.allow_tags = True
    get_full_image.short_description = 'Link'

    def get_image(self):
        thumb_url = get_thumbnailer(self.image).get_thumbnail({'size': (160, 95), 'crop': True}).url

        return u"<img src='%s' />" % thumb_url

    get_image.allow_tags = True
    get_image.short_description = 'Arquivo'

    def __unicode__(self):
        return u'%s' % self.image

def banner_noticia():
    dia = datetime.date.today().strftime('%d/%m/%Y')
    mes = int(datetime.date.today().strftime('%m'))

    banner = Banner.objects.filter(status=1).filter(Q(dias__contains=dia) | Q(mes__contains=mes)).filter(setor=11).order_by('?').first()

    c = Context({'banner': banner})
    html_content = render_to_string('partials/banner-noticia.html', c)
    
    return html_content

def banner_noticia_mobile():
    dia = datetime.date.today().strftime('%d/%m/%Y')
    mes = int(datetime.date.today().strftime('%m'))

    banner = Banner.objects.filter(status=1).filter(Q(dias__contains=dia) | Q(mes__contains=mes)).filter(setor=11).order_by('?').first()
    c = Context({'banner': banner})
    html_content = render_to_string('partials/banner-noticia-mobile.html', c)
    
    return html_content

def veja_tambem(noticia):
    return render_to_string('partials/veja-tambem.html', Context({'noticia': noticia}))

def veja_tambem_mobile(noticia):
    return render_to_string('partials/veja-tambem-mobile.html', Context({'noticia': noticia}))


class New(CachingMixin, models.Model):
    class Meta:
        verbose_name = _(u'Notícia')
        verbose_name_plural = _(u'Notícias')

    link = models.URLField(verbose_name=_(u'Link'), max_length=800, null=True, blank=True)
    is_mobile = False
    category = models.ForeignKey(Category, verbose_name=_(u'Categoria'), blank=False, null=False,
                                 related_name="catessgory")
    relevance = models.CharField(u"Relevância", max_length=10, choices=RELEVANCE, null=False, blank=False)
    author = models.CharField(verbose_name=_(u'Autor'), max_length=255, null=True, blank=True, )
    title = models.CharField(verbose_name=_(u'Título'), max_length=255)
    cidade = models.CharField(verbose_name=_(u'Cidade'), max_length=255, null=True, blank=True, default=u"Patrocínio")
    agendamento = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(verbose_name=_(u'Status'), default=False, blank=True)
    default_content = models.BooleanField(verbose_name=_(u'Conteúdo Padrão'), default=False, blank=True)
    enable_comment = models.BooleanField(verbose_name=_(u'Permitir comentários'), default=True, blank=True)
    shared = models.BooleanField(verbose_name=_(u'Compartilhar Facebook?'), default=True, blank=True)
    championship = models.BooleanField(verbose_name=_(u'Campeonato Minerio'), default=False, blank=True)
    summary = models.TextField(verbose_name=_(u'Descrição'), max_length=255, blank=False, null=False)
    text = models.TextField(verbose_name=_(u'Texto'), blank=False, null=False)
    
    nome_programa = models.CharField(verbose_name=_(u'Nome do Programa'), max_length=255, null=True, blank=True, )
    ao_vivo = models.BooleanField(default=False, blank=True)

    busca = models.TextField(blank=True, null=True)

    image = ImageField(verbose_name=_(u'Imagem'), upload_to=upload_image, blank=True, null=True)
    access_number = models.IntegerField(verbose_name=_(u'Acessos'), max_length=11, default=1, null=True, blank=True)
    position = models.IntegerField(verbose_name=_(u'Posição'), max_length=11, default=1, null=True, blank=True)
    total_comments = models.IntegerField(verbose_name=_(u'Comentários'), max_length=11, default=0, null=True,
                                         blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=False)
    created_at = models.DateTimeField(verbose_name=_(u'Data da notícia'), auto_now_add=False)
    sent = models.BooleanField(verbose_name=_(u'Enviado'), default=False, blank=True)
    id_externo = models.IntegerField(verbose_name=_(u'Posição'), max_length=11, null=True, blank=True, editable=False)
    posicao_banner = models.IntegerField(verbose_name=_(u'Posição do Banner'), max_length=11, null=True, blank=True, help_text=u"Por exemplo, 1, o banner aparecerá depois do primeiro parágrafo")
    
    posicao_outra_noticia = models.IntegerField(verbose_name=_(u'Posição de veja também'), max_length=11, null=True, blank=True)
    
    def get_amp_url(self):
        return reverse('new:amp', args=[str(self.slug), str(self.id)])

    def get_absolute_url(self):

        if self.link:
            return self.link
        
        return reverse('new:new_detail', args=[str(self.slug), str(self.id)])

    def set_clique_redis(self):
        
        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        if not r.get('new-{0}'.format(self.pk)):
            r.set('new-{0}'.format(self.pk), 1)

        count = r.get('new-{0}'.format(self.pk))

        r.set('new-{0}'.format(self.pk), int(count) + 1)

        return r.get('new-{0}'.format(self.pk))

    def get_clique_redis(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        return r.get('new-{0}'.format(self.pk))

    def get_images(self, type):

        images = self.get_images_news.filter(marca=type).order_by('position')
        total_imgs = len(images)

        class_mobile = ''
        if self.is_mobile:
            class_mobile = 'popup-gallery'

        date = self.created_at.strftime('%d/%m/%Y')

        html = u'<div class="galeria-de-fotos %s"><h3><i class="ico-camera"></i> Imagens <span> atualizado em %s &bull; %s fotos</span></h3><ul id="items%s">' \
               % (class_mobile, date, total_imgs, type)

        for image in images:

            thumb_url = get_thumbnailer(image.image).get_thumbnail({'size': (160, 95), 'crop': True}).url
            summary = image.summary

            if image.summary is None: summary = ''

            if self.is_mobile:
                html += u'<li><a class="%s" href="%s" rel="gallery%s" data-fancybox-group="gallery%s" title="%s">' \
                        '<img src="%s" alt="%s" title="%s" class="img_album" /></a></li>' % (
                            type, image.image.url, type, type, summary, thumb_url, summary, summary)
            else:
                html += u'<li><a class="fancybox%s" href="%s" rel="gallery%s" data-fancybox-group="gallery%s" title="%s">' \
                        '<img src="%s" alt="%s" title="%s" class="img_album" /></a></li>' % (
                            type, image.image.url, type, type, summary, thumb_url, summary, summary)

        html += '</ul></div>'

        if not total_imgs: html = ''

        return html


    def get_default(self):

        type = 1
        images = self.get_images_news.filter(marca=type).order_by('position')
        total_imgs = len(images)

        class_mobile = ''
        if self.is_mobile:
            class_mobile = 'popup-gallery'

        date = self.created_at.strftime('%d/%m/%Y')

        html = u'<div class="galeria-de-fotos %s"><h3><i class="ico-camera"></i> Imagens <span> atualizado em %s &bull; %s fotos</span></h3><ul id="items%s">' \
               % (class_mobile, date, total_imgs, type)

        for image in images:

            thumb_url = get_thumbnailer(image.image).get_thumbnail({'size': (160, 95), 'crop': True}).url
            summary = image.summary

            if image.summary is None: summary = ''

            if self.is_mobile:
                html += u'<li><a class="%s" href="%s" rel="gallery%s" data-fancybox-group="gallery%s" title="%s">' \
                        '<img src="%s" alt="%s" title="%s" class="img_album" /></a></li>' % (
                            type, image.image.url, type, type, summary, thumb_url, summary, summary)
            else:
                html += u'<li><a class="fancybox%s" href="%s" rel="gallery%s" data-fancybox-group="gallery%s" title="%s">' \
                        '<img src="%s" alt="%s" title="%s" class="img_album" /></a></li>' % (
                            type, image.image.url, type, type, summary, thumb_url, summary, summary)

        html += '</ul></div>'

        if not total_imgs: html = ''

        return html


    def text_view(self):

        soup = BeautifulSoup(self.text, fromEncoding="UTF-8")

        try:
            marca1 = BeautifulSoup(self.get_images(1))
            soup.find("div", {"id": "marca"}).replaceWith(marca1)
        except:
            pass

        soup = BeautifulSoup(soup.renderContents(), fromEncoding="UTF-8")

        try:
            marca2 = BeautifulSoup(self.get_images(2))
            soup.find("div", {"id": "marca2"}).replaceWith(marca2)
        except:
            pass

        soup = BeautifulSoup(soup.renderContents(), fromEncoding="UTF-8")

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

    def text_view_mobile(self):

        soup = BeautifulSoup(self.text, fromEncoding="UTF-8")

        try:
            banner = BeautifulSoup(banner_noticia_mobile())
            
            if self.posicao_banner:
                p = soup.findAll("p")[self.posicao_banner - 1]
            else:
                p = soup.findAll("p")[0]

            p.append(banner)

        except:
            pass
        
        soup = BeautifulSoup(soup.renderContents(), fromEncoding="UTF-8")

        try:
            veja_t = BeautifulSoup(veja_tambem_mobile(self))
            
            if self.posicao_outra_noticia:
                p = soup.findAll("p")[self.posicao_outra_noticia - 1]
            else:
                p = soup.findAll("p")[0]

            p.append(veja_t)

        except:
            pass

        return soup 


    def __unicode__(self):
        return u'%s' % self.title

    objects = CachingManager()

def atualiza_clique_ph(entity):
    entity.access_number = entity.get_clique_redis()
    entity.save()

class Urna(CachingMixin, models.Model):
    class Meta:
        verbose_name = _(u'Urna')
        verbose_name_plural = _(u'Urnas')
        ordering = ['-id']

    apuradas = models.IntegerField(max_length=11, default=1)

    def __unicode__(self):
        return u'%s' % self.apuradas

    objects = CachingManager()


class OutraNoticia(models.Model):
    class Meta:
        verbose_name = _(u'Veja também')
        verbose_name_plural = _(u'Veja também')
        ordering = ['-id']
        
    new = models.ForeignKey(New, verbose_name=_(u'Notícia'), related_name='get_veja_tambem')
    nome = models.CharField(max_length=150)
    link = models.CharField(verbose_name=_(u'Link'), max_length=150)
    position = models.IntegerField(verbose_name=_(u'Posição'), max_length=11, default=1, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.nome


class Canditado(CachingMixin, models.Model):
    class Meta:
        verbose_name = _(u'Canditado')
        verbose_name_plural = _(u'Canditados')
        ordering = ['-id']
        db_table = 'new_eleicao'

    nome = models.CharField(verbose_name=_(u'Nome'), max_length=150)
    position = models.IntegerField(verbose_name=_(u'Posição'), max_length=11, default=1, null=True, blank=True)
    image = ImageField(verbose_name=_(u'Imagem'), upload_to=upload_image, blank=True, null=True)
    votos = models.IntegerField(verbose_name=_(u'Votos'), max_length=11, default=1)
    text = models.TextField(verbose_name=_(u'Texto'), blank=False, null=False)
    cor = models.CharField(verbose_name=_(u'Cor'), max_length=150, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.nome

    objects = CachingManager()

class Vereador(CachingMixin, models.Model):
    class Meta:
        verbose_name = _(u'Vereador')
        verbose_name_plural = _(u'Vereadores')

    nome = models.CharField(verbose_name=_(u'Nome'), max_length=150, blank=True, null=True)
    image = ImageField(verbose_name=_(u'Imagem'), upload_to=upload_image, blank=True, null=True)
    text = models.TextField(verbose_name=_(u'Texto'), blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.nome

    objects = CachingManager()


class Opcao(CachingMixin, models.Model):
    class Meta:
        verbose_name = _(u'Opção')
        verbose_name_plural = _(u'Opção')
        ordering = ['-id']

    new = models.ForeignKey(New, verbose_name=_(u'Notícia'), )
    title = models.CharField(verbose_name=_(u'Título'), max_length=150)
    position = models.IntegerField(verbose_name=_(u'Posição'), max_length=11, default=1, null=True, blank=True)
    status = models.BooleanField(verbose_name=_(u'Publicar?'), default=False, blank=True)
    text = models.TextField(verbose_name=_(u'Texto'), blank=False, null=False)
    video = models.TextField(verbose_name=_(u'Vídeo'), blank=True, null=True)
    image = ImageField(verbose_name=_(u'Imagem'), upload_to=upload_image, blank=True, null=True)
    positive = models.IntegerField(verbose_name=_(u'P'), max_length=11, default=1, editable=False)
    negative = models.IntegerField(verbose_name=_(u'N'), max_length=11, default=0, editable=False)

    def __unicode__(self):
        return u'%s' % self.title

    def positive_valid(self):
        return self.positive + 20

    def get_responses(self):
        responses = Opcao.objects.filter(comment=self.pk).filter(status=1).order_by('pk')[:15]
        responses.timeout = 30
        return responses

    objects = CachingManager()


class Vote(models.Model):
    class Meta:
        verbose_name = _(u'Voto')
        verbose_name_plural = _(u'Votos')

    opcao = models.ForeignKey(Opcao, verbose_name=_(u'Comentário'), blank=False, null=False)
    ip = models.CharField(verbose_name=_(u'Ip'), max_length=300)

    def __unicode__(self):
        return u'%s' % self.ip


class NoticiaDestaque(New):
    class Meta:
        proxy = True
        verbose_name = _(u'PH Destaque')
        verbose_name_plural = _(u'Notícias (Destaques)')

class Tv(New):
    class Meta:
        proxy = True
        verbose_name = _(u'PH TV')
        verbose_name_plural = _(u'PH TV')


class Section(CachingMixin, models.Model):
    class Meta:
        verbose_name = _(u'Ordem Home')
        verbose_name_plural = _(u'Ordem Home')
        ordering = ['position']

    status = models.BooleanField(verbose_name=_(u'Status'), default=False, blank=True)
    title = models.CharField(verbose_name=_(u'Nome'), max_length=255)
    secao = models.CharField(verbose_name=_(u'Seção'), max_length=80)
    slug = models.CharField(verbose_name=_(u'Slug'), max_length=100)
    position = models.IntegerField(verbose_name=_(u'Posição'), max_length=11, default=1, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.title

    objects = CachingManager()


class Cache(CachingMixin, models.Model):
    class Meta:
        verbose_name = _(u'Tempo Cache Notícia')
        verbose_name_plural = _(u'Tempo Cache Notícias')

    tempo = models.IntegerField(verbose_name=_(u'Tempo em segundos'), help_text="No mínimo 5", max_length=11, default=1,
                                null=False, blank=False)

    def __unicode__(self):
        return u'%s' % self.tempo


class FanPage(models.Model):
    class Meta:
        verbose_name = _(u'Fan Page')
        verbose_name_plural = _(u'Fan Page')

    status = models.BooleanField(verbose_name=_(u'Status'), default=False, blank=True)

    def __unicode__(self):  return u'%s' % self.status


def get_objects():
    qs = New.objects.filter(status=1)
    qs.timeout = 60
    return qs


@receiver(signals.pre_save, sender=New, weak=False, )
def presave_payment_model_check(sender, instance=None, created=False, **kwargs):
    
    if instance._state.adding is True:
        instance.slug = slugify(instance.title)
    
    instance.slug = slugify(instance.title)

def slug_pre_save_title_new(signal, instance, sender, **kwargs):
    if kwargs['created']:
        instance.slug = slugify(instance.title)


#signals.pre_save.connect(presave_payment_model_check, sender=New)
signals.pre_save.connect(slug_pre_save_title, sender=Category)
signals.pre_save.connect(slug_pre_save_title, sender=Fenamilho)
