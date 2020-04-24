from django.db import models
import uuid
from core.models import ModelDefault, upload_image


class Restaurante(ModelDefault):
    
    nome = models.CharField(max_length=150)
    email = models.EmailField(max_length=90)
    telefone = models.CharField(max_length=20)
    ativo = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.nome


