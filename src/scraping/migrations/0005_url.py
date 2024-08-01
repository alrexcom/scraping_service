# Generated by Django 5.0.6 on 2024-07-30 06:31

import django.db.models.deletion
import scraping.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0004_error'),
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_data', models.JSONField(default=scraping.models.defaults_url)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.city', verbose_name='Город')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.language', verbose_name='Язык программирования')),
            ],
            options={
                'unique_together': {('city', 'language')},
            },
        ),
    ]
