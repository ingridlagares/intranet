import django.dispatch

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from users.models import CustomUser
from mainApp.models import Pessoa

def create_pessoa(sender, instance, signal, *args, **kwargs):
    if sender is CustomUser and not Pessoa.objects.filter(user=instance):
        pessoa = Pessoa.objects.create(
           user=instance,
        )
post_save.connect(create_pessoa, sender=CustomUser, dispatch_uid = "create_pessoa")
