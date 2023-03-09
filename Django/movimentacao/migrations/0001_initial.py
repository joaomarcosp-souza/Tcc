# Generated by Django 2.2.7 on 2019-11-20 01:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gfarm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transferencia_Medicamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data Transeferêcia')),
                ('quantidade_transferida', models.FloatField()),
                ('fazenda_destino', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destino_medicamento', to='gfarm.Fazenda')),
                ('fazenda_origem', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='origem_medicamento', to='gfarm.Fazenda')),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gfarm.Medicamento')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transeferêcia de medicamento',
                'verbose_name_plural': 'Transeferêcias de medicamentos',
            },
        ),
        migrations.CreateModel(
            name='Transferencia_Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data Transeferêcia')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gfarm.Animal')),
                ('fazenda_destino', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destino', to='gfarm.Fazenda')),
                ('fazenda_origem', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='origem', to='gfarm.Fazenda')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transeferêcia de animal',
                'verbose_name_plural': 'Transeferêcias de animais',
            },
        ),
        migrations.CreateModel(
            name='Transferencia_Alimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data Transeferêcia')),
                ('quantidade_transferida', models.FloatField()),
                ('alimento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gfarm.Alimento')),
                ('fazenda_destino', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='destino_alimento', to='gfarm.Fazenda')),
                ('fazenda_origem', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='origem_alimento', to='gfarm.Fazenda')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transeferêcia de alimento',
                'verbose_name_plural': 'Transeferêcias de alimentos',
            },
        ),
    ]