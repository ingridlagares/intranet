from django import forms
from django_select2.forms import Select2MultipleWidget
from users.models import CustomUser
from .models import Projeto
from datetime import datetime


class ProjectCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        owner_pk = kwargs.pop('owner_pk')
        super(ProjectCreateForm, self).__init__(*args, **kwargs)

        members = [owner_pk]

        non_members = CustomUser.objects.exclude(
            pk__in=members
        ).order_by('first_name', 'last_name', 'email')

        self.fields['project_members'] = forms.ModelMultipleChoiceField(
            queryset=non_members,
            widget=Select2MultipleWidget,
            required=False,
            label="Integrante(s)"
        )

    titulo = forms.CharField(max_length=500, required=True, label='Título')
    descricao = forms.CharField(max_length=4096, widget=forms.Textarea,
                                required=False, label='Descricao')
    sigla = forms.CharField(max_length=500, required=False, label='Sigla')
    inicio = forms.DateField(required=True, widget=forms.SelectDateWidget)
    termino = forms.DateField(required=False, widget=forms.SelectDateWidget)
    agencia = forms.CharField(max_length=500, required=False, label='Agencia')
    programa = forms.CharField(max_length=500, required=False,
                               label='Programa', widget=forms.Textarea)
    natureza = forms.CharField(max_length=500, required=False,
                               label='Natureza')
    situacao = forms.CharField(max_length=500, required=False,
                               label='Situacao')
    processo = forms.CharField(max_length=500, required=False,
                               label='Processo')
    resolucao = forms.CharField(max_length=500, required=False,
                                label='Resolucao', widget=forms.Textarea)
    imagem_divulgacao = forms.ImageField(required=False)

    class Meta:
        model = Projeto
        fields = ['titulo', 'descricao', 'sigla', 'inicio',
                  'termino', 'agencia', 'programa',
                  'natureza', 'situacao', 'processo',
                  'resolucao', 'imagem_divulgacao']


class ProjectEditForm(forms.ModelForm):
    titulo = forms.CharField(max_length=500, required=True, label='Título')
    descricao = forms.CharField(max_length=4096, widget=forms.Textarea,
                                required=False, label='Descricao')
    sigla = forms.CharField(max_length=500, required=False, label='Sigla')
    inicio = forms.DateField(
        required=True,
        widget=forms.SelectDateWidget(
            years=range(1980, datetime.now().year+20)
        )
    )
    termino = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(
            years=range(1980, datetime.now().year+20)
        )
    )
    agencia = forms.CharField(max_length=500, required=False,
                              label='Agencia')
    programa = forms.CharField(max_length=500, required=False,
                               label='Programa', widget=forms.Textarea)
    natureza = forms.CharField(max_length=500, required=False,
                               label='Natureza')
    situacao = forms.CharField(max_length=500, required=False,
                               label='Situacao')
    processo = forms.CharField(max_length=500, required=False,
                               label='Processo')
    resolucao = forms.CharField(max_length=500, required=False,
                                label='Resolucao', widget=forms.Textarea)

    # The image will be saved in media/imagens_projeto/2019
    imagem_divulgacao = forms.ImageField(required=False)

    class Meta:
        model = Projeto
        fields = [
            'titulo', 'descricao', 'sigla', 'inicio',
            'termino', 'agencia', 'programa', 'natureza',
            'situacao', 'processo', 'resolucao', 'imagem_divulgacao'
        ]
