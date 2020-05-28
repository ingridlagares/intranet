# Generated by Django 3.0.6 on 2020-05-27 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projectsApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projetointegrante',
            name='integrante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projetointegrante',
            name='projeto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projectsApp.Projeto'),
        ),
        migrations.AddField(
            model_name='projetoarea',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projectsApp.Area'),
        ),
        migrations.AddField(
            model_name='projetoarea',
            name='projeto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projectsApp.Projeto'),
        ),
        migrations.AddField(
            model_name='projeto',
            name='coordenador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
