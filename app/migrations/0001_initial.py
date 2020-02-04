# Generated by Django 2.1.5 on 2019-10-16 23:17

import app.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=500)),
                ('descricao', models.CharField(blank=True, max_length=500, null=True)),
                ('sigla', models.CharField(blank=True, max_length=500, null=True)),
                ('inicio', models.DateField(default=datetime.date.today)),
                ('termino', models.DateField(blank=True, null=True)),
                ('agencia', models.CharField(blank=True, max_length=500, null=True)),
                ('programa', models.CharField(blank=True, max_length=500, null=True)),
                ('natureza', models.CharField(blank=True, max_length=500, null=True)),
                ('situacao', models.CharField(blank=True, max_length=500, null=True)),
                ('processo', models.CharField(blank=True, max_length=500, null=True)),
                ('resolucao', models.CharField(blank=True, max_length=500, null=True)),
                ('imagem_divulgacao', models.ImageField(blank=True, null=True, upload_to=app.models.path_and_rename_projeto)),
                ('coordenador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjetoArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.Area')),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.Projeto')),
            ],
        ),
        migrations.CreateModel(
            name='ProjetoIntegrante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('integrante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('projeto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.Projeto')),
            ],
        ),
    ]