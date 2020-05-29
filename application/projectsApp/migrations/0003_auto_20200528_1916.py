# Generated by Django 3.0.6 on 2020-05-28 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
        ('projectsApp', '0002_auto_20200527_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projetoarea',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mainApp.Area'),
        ),
        migrations.DeleteModel(
            name='Area',
        ),
    ]
