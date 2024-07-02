# Generated by Django 5.0.6 on 2024-07-02 10:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finding', '0006_remove_vacancy_timestamps'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='timestamp',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
