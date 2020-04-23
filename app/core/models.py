from django.conf import settings
from django.template.defaultfilters import slugify
from django.db import models
from django.template import Context
import uuid
import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string


class CustomManager(models.Manager):
    def get_queryset(self):
        return super(CustomManager, self).get_queryset().filter(data_cancelamento__isnull=True)

class RegistroCanceladoManager(models.Manager):
    def get_queryset(self):
        return super(RegistroCanceladoManager, self).get_queryset().filter(data_cancelamento__isnull=False)


class ModelDefault(models.Model):
    class Meta:
        abstract = True
    
    created_at = models.DateTimeField( editable=False, auto_now_add=True)
    data_cancelamento = models.DateTimeField( editable=False, null=True, blank=True)
    update_at = models.DateTimeField(editable=False, auto_now=True)
    
    objects = CustomManager()
    cancelados = RegistroCanceladoManager()

    def cancela_registro(self):
        self.data_cancelamento = datetime.datetime.now()
        return self

    def data_pt(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M")

    def data_cancelamento_formatada(self):

        if self.data_cancelamento:
            return self.data_cancelamento.strftime("%d/%m/%Y %H:%M")

        return ''


def upload_image(instance, filename):
    fname = slugify(filename[:-4])
    return '%s/%s.%s' % (instance.__class__.__name__.lower(), fname, filename.split('.')[-1])

