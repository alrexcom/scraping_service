# Generated by Django 5.0.6 on 2024-07-01 15:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finding', '0003_alter_city_slug_vacancy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'verbose_name': 'Вакансию', 'verbose_name_plural': 'Вакансии'},
        ),
        migrations.AddField(
            model_name='vacancy',
            name='timestamp',
            field=models.DateField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finding.city', verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='company',
            field=models.CharField(max_length=250, verbose_name='Работодатель'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='description',
            field=models.TextField(verbose_name='Описание вакансии'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finding.language', verbose_name='Язык программирования'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='url',
            field=models.URLField(max_length=500, unique=True),
        ),
    ]