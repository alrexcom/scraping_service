# Generated by Django 5.0.6 on 2024-07-24 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_vacancy_address_vacancy_company_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='opyt',
            field=models.CharField(default=None, max_length=150, null=True, verbose_name='Опыт'),
        ),
    ]