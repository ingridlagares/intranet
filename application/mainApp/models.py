
import os
import time
import datetime
from uuid import uuid4
from django.db import models
from django.conf import settings

PROFILE_CHOICES = (
    ('PROFESSOR', 'Professor'),
    ('FUNCIONARIO', 'Funcionário'),
    ('SUBSTITUTO', 'Substituto'),
    ('CONTRATADO', 'Contratado'),
)
# Create your models here.
class Area(models.Model):
    nome = models.CharField(max_length=500, null=False, blank=False)

    def __str__(self):
        return self.nome

class Pessoa(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT)
    cpf = models.CharField(unique=True, max_length=11, blank=True, null=True)
    phone = models.CharField(max_length=14, blank=True, null=True)
    email_pessoal = models.EmailField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    estrangeiro = models.BooleanField(blank=True, null=True)
    documento = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.user.username
