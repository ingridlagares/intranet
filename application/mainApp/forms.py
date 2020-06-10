from django import forms
from django_select2.forms import Select2MultipleWidget
from .models import Pessoa
from datetime import datetime

class PessoaEditForm(forms.ModelForm):
    cpf = forms.CharField(max_length=11, label='CPF')
    phone = forms.CharField(max_length=14, required=False, label='Telefone')
    email_pessoal = forms.EmailField(max_length=255, required=False, label='Email Pessoal')
    facebook = forms.CharField(max_length=255, required=False, label='Facebook')
    instagram = forms.CharField(max_length=255, required=False, label='Instagram')
    linkedin = forms.CharField(max_length=255, required=False, label='Linkedin')
    twitter = forms.CharField(max_length=255, required=False, label='Twitter')
    estrangeiro = forms.BooleanField(label='Estrangeiro', required=False)
    documento = forms.CharField(max_length=255, required=False, label='Documento')

    class Meta:
        model = Pessoa
        fields = [
            'cpf',
            'phone',
            'email_pessoal',
            'facebook',
            'instagram',
            'linkedin',
            'twitter',
            'estrangeiro',
            'documento'
        ]
