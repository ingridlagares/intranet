from django.db import models
from django.conf import settings
from mainApp import models as mainApp_models
import os
import time
from uuid import uuid4
import datetime


# oportunidade's imagem_divulgacao path and rename
# name = oportunidade.pk+ ext,
# name = random string + ext
# or name = oportunidade.pk + randomstring + ext
def path_and_rename_projeto(instance, filename):
    # the file will be uploaded on a folder /Current_Year
    upload_to = 'imagem_projeto/{}'.format(time.strftime("%Y/"))
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

class ProjetoIntegrante(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE,
                                blank=True, null=True)
    integrante = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.integrante.first_name} {self.integrante.last_name} - {self.projeto.titulo}'


class ProjetoArea(models.Model):
    projeto = models.ForeignKey('Projeto', on_delete=models.PROTECT,
                                blank=True, null=True)
    area = models.ForeignKey(mainApp_models.Area, on_delete=models.PROTECT,
                             blank=True, null=True)

    def __str__(self):
        return self.area.nome


# Create your models here.
class Projeto(models.Model):
    titulo = models.CharField(max_length=500, null=False, blank=False)
    descricao = models.TextField(max_length=4096, null=True, blank=True)
    sigla = models.CharField(max_length=500, null=True, blank=True)
    inicio = models.DateField(default=datetime.date.today)
    termino = models.DateField(null=True, blank=True)
    coordenador = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.PROTECT)
    agencia = models.CharField(max_length=500, null=True, blank=True)
    programa = models.CharField(max_length=500, null=True, blank=True)
    natureza = models.CharField(max_length=500, null=True, blank=True)
    situacao = models.CharField(max_length=500, null=True, blank=True)
    processo = models.CharField(max_length=500, null=True, blank=True)
    resolucao = models.CharField(max_length=500, null=True, blank=True)

    # The image will be saved in media/imagens_projeto/2019
    imagem_divulgacao = models.ImageField(upload_to=path_and_rename_projeto,
                                          blank=True, null=True)

    def __str__(self):
        return self.titulo
