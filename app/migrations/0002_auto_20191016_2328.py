# Generated by Django 2.1.5 on 2019-10-16 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projeto',
            name='descricao',
            field=models.TextField(blank=True, max_length=4096, null=True),
        ),
    ]
