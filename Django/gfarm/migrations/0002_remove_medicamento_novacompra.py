# Generated by Django 2.2.7 on 2019-11-20 01:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gfarm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicamento',
            name='novaCompra',
        ),
    ]
